from argparse import ArgumentParser

from category_classifier import CategoryClassifier
from report_parser import ReportParser


def main(args):
    rp = ReportParser(args.report_path)
    payment_records = rp.parse()

    cc = CategoryClassifier(payment_records)
    classified_data = cc.classify()
    # TODO generate_csv(args.output)


if __name__ == '__main__':
    parser = ArgumentParser(description="Bank reports analyzer")
    parser.add_argument("report_path")
    parser.add_argument("-o", "--out", dest="output", help="output CSV file")
    args = parser.parse_args()
    main(args)
