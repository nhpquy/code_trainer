import subprocess
import time

from flask import Flask, jsonify, request, Response, abort
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from crawl_spiders import crawl_spiders
from named_entity_recognition import train
from restful.response import ResponseBody
from utils import get_input_file, get_scracy_dir

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get():
    return jsonify({"status": "ok"})


@app.route("/api/v1/crawl", methods=["POST"])
def crawl_data():
    request_body = request.json
    crawl_output = request_body["output_file"]
    crawl_type = request_body["type"]

    spider = crawl_spiders[crawl_type]
    if spider is None:
        abort(406, 'Not support yet')

    crawl_output = get_input_file(crawl_output)

    start_time = time.time()
    subprocess.Popen(['scrapy', 'crawl', crawl_type, "-o", crawl_output], cwd=get_scracy_dir())
    end_time = time.time() - start_time

    result = {
        'crawl_time': end_time,
        'crawl_output': crawl_output
    }
    body = ResponseBody(0, result).to_json()
    response = Response(body, status=200, mimetype="application/json")
    return response


@app.route("/api/v1/train", methods=["POST"])
def train_data():
    request_body = request.json
    input_file = request_body["input_file"]

    start_time = time.time()
    output_file = train.main(input_file=input_file)
    end_time = time.time() - start_time

    result = {
        'train_time': end_time,
        'train_output': output_file
    }
    body = ResponseBody(0, result).to_json()
    response = Response(body, status=200, mimetype="application/json")
    return response


if __name__ == "__main__":
    print("Starting server")
    app.run(host='localhost', port=8082)
    print("Server end")
