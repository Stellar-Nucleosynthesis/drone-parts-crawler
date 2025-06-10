import re
import pandas as pd
import requests

class DistributorsParser:
    def __init__(self, search_detail, find_product_name, find_sale_info, min_similarity=0.7, max_processed_results=10):
        self.search_detail = search_detail
        self.find_product_name = find_product_name
        self.find_sale_info = find_sale_info
        self.min_similarity = min_similarity
        self.max_processed_results = max_processed_results

    @staticmethod
    def __without_cyrillic_words(text):
        return ' '.join([word for word in text.split() if not re.search(r'[а-яА-ЯіїєґІЇЄҐ]', word)])

    @staticmethod
    def __extract_words(text):
        words = text.lower().split()
        with_digits = [w for w in words if re.search(r'\d', w)]
        without_digits = [w for w in words if not re.search(r'\d', w)]
        return set(with_digits), set(without_digits)

    @staticmethod
    def __jaccard_similarity(set1, set2):
        if not set1 and not set2:
            return 1.0
        intersection = set1 & set2
        union = set1 | set2
        return len(intersection) / len(union)

    @staticmethod
    def __find_similarity(text1, text2, weight_digits=0.7, weight_words=0.3):
        if not text1 and not text2:
            return 1.0
        if not text1 or not text2:
            return 0.0

        t1 = DistributorsParser.__without_cyrillic_words(text1)
        t2 = DistributorsParser.__without_cyrillic_words(text2)

        digits1, words1 = DistributorsParser.__extract_words(t1)
        digits2, words2 = DistributorsParser.__extract_words(t2)

        sim_digits = DistributorsParser.__jaccard_similarity(digits1, digits2)
        sim_words = DistributorsParser.__jaccard_similarity(words1, words2)

        final_score = weight_digits * sim_digits + weight_words * sim_words
        print("Similarity between %s and %s: %s" % (text1, text2, round(final_score, 4)))
        return round(final_score, 4)

    def parse(self, details_dataset):
        headers = {"User-Agent": "Mozilla/5.0"}
        details_sales = dict()

        for detail, df in details_dataset.items():
            for index, row in df.iterrows():
                model = row['model']
                urls_list = self.search_detail(model)
                print("URL LIST:", urls_list, "MODEL:", model)
                model_sale_info = pd.DataFrame(columns=[
                    "distributor_name",
                    "distributor_link",
                    "price",
                    "is_available",
                ])
                for url in urls_list[:self.max_processed_results]:
                    page = requests.get(url, headers=headers)
                    product_name = self.find_product_name(page)
                    similarity = self.__find_similarity(model, product_name)
                    if similarity >= self.min_similarity:
                        print("Found the detail %s on page %s" % (model, url))
                        (store_name, price, is_available) = self.find_sale_info(page)
                        model_sale_info.loc[len(model_sale_info)] = \
                            [store_name, url, price, is_available]

                if not model_sale_info.empty:
                    details_sales[model] = model_sale_info

        return details_sales