import pdfplumber
import re
import firebase_admin
from firebase_admin import db, credentials
from firebase_admin import firestore

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def store_data_in_firestore(self, registration_number, name, data):
        doc_ref = self.db.collection('Company').document(registration_number)
        doc_ref.set({
            'name': name,
            'data': data
        })
        
    # authenticate to firebase
    cred = credentials.Certificate("firebase.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    def pagelocate(self, pattern):
        found_pages = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if re.search(pattern, text, re.IGNORECASE):
                    found_pages.append(i + 1)
        return found_pages

    def extract_text_from_pdf_with_tolerance(self, page_number):
        text_lines = []
        with pdfplumber.open(self.pdf_path) as pdf:
            page = pdf.pages[page_number]
            texts = page.extract_text(x_tolerance=2, y_tolerance=2)
            lines = texts.split('\n')
            for line in lines:
                if line.strip():
                    text_lines.append(line.strip())
        return text_lines

    def extract_last_values(self, row):
     if row:
        last_third_value = None
        last_fourth_value = None
        if len(row) >= 3 and isinstance(row[-3], str):  # Check if it's a string
            try:
                last_third_value_str = row[-3].replace(',', '').strip()
                if last_third_value_str.startswith('(') and last_third_value_str.endswith(')'):
                    last_third_value_str = '-' + last_third_value_str[1:-1]
                last_third_value = int(last_third_value_str)
            except (ValueError, TypeError):
                pass
        if len(row) >= 4 and isinstance(row[-4], str):  # Check if it's a string
            try:
                last_fourth_value_str = row[-4].replace(',', '').strip()
                if last_fourth_value_str.startswith('(') and last_fourth_value_str.endswith(')'):
                    last_fourth_value_str = '-' + last_fourth_value_str[1:-1]
                last_fourth_value = int(last_fourth_value_str)
            except (ValueError, TypeError):
                pass
        return last_third_value, last_fourth_value
     else:
        return None, None

    def print_values(self, rows, row_type):
        for row in rows:
            last_third_value, last_fourth_value = self.extract_last_values(row)
            if isinstance(last_third_value, int):
                print(f"Last third value from {row_type} row:", last_third_value)
            if isinstance(last_fourth_value, int):
                print(f"Last fourth value from {row_type} row:", last_fourth_value)

    def extract_fp_data(self, pattern):
        found_pages = self.pagelocate(pattern)
        extracted_lines = []
        for page_number in found_pages:
            extracted_lines.extend(self.extract_text_from_pdf_with_tolerance(page_number - 1))

        split_lines = [line.split() for line in extracted_lines]

        cash_bank_balances_pattern = re.compile(r'Cash\s+and\s+bank\s+balances', re.IGNORECASE)
        total_assets_pattern = re.compile(r'Total\s+assets', re.IGNORECASE)
        bank_borrowing_pattern = re.compile(r'Bank\s+borrowing', re.IGNORECASE)
        cash_bank_balances_rows = []
        total_assets_rows = []
        bank_borrowing_rows = []

        for line in split_lines:
            line_text = ' '.join(line)
            if cash_bank_balances_pattern.search(line_text):
                cash_bank_balances_rows.append(line)
            elif total_assets_pattern.search(line_text):
                total_assets_rows.append(line)
            elif bank_borrowing_pattern.search(line_text):
                bank_borrowing_rows.append(line)
                
        self.print_values(cash_bank_balances_rows, "Cash and bank balances")
        self.print_values(total_assets_rows, "Total assets")
        self.print_values(bank_borrowing_rows, "Bank borrowing")
        
        bank_borrowing_data = {
            'non_current': [],
            'current': []
        }
        
        for row in bank_borrowing_rows:
            last_third_value, last_fourth_value = self.extract_last_values(row)
            if last_third_value is not None and last_fourth_value is not None:
                bank_borrowing_data['non_current'].append(last_third_value)
                bank_borrowing_data['current'].append(last_fourth_value)
        
        return bank_borrowing_data

    def extract_pol_data(self, pattern):
        found_pages = self.pagelocate(pattern)
        extracted_lines = []
        for page_number in found_pages:
            extracted_lines.extend(self.extract_text_from_pdf_with_tolerance(page_number - 1))

        split_lines = [line.split() for line in extracted_lines]

        revenue_pattern = re.compile(r'Revenue', re.IGNORECASE)
        income_pattern = re.compile(r'(?:Interest|Financial)\s+(Income)', re.IGNORECASE)
        beforetax_pattern = re.compile(r'(?:Profit|Loss)\s+Before\s+Tax', re.IGNORECASE)
        revenue_rows = []
        income_rows = []
        beforetax_rows = []

        for line in split_lines:
            line_text = ' '.join(line)
            if revenue_pattern.search(line_text):
                revenue_rows.append(line)
            elif income_pattern.search(line_text):
                income_rows.append(line)
            elif beforetax_pattern.search(line_text):
                beforetax_rows.append(line)
                
        self.print_values(revenue_rows, "Revenue")
        self.print_values(income_rows, "Interest Income")
        self.print_values(beforetax_rows, "Profit/Loss Before Tax")
        
        revenue_data = self.extract_last_values(revenue_rows)
        income_data = self.extract_last_values(income_rows)
        beforetax_data = self.extract_last_values(beforetax_rows)
        
        return {
            'revenue_current': revenue_data[0],
            'revenue_previous': revenue_data[1],
            'income_current': income_data[0],
            'income_previous': income_data[1],
            'beforetax_current': beforetax_data[0],
            'beforetax_previous': beforetax_data[1],
        }

    def extract_name_and_registration(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            first_page = pdf.pages[0]
            first_two_lines = first_page.extract_text().strip().split('\n')[:2]
            name = first_two_lines[0]
            registration_number = re.search(r'\d{12}\s*\([^)]+\)', first_two_lines[1]).group()
            return name, registration_number

# Example usage
pdf_path = r".\Dataset\MCOM 2022 Audit Report.pdf"
pdf_extractor = PDFExtractor(pdf_path)
name, registration_number = pdf_extractor.extract_name_and_registration()
print("Name:", name)
print("Registration Number:", registration_number)

pattern_fp = r"STATEMENT OF FINANCIAL POSITION"
pattern_pol = r"STATEMENT OF PROFIT OR LOSS"
fp_data = pdf_extractor.extract_fp_data(pattern_fp)
pol_data = pdf_extractor.extract_pol_data(pattern_pol)

# Store extracted data in Firestore
pdf_extractor.store_data_in_firestore(registration_number, name, {'fp_data': fp_data, 'pol_data': pol_data})