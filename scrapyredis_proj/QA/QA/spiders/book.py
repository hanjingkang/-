import scrapy
from QA.items import QaItem
 
#  ---1.导入分布式爬虫类
from scrapy_redis.spiders import RedisSpider
 
 
#  ---2.继承分布式爬虫类
class BookSpider(RedisSpider):
    name = 'book'
    # ---3.注销start_url&allow_domains
    # #  修改允许的域,如果爬取的网站中途还有别的域名，需要在这儿添加
    # allowed_domains = ['youlu.net']
    # #  修改起始url
    # start_urls = ['https://www.youlu.net/classify/']
 
 
    #  ---4.设置redis-key
    redis_key = 'myspider'  # 这儿是自己定义的，需要在redis数据库中写数据
 
    #  ---5.设置__init__
    def __init__(self, *args,  **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(BookSpider, self).__init__(*args, **kwargs)
 
    def parse(self, response):
        #  获取所有图书大分类的节点列表
        big_node_list = response.xpath('//*[@id="classifyDefaultRight"]/div[4]/ul/li/div[1]/a')
 
        # print(len(big_node_list))
        for big_node in big_node_list[:1]:
            big_category = big_node.xpath('./text()').extract_first()
            big_category_link = response.urljoin(big_node.xpath('./@href').extract_first())
            # print(big_category)
            # print(big_category_link)
 
            #  获取所有图书的小分类节点列表
            small_node_list = big_node.xpath('..//following-sibling::div[1]/a')
            # print(len(small_node_list))
            for small_node in small_node_list[:3]:
                temp = {}
                temp['big_category'] = big_category
                temp['big_category_link'] = big_category_link
                temp['small_category'] = small_node.xpath('./text()').extract_first()
                temp['small_category_link'] = response.urljoin(small_node.xpath('./@href').extract_first())
 
                print(temp)
                #  模拟点击小分类链接
                yield scrapy.Request(
                    url=temp['small_category_link'],
                    callback=self.parse_book_list,
                    meta={"big": temp}
                )
 
    def parse_book_list(self, response):
        temp = response.meta['big']
 
        book_list = response.xpath('//*[@id="classifyDefaultRight"]/div[5]/ul/li/div[2]/div')
 
        for book in book_list:
            item = QaItem()
 
            item['big_category'] = temp['big_category']
            item['big_category_link'] = temp['big_category_link']
            item['small_category'] = temp['small_category']
            item['small_category_link'] = temp['small_category_link']
 
            item['book_name'] = book.xpath('../div[1]/a/text()').extract_first()
            item['book_price'] = book.xpath('../div[4]/span[2]/text()').extract_first()
            item['book_author'] = book.xpath('../div[2]/text()').extract_first().strip()
            print(item)
            yield item