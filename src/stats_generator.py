import csv
import io

from functions import get_set_from_iter_by_attr


class StatsGenerator:
    def __init__(self, classified_data):
        self.classified_data = classified_data
        self.summary = None

    def generate_csv(self):
        if not self.summary:
            self.calculate_summary()

        output_csv = io.StringIO()
        writer = csv.writer(output_csv)

        for category in self.summary['categories']:
            writer.writerow([category['category_name'], ])

            for sub_category in category['sub_categories']:
                writer.writerow([None, sub_category['sub_category_name']])

                for transaction in sub_category['payment_rows']:
                    writer.writerow([None, None, transaction['payment_date'], transaction['posting_date'],
                                     transaction['payment_name'], transaction['price']])
                writer.writerow([None, f"summary {sub_category['sub_category_name']}",  sub_category['price_summary']])

            writer.writerow([None, f"summary {category['category_name']}", category['price_summary']])
        writer.writerow(["total summary:", self.summary['total_price']])

        res = output_csv.getvalue()
        output_csv.close()
        return res

    def calculate_summary(self):
        self.summary = {'categories': [], 'total_price': 0}
        main_categories = get_set_from_iter_by_attr(self.classified_data, 'categories')
        for main_category in main_categories:
            category_summary = {'category_name': main_category, 'sub_categories': [], 'price_summary': 0}
            pay_rows_by_main_cat = list(filter(lambda x: main_category in x['categories'], self.classified_data))
            sub_categories = get_set_from_iter_by_attr(pay_rows_by_main_cat, 'sub_categories')

            for sub_category in sub_categories:
                sub_category_summary = {'sub_category_name': sub_category, 'payment_rows': [], 'price_summary': 0}
                pay_rows_by_sub_cat = list(filter(lambda x: sub_category in x['sub_categories'], pay_rows_by_main_cat))
                summary_price = sum(row['price'] for row in pay_rows_by_sub_cat)

                sub_category_summary['price_summary'] = summary_price
                sub_category_summary['payment_rows'] = pay_rows_by_sub_cat

                category_summary['sub_categories'].append(sub_category_summary)
                category_summary['price_summary'] += summary_price
                self.summary['total_price'] += summary_price

            self.summary['categories'].append(category_summary)
        return self.summary
