from pathlib import Path
from bs4 import BeautifulSoup

import re
import scrapy


class WikiCategorySpider(scrapy.Spider):
    name = "wikicategory" # name of the spider

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/Category:1532_births',
            #'https://quotes.toscrape.com/page/1/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pagination_links = response.css('div.mw-category-group ul li a')
        yield from  response.follow_all(pagination_links, self.parse_person)
    
    def parse_person(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        place = ''

        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.find('div', {'class': 'mw-parser-output'})
        content_table = content.findChildren("table", recursive=False)
        if len(content_table) > 0:
            content_trs = content_table[0].findChildren("tr" , recursive=True)
            print(len(content_trs))
            for content_tr in content_trs:
                content_th = content_tr.findChildren("th", recursive=False)
                if content_th[0].text == "Born":
                    content_td = content_tr.findChidren("td", recursive=False)
                    content_a = content_td[0].findChildren("a", recursive=False)
                    place = content_a.text
                    break

        
        lang_count_text = extract_with_css('label#p-lang-btn-label span.vector-menu-heading-label::text')
        lang_numbers = re.findall(r'\d+', lang_count_text)

        if len(lang_numbers) < 1 or int(lang_numbers[0]) < 10:
            return

        yield {
            'url': response.url,
            'lang_count': lang_numbers[0],
            'place': place,
        }


