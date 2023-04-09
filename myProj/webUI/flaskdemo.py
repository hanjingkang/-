import random
from flask import Flask, request, jsonify
import socket
from flask_cors import CORS

app = Flask(__name__)
globalClient=None
ifstartwork=None

CORS(app, resources=r'/*')
# 假设这是一些爬虫获取的数据
spider_data = [{'title': 'article 1', 'content': 'This is article 1.'}, {'title': 'article 2', 'content': 'This is article 2.'}]
data = []

@app.route('/test', methods=['POST'])
def test_connect():
    #测试连接
    global globalClient
    if(globalClient!=None):
        return "爬虫已经连接"
    globalClient= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    globalClient.connect(("192.168.112.143",8000))
    globalClient.send(bytes("2", 'utf-8'))
    data = globalClient.recv(1024)
    print(data)
    print(globalClient)
    return data


@app.route('/start', methods=['GET'])
def start_spider():
    # 在这里进行开始爬虫的处理,
    global globalClient
    global ifstartwork
    if(globalClient==None):
        updateblank=" "*random.randint(0,3)
        return updateblank+"请先连接爬虫"
    if(ifstartwork==False):
        globalClient.send(bytes("1", 'utf-8'))
        ifstartwork=True
        data = globalClient.recv(1024)
    else:
        #这里实时接收slave数据，另开一个套接字
        dataclient= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataclient.connect(("192.168.112.143",8000))
        dataclient.send(bytes("3", 'utf-8'))
        data = dataclient.recv(1024)
    
    print(data)
    return data


""" @app.route('/data', methods=['GET'])
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
    return jsonify(res) """


@app.route('/reset', methods=['POST'])
def reset_data():
    # 在这里进行停止、重置的操作
    global globalClient
    global ifstartwork
    if(globalClient==None):
        return "爬虫已关闭"

    globalClient.send(bytes("q", 'utf-8'))
    data = globalClient.recv(1024)
    print(data)
    globalClient.close()
    globalClient=None
    ifstartwork==False
    return data


""" @app.route('/query', methods=['GET'])
def query_data():
    # 在这里进行查询数据的处理
    title = request.args.get('title')
    result = [d for d in data if d['title'] == title]
    return jsonify(result) """


if __name__ == '__main__':
    app.run(port=8000)