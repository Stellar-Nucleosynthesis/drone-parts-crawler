import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DistributorsParser:
    def __init__(self, search_detail, find_product_name, find_sale_info, min_similarity=0.9):
        self.search_detail = search_detail
        self.find_product_name = find_product_name
        self.find_sale_info = find_sale_info
        self.min_similarity = min_similarity

    @staticmethod
    def __find_similarity(text1, text2):
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])
        return similarity[0][0]

    def parse(self, details_dataset):
        headers = {"User-Agent": "Mozilla/5.0"}
        details_sales = dict()

        for detail, df in details_dataset.items():
            for index, row in df.iterrows():
                model = row['model']
                urls_list = self.search_detail(row['model'])
                print("URL LIST:", urls_list, "MODEL:", model)
                model_sale_info = pd.DataFrame(columns=[
                    "distributor_name",
                    "distributor_link",
                    "price",
                    "is_available",
                ])
                for url in urls_list:
                    page = requests.get(url, headers=headers)
                    product_name = self.find_product_name(page)
                    similarity = self.__find_similarity(model, product_name)
                    if similarity >= self.min_similarity:
                        (store_name, price, is_available) = self.find_sale_info(page)
                        model_sale_info.loc[len(model_sale_info)] = \
                            [store_name, url, price, is_available]

                if not model_sale_info.empty:
                    details_sales[model] = model_sale_info

        return details_sales