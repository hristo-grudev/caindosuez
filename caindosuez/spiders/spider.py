import scrapy

from scrapy.loader import ItemLoader
from ..items import CaindosuezItem
from itemloaders.processors import TakeFirst


class CaindosuezSpider(scrapy.Spider):
	name = 'caindosuez'
	start_urls = ['https://luxembourg.ca-indosuez.com/a-la-une/actualites']

	def parse(self, response):
		post_links = response.xpath('//a[@class="block-article--link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="block-articleTitle--title mb-30"]/h3/text()').get()
		description = response.xpath('//div[@class="block-wysiwg-text"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="block-articleTitle--author mb-30"]/p/text()').get()

		item = ItemLoader(item=CaindosuezItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
