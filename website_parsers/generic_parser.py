import requests
import pandas as pd

from drone_parts import details_info


class MarketplaceParser:
    def __init__(self, url, detail_paths, product_url_parser, attribute_parsers):
        self.url = url
        self.detail_paths = detail_paths
        self.product_url_parser = product_url_parser
        self.attribute_parsers = attribute_parsers

    def __get_page__(self, url):
        headers = {"User-Agent": "Mozilla/5.0"}
        return requests.get(url, headers=headers)

    def __get_detail_url_lists__(self):
        details_sell_pages = {}
        for detail, path in self.detail_paths.items():
            pages = []
            for page_num in range(10):
                page_url = self.url + path + "?page=%d" % page_num
                print(page_url)
                page = self.__get_page__(page_url)
                if len(pages) > 0 and page.text == pages[-1].text or not page.status_code == 200:
                    break
                pages.append(page)
            details_sell_pages[detail] = pages

        detail_url_list = {}
        for detail, sell_pages in details_sell_pages.items():
            detail_urls = []
            for sell_page in sell_pages:
                detail_urls.extend(self.product_url_parser(sell_page))
            detail_url_list[detail] = detail_urls

        return detail_url_list

    def __get_detail_characteristics__(self, detail, detail_url):
        detail_page = self.__get_page__(detail_url)
        if not detail_page.status_code == 200:
            return None

        detail_chars = {}
        for attribute in details_info.details_list[detail]:
            attr_parser = self.attribute_parsers[attribute]
            value = attr_parser(detail_page)
            if not value:
                print("Couldn't find %s in " % attribute, detail_url)
                return None
            detail_chars[attribute] = value
        return detail_chars

    def parse(self):
        detail_url_lists = self.__get_detail_url_lists__()

        result = {}
        for detail, attr_list in details_info.details_list.items():
            details = pd.DataFrame(columns=attr_list)

            for detail_url in detail_url_lists[detail]:
                print("Looking up %s" % detail_url)
                detail_chars = self.__get_detail_characteristics__(detail, detail_url)
                if detail_chars == None:
                    continue
                details.loc[len(details)] = detail_chars
            result[detail] = details
        return result