import re

import yaml


class CategoryClassifier:
    def __init__(self, data):
        self.classified_data = None
        self.data = data
        self.categories = yaml.load(open("categories.yml"))

    def classify(self, case_sensitive=False):
        res = []
        for record in self.data:
            category_matches = set()  # eg. transport, food
            elem_name_matches = set()  # eg. uber, carrefour etc.

            for category in self.categories:
                for elem_name in self.categories[category]:
                    # move out re.search arguments outside call to make code logic for case sensitivity problem
                    args = [elem_name, ''.join([record['payment_type'], record['payment_name']])]
                    if not case_sensitive:
                        args.append(re.IGNORECASE)

                    if re.search(*args):
                        elem_name_matches.add(elem_name)
                        category_matches.add(category)

            record['categories'] = category_matches
            record['categories_found_elements'] = elem_name_matches
            res.append(record)
        self.classified_data = res
        return res

    def get_result(self):
        return self.classified_data
