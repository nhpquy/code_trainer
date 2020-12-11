import calendar
import subprocess
import time

from flask import Flask, request, Response, abort, render_template

from crawl_spiders import crawl_spiders
from named_entity_recognition import train
from restful.response import ResponseBody
from utils import get_input_file, get_scracy_dir

app = Flask(__name__, template_folder='templates')


@app.route("/api/v1/process", methods=["POST"])
# API cho viec crawl va train du lieu
def crawl_and_train():
    request_body = request.json
    # request gui len co dang:
    # {
    #     type: "type"
    # }
    # voi type o day la loai spider dung de crawl -> duoc dinh nghia trong file 'crawl_spiders'
    # type nay duoc lay trong select box tren front end va truyen len request khi goi API
    crawl_type = request_body["type"]

    #### B1: Tao spider crawl cho tung loai trang Web IT
    # lay Spider tuong ung voi loai Web IT
    spider = crawl_spiders[crawl_type]
    # neu khong co loai tuong ung thi throw loi
    if spider is None:
        abort(406, 'Not support yet')

    #### B2: Tao file crawl du lieu
    # tao file name cho file crawl du lieu tu web: file name = timestamp + type spider + json extension
    timestamp = calendar.timegm(time.gmtime())
    input_file = crawl_type + "_" + str(timestamp) + ".json";
    # lay duong dan tuyet doi cho file nay: /home/ngoc/PycharmProjects/code_trainer/inputs + ten file
    crawl_output = get_input_file(input_file)

    #### B3: Crawl du lieu bang Scrapy
    # mo 1 subprocess de crawl du lieu tu web
    # (scrapy yeu cau dung nguyen 1 process moi co the crawl du lieu => nen phai dung subprocess de chay ngam)
    # cau lenh chinh la command line de crawl du lieu theo tung spider
    crawl_start_time = time.time()
    p = subprocess.Popen(['scrapy', 'crawl', crawl_type, "-o", crawl_output], cwd=get_scracy_dir())

    # ham wait() nay dung de doi subprocess chay xong se notify cho process chinh chay tiep tuc
    # => doi crawl du lieu xong moi chay tiep
    p.wait()
    crawl_end_time = time.time() - crawl_start_time

    #### B4: Train du lieu va phan tich luu tru cac dinh, cac canh quan he vao database cua Neo4j => phuc vu Visualize
    train_start_time = time.time()
    # Ham train tra ve 3 loai du lieu:
    # + file luu du lieu da train va phan tich
    # + thong so train: that bai, thanh cong
    train_output, losses, scores = train.main(input_file=input_file, timestamp=timestamp)
    train_end_time = time.time() - train_start_time

    #### B5: Tra ve response cho front end
    result = {
        'timestamp': timestamp,
        'crawl_time': crawl_end_time,
        'train_time': train_end_time,
        'crawl_output': crawl_output,
        'train_output': train_output,
        'losses': losses,
        'scores': scores
    }
    body = ResponseBody(0, result).to_json()
    response = Response(body, status=200, mimetype="application/json")
    return response


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


# API nay dung de query database Neo4j va hien thi tren frontend
# Yeu cau la can truyen vao timestamp => query nhung node da crawl tai thoi diem do
# Can bo sung
@app.route('/visualize', methods=['GET', 'POST'])
def visualize():
    return render_template('visualize.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    print("Starting server")
    app.run(host='localhost', port=8082)
    print("Server end")
