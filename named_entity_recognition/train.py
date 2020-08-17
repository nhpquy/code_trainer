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

import json
import random
import uuid
from pathlib import Path

import spacy
from spacy.util import minibatch, compounding

from named_entity_recognition.train_data import TRAIN_DATA
# training data
# Note: If you're using an existing model, make sure to mix in examples of
# other entity types that spaCy correctly recognized before. Otherwise, your
# model might learn the new type, but "forget" what it previously knew.
# https://explosion.ai/blog/pseudo-rehearsal-catastrophic-forgetting
from utils import get_output_dir, get_output_file, get_input_file

default_output_dir = get_output_dir()


def main(model=None, new_model_name="new_model", output_dir=default_output_dir, n_iter=10, input_file=None):
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
                nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
            print("Losses", losses)

    output_file = get_output_file('output_%s' % input_file)

    # test the trained model
    input_file = get_input_file(input_file)
    with open(input_file, mode='r', encoding='utf8') as f_input:
        test_arr = json.load(f_input)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()

    results = []
    for test_obj in test_arr:
        json_text = json.dumps(test_obj, ensure_ascii=False)
        doc = nlp(json_text)

        result = {
            'ENTITY_ID': str(uuid.uuid1()),
            'ENTITY': json_text,
            'JOB': [],
            'LANGUAGE': [],
            'FRAMEWORK': [],
            'DEVICE': [],
            'KNOWLEDGE': [],
            'EXPERIENCE': []
        }
        for ent in doc.ents:
            result.get(ent.label_).append(ent.text)
        results.append(result)

    with open(output_file, mode='w', encoding='utf8') as f_output:
        json.dump(results, f_output, ensure_ascii=False)

    return output_file
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
