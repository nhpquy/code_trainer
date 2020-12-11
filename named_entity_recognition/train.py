#!/usr/bin/env python
# coding: utf8
"""Example of training an additional entity type

This script shows how to add a new entity type to an existing pretrained NER
model. To keep the example short and simple, only four sentences are provided
as examples. In practice, you'll need many more — a few hundred would be a
good start. You will also likely need to mix in examples of other entity
types, which might be obtained by running the entity recognizer over unlabelled
sentences, and adding their annotations to the training set.

The actual training is performed by looping over the examples, and calling
`nlp.entity.update()`. The `update()` method steps through the words of the
input. At each word, it makes a prediction. It then consults the annotations
provided on the GoldParse instance, to see whether it was right. If it was
wrong, it adjusts its weights so that the correct action will score higher
next time.

After training your model, you can save it to a directory. We recommend
wrapping models as Python packages, for ease of deployment.

For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities

Compatible with: spaCy v2.1.0+
Last tested with: v2.1.0
"""
from __future__ import unicode_literals, print_function

import hashlib
import json
import random
import time
from json import JSONDecodeError
from pathlib import Path

import spacy
from spacy.util import minibatch, compounding

from connector.pipelines import CrawlPipeline
from named_entity_recognition.train_data import TRAIN_DATA
from named_entity_recognition.test_data import TEST_DATA
# training data
# Note: If you're using an existing model, make sure to mix in examples of
# other entity types that spaCy correctly recognized before. Otherwise, your
# model might learn the new type, but "forget" what it previously knew.
# https://explosion.ai/blog/pseudo-rehearsal-catastrophic-forgetting
from utils import get_output_dir, get_output_file, get_input_file

default_output_dir = get_output_dir()

def evaluate(ner, textcat, texts, cats):
    docs = (ner(text) for text in texts)
    tp = 0.0  # True positives
    fp = 1e-8  # False positives
    fn = 1e-8  # False negatives
    tn = 0.0  # True negatives
    for i, doc in enumerate(textcat.pipe(docs)):
        gold = cats[i]
        # print("Test gold", gold)
        for label, score in doc.cats.items():
            print("test label", label)
            print("test score",score)
            if label not in gold:
                continue
            if label == "JOB":
                continue
            if score >= 0.5 and gold[label] >= 0.5:
                tp += 1.0
            elif score >= 0.5 and gold[label] < 0.5:
                fp += 1.0
            elif score < 0.5 and gold[label] < 0.5:
                tn += 1
            elif score < 0.5 and gold[label] >= 0.5:
                fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    if (precision + recall) == 0:
        f_score = 0.0
    else:
        f_score = 2 * (precision * recall) / (precision + recall)
    return {"precision": precision, "recall": recall, "f_score": f_score}

def main(model=None, new_model_name="new_model", output_dir=default_output_dir, n_iter=20, input_file=None, timestamp=None):
    if input_file is None:
        return
    """Set up the pipeline and entity recognizer, and train the new entity."""
    random.seed(0)
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("vi")  # create blank Language class
        print("Created blank 'vi' model")
    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe("ner")

    # add new entities label to entity recognizer
    ner.add_label('JOB')
    ner.add_label('LANGUAGE')
    ner.add_label('FRAMEWORK')
    ner.add_label('DEVICE')
    ner.add_label('KNOWLEDGE')
    ner.add_label('EXPERIENCE')

    if model is None:
        optimizer = nlp.begin_training()
    else:
        optimizer = nlp.resume_training()

    texts_test, labels_test = zip(*TEST_DATA)


    move_names = list(ner.move_names)
    # get names of other pipes to disable them during training
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        sizes = compounding(4., 32., 1.001)
        # batch up the examples using spaCy's minibatch
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            batches = minibatch(TRAIN_DATA, size=sizes)
            losses = {}
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.25, losses=losses)
                with ner.model.use_params(optimizer.averages):
                    # evaluate on the dev data split off in load_data()
                    scores = evaluate(nlp.tokenizer, ner, texts_test, labels_test)
            print("Losses", losses)
            print("Scores", scores)

    # Tao file output de luu noi dung train va phan tich du lieu da crawl
    # Duong dan tuyet doi cua file: /home/ngoc/PycharmProjects/code_trainer/outputs + file output
    output_file = get_output_file('output_%s' % input_file)

    # test the trained model
    # Doc file crawl duoi dang JSON
    input_file = get_input_file(input_file)
    with open(input_file, mode='r', encoding='utf8') as f_input:
        try:
            test_arr = json.load(f_input)
        #  => Tra ve ket qua output file va ket qua train la rong~ neu file crawl la rong~
        except JSONDecodeError:
            return None, {}, {}

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()

    results = []
    created_at = timestamp

    # CrawlPipeline la Class dung du lieu da train va phan tich de tao ra cac dinh, cac canh quan he trong Neo4j
    # Input: result da train va phan tich du lieu
    # Out: cac node, cac canh quan he cua cac field knowledge: job, language,... trong Neo4j
    crawl_pipeline = CrawlPipeline()

    # Tuan tu phan tich tung cau
    for test_obj in test_arr:
        json_text = json.dumps(test_obj, ensure_ascii=False)
        doc = nlp(json_text)

        entity_id = hashlib.md5(json_text.encode('utf-8')).hexdigest()

        # Object result la du lieu phan tich sau khi train
        # Bao gom entity: la cau phan tich:
        # 'entity_id' la hash md5 cua cau phan tich
        # 'created_at' la thoi gian tao => Cho nay co the thay the bang timestamp tao file luc ban dau
        # Sau nay dung field nay de query cac node, canh quan he WHERE created_at = ?
        result = {
            'entity': {
                'id': entity_id,
                'value': json_text,
                'created_at': created_at
            },
            'jobs': [],
            'languages': [],
            'frameworks': [],
            'knowledges': [],
            'devices': [],
            'experiences': []
        }

        # lan luot phan tich du lieu da train thanh cac object result, bao gom job, language, framework
        # moi object nay se co dang:
        # {
        #     "id": hash md5 cua gia tri object
        #     "value": gia tri raw cua object
        # }

        # Vi du:
        # {
        #     "id": hash_md5("Java"),
        #     "value": "Java"
        # }

        # ner.add_label('JOB')
        # ner.add_label('LANGUAGE')
        # ner.add_label('FRAMEWORK')
        # ner.add_label('DEVICE')
        # ner.add_label('KNOWLEDGE')
        # ner.add_label('EXPERIENCE')
        # vong lap for ben duoi de chuyen du lieu tu Object Train nay sang Object result da dinh nghia o dong 179,
        # cac knowledge thuoc chung 1 loai se dua vao 1 array voi key la voi key "type cua knowledge" + "s"
        for ent in doc.ents:
            if ent.label_ and ent.text:
                attribute = {
                    'id': hashlib.md5(ent.text.encode('utf-8')).hexdigest(),
                    'value': ent.text
                }
                # Sau khi da phan tich => them object nay vao dung array cua tung loai job, framework:
                # voi key "type cua knowledge" + "s" => jobs, frameworks,... (tuong trung cho array): jobs': []
                attribute_arr_key = ent.label_.lower() + 's'
                # them vao array voi ham append
                result[attribute_arr_key].append(attribute)

        # Gan du lieu da phan tich (Object result) vao pipeline
        crawl_pipeline.crawl_result = result
        # Thuc hien chuyen du lieu nay sang cac node va canh quan he trong graph cua Neo4j => transfrom_data
        # Moi result tuong ung voi 1 cau da duoc train va phan tich
        crawl_pipeline.transform_data()
        results.append(result)

        # Ghi du lieu da phan tich ra ra file (du lieu phan tich la du lieu dung` de tao object graph: result)
        with open(output_file, mode='w', encoding='utf8') as f_output:
            json.dump(results, f_output, ensure_ascii=False)

        # Tra ve file output cung voi cac thong tin danh gia'sau khi train
        return output_file, losses, scores
        # save model to output directory
        # if output_dir is not None:
        #     output_dir = Path(output_dir)
        #     if not output_dir.exists():
        #         output_dir.mkdir()
        #     nlp.meta["name"] = new_model_name  # rename model
        #     nlp.to_disk(output_dir)
        #     print("Saved model to", output_dir)


if __name__ == "__main__":
    main(input_file='tv.json')
