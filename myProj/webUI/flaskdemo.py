import random
from flask import Flask, request, jsonify

from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources=r'/*')
# 假设这是一些爬虫获取的数据
spider_data = [{'title': 'article 1', 'content': 'This is article 1.'}, {'title': 'article 2', 'content': 'This is article 2.'}]
data = []


@app.route('/start', methods=['POST'])
def start_spider():
    # 在这里进行开始爬虫的处理
    global data
    data.extend(spider_data) # 假设获取的数据与原有数据合并
    return 'Spider has started.'


@app.route('/data', methods=['GET'])
def get_data():
    # 在这里返回slave以及数据库各项性能指标，报文类型[[slave1*4],[slave2*4],[slave3*4],[redis*1],[mysql*3]]
    res=[]
    for i in range(0,4):
        res.append(random.randrange(1,100))
        res.append(random.randrange(1,100))
        res.append(random.randrange(1,100))
    res.append(random.randrange(1,10))
    for i in range(0,3):
        res.append(random.randrange(1,100))
    print("web ask",res)
    return jsonify(res)


@app.route('/reset', methods=['POST'])
def reset_data():
    # 在这里进行重置数据的处理
    global data
    data = []
    return 'Data has been reset.'


@app.route('/query', methods=['GET'])
def query_data():
    # 在这里进行查询数据的处理
    title = request.args.get('title')
    result = [d for d in data if d['title'] == title]
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=8000)