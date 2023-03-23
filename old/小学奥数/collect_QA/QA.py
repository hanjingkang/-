from lxml import etree
import re


class select_QA():
    def __init__(self,html) -> None:
        self.html=etree.HTML(html)
        self.section=None
        self.text=None
        self.question_mode = re.compile("(【题目】  [1-6]年级)")
        self.last_loc = 0
        self.last_name = ''
        self.QA_dic = {}
        self.count = 1
        self.a_last_loc = 0
    
    def pre_process(self):
        self.section=self.html.xpth("//div[@id='js_content']//section[@data-source='bj.96weixin.com']")
        for i in range(0,len(self.section)):
            self.section[i]=etree.tostring(self.section[i],encoding="utf-8",pretty_print=True,method="html").decode('utf-8')
        self.text='\n'.join(self.section)
        self.text=re.sub("<section.*?>|<p.*?>|</section>|</p>|<strong.*?>|</strong>|<span.*?>|</span>|<br.*?>|</br>|<pre.*?>|</pre>|<h1.*?>|</h1>","",self.text)
        self.text=self.text.split("\n")
    def get_QA(self):
        for i in range(0, len(self.text)):
            try:
                q = re.findall(question_mode, self.text[i])[0].replace('【题目】  ', '')
                self.QA_dic[q] = []
                if(self.last_loc == 0):
                    self.last_loc=i
                    self.last_name=q
                    continue
                else:
                    question_content = ''.join(t[self.last_loc+1: i])
                    self.QA_dic[self.last_name].append(question_content.replace(" ", "").replace("\n",'').replace("\xa0","").replace("\u3000",""))
                    self.last_loc = i
                    self.last_name = q
            except IndexError:
                if('答案与解析' in t[i]):
                    if(self.a_last_loc != 0):
                        answer_content = ''.join(t[self.a_last_loc+1:i]).replace("\n",'').replace(" ","").replace("\xa0","").replace("\u3000","")
                        answer_content = re.sub("[1-6]年级", "", answer_content)
                        self.QA_dic[str(self.count)+"年级"].append(answer_content)
                        self.a_last_loc = i
                        self.count += 1
                    else:
                        question_content = ''.join(t[self.last_loc+1: i])
                        question_content = re.sub("[1-6]年级", "", question_content)
                        self.a_last_loc=i
                        self.QA_dic[self.last_name].append(question_content.replace(" ", "").replace("\n",'').replace("\xa0","").replace("\u3000",""))
                else:
                    continue

        answer_content = ''.join(t[self.a_last_loc+1:len(self.text)-1])
        self.QA_dic[str(self.count)+"年级"].append(answer_content.replace(" ", "").replace("\n",'').replace("\xa0","").replace("\u3000",""))





with open(r"C:/Users/Han JingKang/Desktop/分布式爬虫/小学奥数/temp/page.html", 'r', encoding="utf-8") as f:
    t = f.readlines()

#t =etree.HTML(t)
# t=t.xpath("//div[@id='js_content']//section[@data-source='bj.96weixin.com']")
""" t=t.xpath("//section[@data-source='bj.96weixin.com']")

for i in range(0,len(t)):
    t[i]=etree.tostring(t[i],encoding="utf-8",pretty_print=True,method="html").decode('utf-8')



with open(r"C:/Users/Han JingKang/Desktop/分布式爬虫/小学奥数/temp/page.html", 'w', encoding="utf-8") as f:
    f.write('\n'.join()) """


""" t=re.sub("<section.*?>","",t)
t=re.sub("<p.*?>","",t)
t=re.sub("</section>","",t)
t=re.sub("</p>","",t)
t=re.sub("<strong.*?>","",t)
t=re.sub("</strong>","",t)
t=re.sub("<span.*?>","",t)
t=re.sub("</span>","",t)
t=re.sub("<br.*?>","",t)
t=re.sub("</br>","",t)
t=re.sub("<pre.*?>","",t)
t=re.sub("</pre>","",t)
t=re.sub("<h1.*?>","",t)
t=re.sub("</h1>","",t)


with open(r"C:/Users/Han JingKang/Desktop/分布式爬虫/小学奥数/temp/page.html", 'w', encoding="utf-8") as f:
    f.write(t) """

question_mode = re.compile("(【题目】  [1-6]年级)")
last_loc = 0
last_name = ''
QA_dic = {}
count = 1
a_last_loc = 0


for i in range(0, len(t)):
    try:
        q = re.findall(question_mode, t[i])[0].replace('【题目】  ', '')
        QA_dic[q] = []
        if(last_loc == 0):
            last_loc=i
            last_name=q
            continue
        else:
            question_content = ''.join(t[last_loc+1: i])
            QA_dic[last_name].append(question_content.replace(" ", "").replace("\n",'').replace("\xa0","").replace("\u3000",""))
            last_loc = i
            last_name = q
    except IndexError:
        if('答案与解析' in t[i]):
            if(a_last_loc != 0):
                answer_content = ''.join(t[a_last_loc+1:i]).replace("\n",'').replace(" ","").replace("\xa0","").replace("\u3000","")
                answer_content = re.sub("[1-6]年级", "", answer_content)
                QA_dic[str(count)+"年级"].append(answer_content)
                a_last_loc = i
                count += 1
            else:
                question_content = ''.join(t[last_loc+1: i])
                question_content = re.sub("[1-6]年级", "", question_content)
                a_last_loc=i
                QA_dic[last_name].append(question_content.replace(" ", "").replace("\n",'').replace("\xa0","").replace("\u3000",""))
        else:
            continue

answer_content = ''.join(t[a_last_loc+1:len(t)-1])
QA_dic[str(count)+"年级"].append(answer_content.replace(" ", "").replace("\n",'').replace("\xa0","").replace("\u3000",""))

print(QA_dic)

