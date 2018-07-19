import re
import settings
from PyPDF2 import PdfFileReader


class ReportAnalyzer:
    def __init__(self, pdf_file):
        self.file_path = pdf_file
        self.txt = ""

    def analyze(self):
        self._read_text()
        self._trunc_excessive_data()
        self._search_for_payment_records()

    def _read_text(self):
        txt = ""
        pdf_reader = PdfFileReader(self.file_path)
        for page_nmb in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_nmb)
            txt += page.extractText()
        self.txt = txt

    def _trunc_excessive_data(self):
        # Truncate the first page info
        start_of_trans_table = self.txt.find(settings.START_TRANSFERS_TABLE_PATTERN)
        self.txt = self.txt[start_of_trans_table+len(settings.START_TRANSFERS_TABLE_PATTERN):]

    def _search_for_payment_records(self):
        date_regex = r'(20\d\d\.\d\d\.\d\d)'
        price_regex = r'(-?\d+\,\d\d)([0-9€,]*)'  # this price has scientific notation (eg. 23.234e23) so truncate the end
        transaction_name_regex = r'(.*?)'
        payment_info_suffix = r'Data transakcji:'

        row_regex = re.compile(f"{date_regex}{date_regex}TRANSAKCJA KART¥ DEBETOW¥{price_regex}{transaction_name_regex}{payment_info_suffix}")

        found_records = row_regex.findall(self.txt)  # TODO transform it into dictionary. Dictionary save into self.data

        # map tuple into dictionary
        res = map(lambda x: {"posting_date": x[0], "payment_date": x[1], "price": float(x[2].replace(',', '.')),
                             "payment_name": x[4]}, found_records)
        self.data = list(res)
        return res

    def generate_csv(self, output):
        pass  # TODO
