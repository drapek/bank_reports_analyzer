from argparse import ArgumentParser
from reportanalyzer import ReportAnalyzer


def main(args):
    print(args.report_path, args.output)
    rep_anal = ReportAnalyzer(args.report_path)
    rep_anal.analyze()
    rep_anal.generate_csv(args.output)


if __name__ == '__main__':
    parser = ArgumentParser(description="Bank reports analyzer")
    parser.add_argument("report_path")
    parser.add_argument("-o", "--out", dest="output", help="output CSV file")
    args = parser.parse_args()
    main(args)
