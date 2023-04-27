from pathlib import Path
from bs4 import BeautifulSoup

import scrapy


class WikiYearSpider(scrapy.Spider):
    name = "wikiyear" # name of the spider

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/1881',
            #'https://quotes.toscrape.com/page/1/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        f = open("demofile2.txt", "a")
        
        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.find('div', {'class': 'mw-parser-output'})

        birth_started = False
        for tag in content.findChildren(recursive=False):
            f.write(tag.name)
            if tag.name == "h2" and "Births" in tag.text:
                birth_started = True
            if tag.name == "h2" and "Deaths" in tag.text:
                birth_started = False
            if birth_started == True and tag.name == "ul":
                li_children = tag.findChildren("li" , recursive=False)
                for li_child in li_children:
                    if len(li_child.findChildren("ul", recursive=False)) == 0:
                        a_children = li_child.findChildren("a" , recursive=False)
                        date = a_children[0].text if (len(a_children) > 0) else ''
                        name = a_children[1].text if (len(a_children) > 1) else ''
                        death = a_children[len(a_children)-1].text if (len(a_children) > 2) else ''
                        description = li_child.text

                        yield {
                            'date': date,
                            'name': name,
                            'death': death,
                            'description': description
                        }
                    else:
                        a_children = li_child.findChildren("a" , recursive=False)
                        date = a_children[0].text if (len(a_children) > 0) else ''
                        li_subchildren = li_child.findChildren("li")
                        for li_subchild in li_subchildren:
                            a_subchildren = li_subchild.findChildren("a", recursive=False)
                            name = a_subchildren[0].text if (len(a_subchildren) > 0) else ''
                            death = a_subchildren[len(a_subchildren)-1].text if (len(a_subchildren) > 1) else ''
                            description = li_subchild.text
                            yield {
                                'date': date,
                                'name': name,
                                'death': death,
                                'description': description
                            }
        
        f.close()
