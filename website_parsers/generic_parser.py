import requests
import pandas as pd

from drone_parts import details_info


class MarketplaceParser:
    def __init__(self, url, detail_paths, detail_url_finder, attribute_parsers, normalizers):
        self.url = url
        self.detail_paths = detail_paths
        self.detail_url_finder = detail_url_finder
        self.attribute_parsers = attribute_parsers
        self.normalizers = normalizers

    @staticmethod
    def __get_page__(url):
        headers = {"User-Agent": "Mozilla/5.0"}
        return requests.get(url, headers=headers)

    def __get_detail_url_lists__(self):
        details_sell_pages = {}
        for detail, path in self.detail_paths.items():
            pages = []
            for page_num in range(1, 10):
                page_url = self.url + path + "?page=%d" % page_num
                print(page_url)
                page = self.__get_page__(page_url)
                if len(pages) > 0 and page.text == pages[-1].text or not page.status_code == 200:
                    break
                pages.append(page)
            details_sell_pages[detail] = pages

        detail_url_lists = {}
        for detail, sell_pages in details_sell_pages.items():
            detail_urls = []
            for sell_page in sell_pages:
                detail_urls.extend(self.detail_url_finder(sell_page))
            detail_url_lists[detail] = detail_urls

        return detail_url_lists

    def __get_detail_characteristics__(self, detail, detail_url):
        detail_page = self.__get_page__(detail_url)
        if not detail_page.status_code == 200:
            return None

        detail_chars = {}
        for attribute in details_info.details_list[detail]:
            attr_parser = self.attribute_parsers[detail][attribute]
            detail_chars[attribute] = attr_parser(detail_page)
        return detail_chars

    def parse(self):
        detail_url_lists = self.__get_detail_url_lists__()

        result = {}
        for detail, attr_list in details_info.details_list.items():
            details = pd.DataFrame(columns=attr_list)

            for detail_url in detail_url_lists[detail]:
                print("Looking up %s" % detail_url)
                detail_chars = self.__get_detail_characteristics__(detail, detail_url)
                if not detail_chars:
                    continue
                details.loc[len(details)] = detail_chars

            result[detail] = self.normalizers[detail](details)

        return result