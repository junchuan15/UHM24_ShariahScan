import pdfplumber
import re
import firebase_admin
from firebase_admin import db, credentials
from firebase_admin import firestore
from database import Database

class PDFExtractor:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.db = Database()

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
            texts = page.extract_text(x_tolerance=5, y_tolerance=2)
            lines = texts.split("\n")
            for line in lines:
                if line.strip():
                    text_lines.append(line.strip())
        return text_lines 
    
<<<<<<< HEAD
    def extract_last_values(self, row, registration_number, row_type, multiply_by_1000=False):
=======
    def extract_last_values(self, row, registration_number, row_type, pattern):
>>>>>>> f1abfc879bec5ac6452fa430298cc4e8b5d716ab
        last_third_value = None
        last_fourth_value = None

        if row:
            if len(row) >= 3 and isinstance(row[-3], str): 
                try:
                    last_third_value_str = row[-3].replace(",", "").strip()
                    if last_third_value_str.startswith("(") and last_third_value_str.endswith(")"):
                        last_third_value_str = "-" + last_third_value_str[1:-1]
                    last_third_value = int(last_third_value_str)
                    if self.check_money(pattern): 
                        last_third_value *= 1000
                    third_field_name = f"{row_type}_previous"
                    doc_ref = self.db.db.collection("Company").document(registration_number)
                    doc_ref.update({third_field_name: last_third_value})
                    print("Row from which value is extracted:", row) 
                except (ValueError, TypeError):
                    pass
            if len(row) >= 4 and isinstance(row[-4], str): 
                try:
                    last_fourth_value_str = row[-4].replace(",", "").strip()
                    if last_fourth_value_str.startswith("(") and last_fourth_value_str.endswith(")"):
                        last_fourth_value_str = "-" + last_fourth_value_str[1:-1]
                    last_fourth_value = int(last_fourth_value_str)
                    if self.check_money(pattern): 
                        last_fourth_value *= 1000
                    fourth_field_name = f"{row_type}_current"
                    doc_ref = self.db.db.collection("Company").document(registration_number)
                    doc_ref.update({fourth_field_name: last_fourth_value})
                except (ValueError, TypeError):
                    pass
        return last_third_value, last_fourth_value


<<<<<<< HEAD

    def print_extracted_values(self, field_name, value):
        print(f"Extracted {field_name}: {value}")
=======
>>>>>>> f1abfc879bec5ac6452fa430298cc4e8b5d716ab
                
    def extract_fp_data(self, pattern, registration_number):
        found_pages = self.pagelocate(pattern)
        extracted_lines = []
        for page_number in found_pages:
            extracted_lines.extend(
                self.extract_text_from_pdf_with_tolerance(page_number - 1)
            )

        split_lines = [line.split() for line in extracted_lines]

        cash_bank_balances_pattern = re.compile(r"Cash\s+and\s+bank\s+balances", re.IGNORECASE)
        total_assets_pattern = re.compile(r"Total\s+assets", re.IGNORECASE)
        bank_borrowing_pattern = re.compile(r"(?:Bank\s)?borrowings?\b", re.IGNORECASE)
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
<<<<<<< HEAD
            last_third_value, last_fourth_value = self.extract_last_values(row, registration_number, "CBB", multiply_by_1000=True)

        for row in total_assets_rows:
            last_third_value, last_fourth_value = self.extract_last_values(row, registration_number, "TA", multiply_by_1000=True)

        for row in non_current_bank_borrowing_rows:
            last_third_value, last_fourth_value = self.extract_last_values(row, registration_number, "Noncurrent_BB", multiply_by_1000=True)

        for row in current_bank_borrowing_rows:
            last_third_value, last_fourth_value = self.extract_last_values(row, registration_number, "current_BB", multiply_by_1000=True)

=======
            last_third_value, last_fourth_value = self.extract_last_values(row, registration_number, "CBB", pattern)
            print(last_third_value)
            print(last_fourth_value)

        for row in total_assets_rows:
            last_third_value, last_fourth_value = self.extract_last_values(row, registration_number, "TA", pattern)
            print(last_third_value)
            print(last_fourth_value)
            
        for row in non_current_bank_borrowing_rows:
            last_third_value, last_fourth_value = self.extract_last_values(row, registration_number, "Noncurrent_BB", pattern)
            print(last_third_value)
            print(last_fourth_value)
        
        for row in current_bank_borrowing_rows:
            last_third_value, last_fourth_value = self.extract_last_values(row, registration_number, "current_BB", pattern)
            print(last_third_value)
            print(last_fourth_value)
>>>>>>> f1abfc879bec5ac6452fa430298cc4e8b5d716ab

    def extract_pol_data(self, pattern, registration_number):
        found_pages = self.pagelocate(pattern)
        if not found_pages:
            return

        revenue_pattern = re.compile(r'Revenue', re.IGNORECASE)
        income_pattern = re.compile(r'(?:Interest|Financial)\s+(Income)', re.IGNORECASE)
        beforetax_pattern = re.compile(r'(?:Profit|Loss|\b\w+\b)\s+(?:Before Tax) |Profit/(loss) before taxation', re.IGNORECASE)
        
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
                self.extract_last_values(row, registration_number, "Revenue", pattern)

            for row in income_rows:
                self.extract_last_values(row, registration_number, "II", pattern)

            for row in beforetax_rows:
<<<<<<< HEAD
                self.extract_last_values(row, registration_number, "PL_Before_Tax")

    '''def extract_compliant_data(self, pattern, registration_number):
            found_pages = self.pagelocate(pattern)
            if not found_pages:
                return

            category_data = {}  # Dictionary to accumulate data for each category

            for category, keywords in categories.items():
                category_field_name = re.sub(r'\W+', '_', category)  # Sanitize category name
                category_pattern = re.compile(fr"\b({'|'.join(keywords)})\b", re.IGNORECASE)

                for page_number in found_pages:
                    extracted_lines = self.extract_text_from_pdf_with_tolerance(page_number - 1)
                    split_lines = [line.split() for line in extracted_lines]

                    category_rows = []

                    for line in split_lines:
                        line_text = ' '.join(line)
                        if category_pattern.search(line_text):
                            category_rows.append(line)

                    for row in category_rows:
                        print(f"Category: {category}, Row: {row}")  # Check if it's extracting correct rows
                        last_third_value, last_fourth_value = self.extract_last_values(row, registration_number, f"non_syariah_{category_field_name}")
                        # Accumulate data for each category
                        category_data.setdefault(category, []).append((last_third_value, last_fourth_value))
=======
                self.extract_last_values(row, registration_number, "PL_Before_Tax", pattern)
>>>>>>> f1abfc879bec5ac6452fa430298cc4e8b5d716ab

            # Update the Firestore database after accumulating data for all categories
            for category, data_list in category_data.items():
                current_values = [data[1] for data in data_list]
                previous_values = [data[0] for data in data_list]
                sanitized_field_name = re.sub(r'\W+', '_', category)
                doc_ref = self.db.collection("Company").document(registration_number)
                doc_ref.update({
                    f"non_syariah_{sanitized_field_name}_current": current_values,
                    f"non_syariah_{sanitized_field_name}_previous": previous_values
                })
    '''

    def extract_name_and_registration(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            first_page = pdf.pages[0]
            first_two_lines = first_page.extract_text().strip().split("\n")[:2]
            name = None
            registration_number = None

            for line in first_two_lines:
                if "Registration" in line or "Company" in line:
                    registration_number = line.strip()
                else:
                    name = line.strip()

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
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            date_match = re.search(date_pattern, text, re.IGNORECASE)
            if date_match:
                financial_ended_date = date_match.group(0)

            # Create document with registration number and company details
            doc_ref = self.db.db.collection("Company").document(registration_number)
            doc_ref.set({
                "name": name,
                "Announcement_Date": announcement_date,
                "FE_Date": financial_ended_date
            })

        return registration_number, name

    def check_money(self, pattern):
        found_pages = self.pagelocate(pattern)
        extracted_lines = []
        for page_number in found_pages:
            extracted_lines.extend(
                self.extract_text_from_pdf_with_tolerance(page_number - 1)
            )

        split_lines = [line.split() for line in extracted_lines]

        RM_pattern = re.compile(r"RM’000", re.IGNORECASE)
        for line in split_lines:
            line_text = " ".join(line)
            if RM_pattern.search(line_text):
                return True
        return False


    def extract_data_from_pdf(self):
        registration_number, company_name = self.extract_name_and_registration()
        pattern_fp = r"STATEMENTS?\S* OF FINANCIAL POSITION"
        pattern_pol = r"STATEMENT?\S* OF PROFIT OR LOSS"
        self.extract_fp_data(pattern_fp, registration_number)
        self.extract_pol_data(pattern_pol, registration_number)
        return company_name
    
PDFExtractor = PDFExtractor(r"C:\UM\Y2S2\2024Competition\Um  Hack\ShariahScan\5_Kumpulan Europlus Berhad-AFS 2015.pdf")
company_name = PDFExtractor.extract_data_from_pdf()