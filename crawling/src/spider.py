from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess
import os

PAGES_COUNT = 100

save_dir_ru = 'crawling/result/ru'
index_file = 'crawling/result/index.txt'

restricted_domains = ['t.me', 'telegram.org', 'instagram.com', 'vk.com', 'm.vk.com', 'ok.ru', 'youtube.com', 'www.youtube.com',
                      'www.tiktok.com', 'viber.com', 'music.apple.com', 'rutube.ru', 'www.linkedin.com',
                      'linkedin.com', 'apps.apple.com', 'www.apple.com', 'github.com', 'account.ncbi.nlm.nih.gov',
                      'kudago.com', 'www.zoom.com', 'swiftwithmajid.com', 'danielsaidi.com', 'www.kodeco.com',
                      'help.kodeco.com', 'holyswift.app', 'account.habr.com', 'support.google.com', 'www.avanderlee.com',
                      'developer.apple.com', 'fakestoreapi.com', 'en.wikipedia.org', 'devstreaming-cdn.apple.com',
                      'apptractor.ru', 'connect.ok.ru', 'nodejs.org', 'page.hyoo.ru', 'idea.hyoo.ru', 'developer.mozilla.org',
                      'ftdichip.com', 'www.donnywals.com', 'telegram.me', 'sso.passport.yandex.ru', 'passport.yandex.ru',
                      'tenor.com', 'transparencyreport.google.com', 'techcrunch.com', 'de.wikipedia.org', 'no.wikipedia.org',
                      'fa.wikipedia.org', 'it.wikipedia.org', 'oc.wikipedia']
restricted_urls = ['https://zen.yandex.ru/tolkosprosit']
restricted_paths = ['about', 'register', 'login', 'agreement', 'docs']
start_urls = [
    'https://habr.com/ru/articles/797735/',
    'https://habr.com/ru/companies/productivity_inside/articles/797733/',
    'https://habr.com/ru/companies/nfckey/articles/797683/',
    'https://habr.com/ru/news/797589/',
    'https://habr.com/ru/news/797505/',
    'https://habr.com/ru/articles/797381/',
]

class PagesSpider(scrapy.Spider):
    name = "pages"
    start_urls = start_urls
    page_counter = 1

    @classmethod
    def increment_counters(cls):
        cls.page_counter += 1

    def counters_reached(self):
        return self.page_counter >= PAGES_COUNT

    def total_pages(self):
        return self.page_counter
    
    def page_allowed(self, next_page):
        try:
            url_domain = next_page.split('/')[2]
            url_path = next_page.split('/')[3]
            if next_page in restricted_urls or url_domain in restricted_domains or url_path in restricted_paths:
                return False
            else:
                return True
        except:
            return True

    def parse(self, response): 
        url_domain = response.url.split('/')[2]
        url_path = response.url.split('/')[3]
        if response.url in restricted_urls or url_domain in restricted_domains or url_path in restricted_paths:
            self.log(f'{response.url} blocked by list during parsing')
        else:
            lang_attribute = response.xpath('//html/@lang').get()
            language = lang_attribute.strip()

            if not language.startswith('ru'): return
            
            filename = f'{self.page_counter}-{response.url.split("/")[-2]}.html'
            filepath = os.path.join(save_dir_ru, filename)

            with open(filepath, 'wb') as f:
                f.write(response.body)
            with open(index_file, 'a') as f:
                f.write(f'{response.url},ru,{filename},{filepath}\n')

            self.increment_counters()

            if self.counters_reached():
                raise scrapy.exceptions.CloseSpider(
                    f'{self.page_counter}')

            next_pages = set(response.css('a::attr(href)').getall() + response.xpath("//a/@href").getall())
            for next_page in next_pages:
                if (next_page is not None) and (self.page_allowed(next_page)):
                    yield response.follow(next_page, callback=self.parse)


def create_directories():
    if not os.path.exists(save_dir_ru):
        os.makedirs(save_dir_ru)


if __name__ == "__main__":
    create_directories()

    process = CrawlerProcess()
    process.crawl(PagesSpider)
    process.start()
