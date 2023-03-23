# 小学奥数题库建设
from re import S
import requests


class select_URL():
    def __init__(self) -> None:
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36 Edg/107.0.1418.42'
        }
        self.baseurl = 'https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz=Mzg3ODI1MTU2Mg==&album_id=1681667206486523905&count=10&uin=MTIwMzE5NjA0Mg%253D%253D&key=35546b77f2ad8d88e3d6c7bcb5a9fa53e9551b21619941de93af310fd5b0fbdab5d3c46180f9e70ae4fa7b6d3b19d6dbeccb3fb371ee32ff7d77c5bce313d332a7d1cece42178866947839fc6e19788287d8d7319d943c63458c9dd9111c59133777535710c9bfb9e776c468ffb5e50dc4a1bd4cd509620729866442dfe2ff87&pass_ticket=I5GEIm69Ny9xhRlHzmtluOPxLMnFd3jwyaVae48PwRcZCUKmei%25252BvOOpgbmmxlP2k&wxtoken=&devicetype=Windows%26nbsp%3B11%26nbsp%3Bx64&clientversion=6308001b&__biz=Mzg3ODI1MTU2Mg%3D%3D&appmsg_token=1192_dBpJVNJxb4kL9O1JebFBBeXC004uKR5XO_2mRQ~~&x5=0&f=json'
        self.Params = {'begin_msgid': '2247773399', 'begin_itemidx': '1'}
        self.urllist = []

    def getSingleUrl(self):
        r = requests.get(url=self.baseurl, params=self.Params,
                         headers=self.header)
        r = r.json()
        # 关于参数:每次请求得到的json,将最后一条数据的begin_msgid和begin_itemidx作为新的url请
        # 再次请求数据，循环遍历得到所有推文的URL数据
        for i in range(0, len(r['getalbum_resp']['article_list'])):
            self.urllist.append(r['getalbum_resp']['article_list'][i]["url"])
            self.Params["begin_msgid"] = r['getalbum_resp']['article_list'][i]['msgid']
            self.Params["begin_itemidx"] = r['getalbum_resp']['article_list'][i]['itemidx']

    def getAllUrl(self):
        while(1):
            try:
                self.getSingleUrl()
                print("url nums:", len(self.urllist))
            except Exception as e:
                print(e)
                break

select_URL().getAllUrl()