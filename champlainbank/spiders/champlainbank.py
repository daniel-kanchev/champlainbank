import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from champlainbank.items import Article


class ChamplainbankSpider(scrapy.Spider):
    name = 'champlainbank'
    start_urls = ['https://www.champlainbank.com/news.htm']

    def parse(self, response):
        articles = response.xpath('//div[@class="news-container"]/div')
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = article.xpath('./h2/text()').get()
            if title:
                title = title.strip()
            date = article.xpath('./p[1]//text()').get()

            content = article.xpath('.//text()').getall()
            content = [text for text in content if text.strip()]
            content = "\n".join(content[2:]).strip()

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()



