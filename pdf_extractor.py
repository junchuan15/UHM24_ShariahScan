import pdfplumber
import re

def pagelocate(pdf_path, pattern):
    found_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if re.search(pattern, text, re.IGNORECASE):
                found_pages.append(i + 1) 
    return found_pages

def extract_text_from_pdf_with_tolerance(pdf_path, page_number):
    text_lines = []
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number]
        texts = page.extract_text(x_tolerance=2, y_tolerance=2)
        lines = texts.split('\n')
        for line in lines:
            if line.strip():  
                text_lines.append(line.strip())
    return text_lines

def extract_last_values(row):
    if row:
        last_third_value = None
        last_fourth_value = None
        if len(row) >= 3:
            try:
                last_third_value = int(row[-3].replace(',', ''))
            except (ValueError, TypeError):
                pass
        if len(row) >= 4:
            try:
                last_fourth_value = int(row[-4].replace(',', ''))
            except (ValueError, TypeError):
                pass
        return last_third_value, last_fourth_value
    else:
        return None, None

def checking(rows, row_type):
    for row in rows:
        last_third_value, last_fourth_value = extract_last_values(row)
        if isinstance(last_third_value, int):
            print(f"Last third value from {row_type} row:", last_third_value)
        if isinstance(last_fourth_value, int):
            print(f"Last fourth value from {row_type} row:", last_fourth_value)

def extract_and_print_values_from_pdf(pdf_path, pattern):
    found_pages = pagelocate(pdf_path, pattern)
    extracted_lines = []
    for page_number in found_pages:
        extracted_lines.extend(extract_text_from_pdf_with_tolerance(pdf_path, page_number - 1))

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

    checking(cash_bank_balances_rows, "Cash and bank balances")
    checking(total_assets_rows, "Total assets")
    checking(bank_borrowing_rows, "Bank borrowing")

pdf_path = r".\Dataset\MCOM 2022 Audit Report.pdf"
pattern = r"STATEMENT OF FINANCIAL POSITION"
extract_and_print_values_from_pdf(pdf_path, pattern)
