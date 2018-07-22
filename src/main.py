from argparse import ArgumentParser
from category_classifier import CategoryClassifier
from report_parser import ReportParser
from stats_generator import StatsGenerator


def main(args):
    rp = ReportParser(args.report_path)
    raw_payment_records = rp.parse()

    if args.verbose:
        print("Read {} records.".format(len(list(raw_payment_records))))

    cc = CategoryClassifier(raw_payment_records)
    classified_data = cc.classify()

    sg = StatsGenerator(classified_data)
    stats_csv = sg.generate_csv()

    if args.output:
        with open(args.output, "w") as f_write_csv:
            f_write_csv.write(stats_csv)
            f_write_csv.close()
            print(f"CSV file {args.output} is generated.")
    else:
        print(stats_csv)


if __name__ == '__main__':
    parser = ArgumentParser(description="Bank reports analyzer")
    parser.add_argument("report_path")
    parser.add_argument("-o", "--out", dest="output", help="output CSV file")
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    main(args)
