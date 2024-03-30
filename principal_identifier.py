import pdfplumber
import re

class PrincipalIdentifier:

    categories = {
    "Conventional Banking and Lending": ["Other income", "Deposits", "Interest income", "Interest expense", "Financial assets", "Financial liabilities", "Credit facilities"],
    "Conventional Insurance": ["Insurance premiums", "Policyholders", "Claims", "Underwriting", "Reinsurance", "Actuarial reserves"],
    "Gambling": ["Gaming revenue", "Betting", "Casino operations", "Lottery", "Gaming machines", "Wagering"],
    "Liquor and Liquor-Related Activities": ["Alcohol sales", "Beverage revenue", "Brewery operations", "Distillery", "Wine production", "Spirits"],
    "Pork and Pork-Related Activities": ["Pork products", "Pork sales", "Meat processing", "Pork supply chain", "Pork industry", "Swine farming"],
    "Non-Halal Food and Beverages": ["Non-halal products", "Food sales", "Beverage sales", "Food processing", "Food safety standards", "Halal certification"],
    "Tobacco and Tobacco-Related Activities": ["Tobacco sales", "Cigarette revenue", "Tobacco manufacturing", "Smoking products", "Tobacco industry", "Nicotine products"],
    "Interest Income from Conventional Accounts and Instruments": ["Interest earned", "Fixed deposits", "Savings accounts", "Interest receivable", "Interest-bearing assets", "Treasury bonds"],
    "Dividends from Shariah Non-Compliant Investments": ["Dividend income", "Equity investments", "Stock dividends", "Investment income", "Shareholder distributions", "Dividend yield"],
    "Shariah Non-Compliant Entertainment": ["Entertainment expenses", "Event hosting", "Entertainment venues", "Leisure activities", "Cultural events", "Entertainment industry"]
    }

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def pagelocate(self, pattern):
        found_pages = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if re.search(pattern, text, re.IGNORECASE):
                    found_pages.append(i)
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
    
    def extract_last_values(self, row):
        last_third_value = None
        last_fourth_value = None

        if row:
            if len(row) >= 3 and isinstance(row[-3], str): 
                try:
                    last_third_value_str = row[-3].replace(",", "").strip()
                    if last_third_value_str.startswith("(") and last_third_value_str.endswith(")"):
                        last_third_value_str = "-" + last_third_value_str[1:-1]
                    last_third_value = int(last_third_value_str)
                except (ValueError, TypeError):
                    pass
            if len(row) >= 4 and isinstance(row[-4], str): 
                try:
                    last_fourth_value_str = row[-4].replace(",", "").strip()
                    if last_fourth_value_str.startswith("(") and last_fourth_value_str.endswith(")"):
                        last_fourth_value_str = "-" + last_fourth_value_str[1:-1]
                    last_fourth_value = int(last_fourth_value_str)
                except (ValueError, TypeError):
                    pass
        return last_third_value, last_fourth_value


    def extract_pol_data(self, pattern, registration_number):
        found_pages = self.pagelocate(pattern)
        extracted_lines = []
        for page_number in found_pages:
            extracted_lines.extend(
                self.extract_text_from_pdf_with_tolerance(page_number - 1)
            )

        split_lines = [line.split() for line in extracted_lines]

        revenue_pattern = re.compile(r'Revenue', re.IGNORECASE)
        revenue_rows = []

        for line in split_lines:
            line_text = ' '.join(line)
            if revenue_pattern.search(line_text):
                revenue_rows.append(line)

        last_third_value, last_fourth_value = None, None
        for row in revenue_rows:
            last_third_value, last_fourth_value = self.extract_last_values(row)
            
       
        return last_third_value, last_fourth_value
       
    def extract_name_and_registration(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            first_page = pdf.pages[0]
            first_two_lines = first_page.extract_text().strip().split("\n")[:2]
            name = first_two_lines[0]
            registration_number = re.search(
                r"\d{12}\s*\([^)]+\)", first_two_lines[1]
            ).group()
            return registration_number

    def extract_values_from_categories(self, lines):
        category_values = {category: [] for category in self.categories}
        for line in lines:
            for category, keywords in self.categories.items():
                for keyword in keywords:
                    if keyword.lower() in line.lower():
                        category_values[category].append(line)
                        break
        return category_values

# Example usage
pdf_path = r".\Dataset\MCOM 2022 Audit Report.pdf"
pdf_extractor = PrincipalIdentifier(pdf_path)
registration_number = pdf_extractor.extract_name_and_registration()
pattern_pol = r"STATEMENT OF PROFIT OR LOSS"
pol_data = pdf_extractor.extract_pol_data(pattern_pol, registration_number)

# Extract all lines from the PDF
all_lines = pdf_extractor.extract_text_from_pdf_with_tolerance(0)

# Extract values from categories
category_values = pdf_extractor.extract_values_from_categories(all_lines)

# Display the results
print("Values in Categories:")
for category, values in category_values.items():
    print(f"Category: {category}")
    for value in values:
        print(f"  {value}")

print("Extracted POL Data:", pol_data)
