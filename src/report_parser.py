import re
import settings
from PyPDF2 import PdfFileReader


class ReportParser:
    def __init__(self, pdf_file):
        self.file_path = pdf_file
        self.records_count = 0
        self.txt = ""

    def parse(self):
        self._read_text()
        self._trunc_excessive_data()
        return self._search_for_payment_records()

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
        date_regex = r'20\d\d\.\d\d\.\d\d'
        price_regex = r'(-?\d+\,\d\d)(\d\d€\d\d\d,\d\d)?'  # this price has scientific notation (eg. 23.234e23)
        transaction_name_regex = r'(.*?)'
        payment_info_suffix = f'(Kwota.?i.?waluta.?oryginalna.?transakcji|(?={date_regex}))'
        # TODO regex finish row on the date of next row.
        row_regex = re.compile(f"({date_regex})({date_regex})(TRANSAKCJA KART¥ DEBETOW¥|"
                               f"P£ACÊ Z T-MOBILE US£UGI BANKOWE|PRZELEW KRAJOWY|DO£ADOWANIE TELEFONU|"
                               f"PRZELEW W RAMACH BANKU NA RACH OBCY|PRZELEW P2P)"
                               f"{price_regex}{transaction_name_regex}{payment_info_suffix}")

        found_records = row_regex.findall(self.txt)

        self.records_count = len(found_records)
        # map tuple into dictionary
        res = map(lambda x: {"posting_date": x[0], "payment_date": x[1], "payment_type": x[2],
                             "price": float(x[3].replace(',', '.')),
                             "payment_name": x[5]}, found_records)
        return res
