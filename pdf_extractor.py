import pdfplumber
import re
import firebase_admin
from firebase_admin import db, credentials
from firebase_admin import firestore
import traceback

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

        # authenticate to firebase
        cred = credentials.Certificate("firebase.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

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
            lines = texts.split("\n")
            for line in lines:
                if line.strip():
                    text_lines.append(line.strip())
        return text_lines
    
    def extract_last_values(self, row, registration_number, row_type):
        last_third_value = None
        last_fourth_value = None

        if row:
            if len(row) >= 3 and isinstance(row[-3], str): 
                try:
                    last_third_value_str = row[-3].replace(",", "").strip()
                    if last_third_value_str.startswith("(") and last_third_value_str.endswith(")"):
                        last_third_value_str = "-" + last_third_value_str[1:-1]
                    last_third_value = int(last_third_value_str)
                    third_field_name = f"{row_type}_previous"
                    doc_ref = self.db.collection("Company").document(registration_number)
                    doc_ref.update({third_field_name: last_third_value})
                except (ValueError, TypeError):
                    pass
            if len(row) >= 4 and isinstance(row[-4], str): 
                try:
                    last_fourth_value_str = row[-4].replace(",", "").strip()
                    if last_fourth_value_str.startswith("(") and last_fourth_value_str.endswith(")"):
                        last_fourth_value_str = "-" + last_fourth_value_str[1:-1]
                    last_fourth_value = int(last_fourth_value_str)
                    fourth_field_name = f"{row_type}_current"
                    doc_ref = self.db.collection("Company").document(registration_number)
                    doc_ref.update({fourth_field_name: last_fourth_value})
                except (ValueError, TypeError):
                    pass
        return last_third_value, last_fourth_value

                
    def extract_fp_data(self, pattern, registration_number):
        found_pages = self.pagelocate(pattern)
        extracted_lines = []
        for page_number in found_pages:
            extracted_lines.extend(
                self.extract_text_from_pdf_with_tolerance(page_number - 1)
            )

        split_lines = [line.split() for line in extracted_lines]

        cash_bank_balances_pattern = re.compile(
            r"Cash\s+and\s+bank\s+balances", re.IGNORECASE
        )
        total_assets_pattern = re.compile(r"Total\s+assets", re.IGNORECASE)
        bank_borrowing_pattern = re.compile(r"Bank\s+borrowing", re.IGNORECASE)
        cash_bank_balances_rows = []
        total_assets_rows = []
        bank_borrowing_rows = []

        for line in split_lines:
            line_text = " ".join(line)
            if cash_bank_balances_pattern.search(line_text):
                cash_bank_balances_rows.append(line)
            elif total_assets_pattern.search(line_text):
                total_assets_rows.append(line)
            elif bank_borrowing_pattern.search(line_text):
                bank_borrowing_rows.append(line)

    
        current_bank_borrowing_rows = bank_borrowing_rows[1:] 
        non_current_bank_borrowing_rows = bank_borrowing_rows[:1] 

        for row in cash_bank_balances_rows:
            last_third_value, last_fourth_value = self.extract_last_values(row, registration_number, "CBB")

        for row in total_assets_rows:
            last_third_value, last_fourth_value = self.extract_last_values(row, registration_number, "TA")
            
        for row in non_current_bank_borrowing_rows:
            last_third_value, last_fourth_value = self.extract_last_values(row, registration_number, "Noncurrent_BB")
        
        for row in current_bank_borrowing_rows:
            last_third_value, last_fourth_value = self.extract_last_values(row, registration_number, "current_BB")

    def extract_pol_data(self, pattern, registration_number):
        found_pages = self.pagelocate(pattern)
        if not found_pages:
            return

        revenue_pattern = re.compile(r'Revenue', re.IGNORECASE)
        income_pattern = re.compile(r'(?:Interest|Financial)\s+(Income)', re.IGNORECASE)
        beforetax_pattern = re.compile(r'(?:Profit|Loss|\(loss\))\s*(?:Before\s+Tax|before\staxation)?', re.IGNORECASE)

        for page_number in found_pages:
            extracted_lines = self.extract_text_from_pdf_with_tolerance(page_number - 1)
            split_lines = [line.split() for line in extracted_lines]

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

            for row in revenue_rows:
                self.extract_last_values(row, registration_number, "Revenue")

            for row in income_rows:
                self.extract_last_values(row, registration_number, "II")

            for row in beforetax_rows:
                self.extract_last_values(row, registration_number, "PL_Before_Tax")

    def extract_name_and_registration(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            first_page = pdf.pages[0]
            first_two_lines = first_page.extract_text().strip().split("\n")[:2]
            name = first_two_lines[0]
            registration_number = re.search(r"\d{12}\s*\([^)]+\)", first_two_lines[1]).group()
            announcement_date = None
            date_pattern = r"\b(?:0?[1-9]|[12]\d|3[01])\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b"
            page_num = self.pagelocate('Chartered Accountants')
            if page_num:
                for num in page_num:
                    if num <= len(pdf.pages):
                        page = pdf.pages[num - 1]
                        text = page.extract_text()
                        date_matches = re.findall(date_pattern, text, re.IGNORECASE)
                        if date_matches:
                            announcement_date = date_matches[-1]

            financial_ended_date = None
            date_pattern = r"\b(?:0?[1-9]|[12]\d|3[01])\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b"
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            date_match = re.search(date_pattern, text, re.IGNORECASE)
            if date_match:
                financial_ended_date = date_match.group(0)

            doc_ref = self.db.collection("Company").document(registration_number)
            doc_ref.set({
                "name": name,
                "Announcement_Date": announcement_date,
                "FE_Date": financial_ended_date
            })

        return registration_number, name

    def extract_data_from_pdf(self):
        registration_number, company_name = self.extract_name_and_registration()
        pattern_fp = r"STATEMENT OF FINANCIAL POSITION"
        pattern_pol = r"STATEMENT OF PROFIT OR LOSS | COMPREHENSIVE INCOME"
        self.extract_fp_data(pattern_fp, registration_number)
        self.extract_pol_data(pattern_pol, registration_number)
        return company_name
    
    
pdf_extractor = PDFExtractor(r".\Dataset\MCOM 2022 Audit Report.pdf")
name = pdf_extractor.extract_data_from_pdf()
