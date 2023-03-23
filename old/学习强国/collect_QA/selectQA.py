
from itertools import tee
import re
from matplotlib.pyplot import text
import requests
from lxml import etree


class select_QA_byURL():
    def __init__(self,url) -> None:
        self.url=url
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36 Edg/107.0.1418.42'
        }
        self.opt_mode=re.compile("<p>([A-Z].*)</p>")
        self.Answer_mode=re.compile("<p>(答案：.*)</p>")
        self.span_mode=re.compile("<span.*>(.*)</span>")
        self.title_mode=re.compile("<p>(.*)</p>")
        self.templist=[]
        self.Qset=[]

    def nospan(self,str):
        if("span"not in str):
            try:
                return re.findall(self.opt_mode,str)[0]
            except IndexError:
                return str
        else:
            return re.findall(self.span_mode,str)[0]

    def getQA_fromHtml(self):
        htmlfile=requests.get(self.url,headers=self.header)
        html=etree.HTML(htmlfile.text)
        part=html.xpath('//section[@label="edit by 135editor"]//section[@data-role="paragraph"]')
        section=etree.tostring(part[0],encoding="utf-8",pretty_print=True,method="html").decode("utf-8")
        content=str(section)
        content=re.sub("<span.*?>","",content)
        content=re.sub("<section.*?>","",content)
        content=re.sub("</section>","",content)
        content=re.sub("</span>","",content).replace("\xa0","").split("\n")
        
        for i in range(0,len(content)):
            answer=re.findall(self.Answer_mode,content[i])
            if (len(answer)>0):
                self.templist.append(self.nospan(answer[0]))
                if('\u4e00'<=answer[0][3]<='\u9fff'):
                    self.templist.append(self.nospan(re.findall(self.title_mode,content[i-2])[0]))
                else:
                    j=i-2
                    while(1):
                        try:
                            opt=self.nospan(content[j])
                            self.templist.append(opt)
                            if(opt[0]=="A"):
                                j=j-2
                                self.templist.append(self.nospan(re.findall(self.title_mode,content[j])[0]))
                                break;
                            j-=1
                        except IndexError:
                            j-=1
                            continue
                self.Qset.append(self.templist)
                self.templist=[]
        print(self.Qset)

  
a=select_QA_byURL("https://mp.weixin.qq.com/s?__biz=Mzg3ODI1MTU2Mg==&mid=2247774811&idx=1&sn=c88bbc8eb765406bb9428cf4234acf03&chksm=cf18691ef86fe0089e5bc6dafc1ea5cb7b89038a13a60c065bc60bb0c1051000fd3a27cbe90e&scene=178&cur_album_id=1681667206486523905#rd")

a.getQA_fromHtml()

