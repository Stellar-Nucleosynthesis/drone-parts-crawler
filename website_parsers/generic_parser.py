import requests
import pandas as pd
from bs4 import BeautifulSoup

from drone_parts import details


class MarketplaceParser:
    def __init__(self, url, detail_paths, product_url_parser, attribute_parsers):
        self.url = url
        self.detail_paths = detail_paths
        self.product_url_parser = product_url_parser
        self.attribute_parsers = attribute_parsers

    def parse(self):
        headers = { "User-Agent": "Mozilla/5.0" }

        details_sell_pages = {}
        for detail, path in self.detail_paths.items():
            pages = []
            for page_num in range(10):
                page_url = self.url + path + "?page=%d" % page_num
                print(page_url)
                page = requests.get(page_url, headers=headers)
                if len(pages) > 0 and page.text == pages[-1].text or not page.status_code == 200:
                    break
                pages.append(page)
            details_sell_pages[detail] = pages

        result = {}
        for detail, sell_pages in details_sell_pages.items():
            details_list = pd.DataFrame(columns=details.details_list[detail])

            detail_urls = []
            for sell_page in sell_pages:
                detail_urls.extend(self.product_url_parser(sell_page))

            for detail_url in detail_urls:
                print("Looking up %s" % detail_url)
                detail_page = requests.get(detail_url, headers=headers)
                if not detail_page.status_code == 200:
                    break
                detail_info = {}
                for attribute in details.details_list[detail]:
                    attr_parser = self.attribute_parsers[attribute]
                    detail_attr = attr_parser(detail_page)
                    if not detail_attr:
                        print("Couldn't find %s" % attribute)
                        break
                    detail_info[attribute] = attr_parser(detail_page)
                if not len(detail_info) == len(details.details_list[detail]):
                    continue
                details_list.loc[len(details_list)] = detail_info
            result[detail] = details_list
        return result