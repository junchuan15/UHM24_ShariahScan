from database import Database

class Calculation:
    def __init__(self):
        self.db = Database()

    def calculate_cash_percentage(self, cash, total_assets):
        if total_assets == 0:
            return "Error: Total assets cannot be zero."
        cash_percentage = (cash / total_assets) * 100
        return cash_percentage

    def calculate_debt_percentage(self, debt, total_assets):
        if total_assets == 0:
            return "Error: Total assets cannot be zero."
        debt_percentage = (debt / total_assets) * 100
        return debt_percentage

    def calculate_non_compliant_percentage(self, non_compliant_revenue, non_compliant_profit, total_revenue, total_profit):
        non_compliant_revenue_percentage = (non_compliant_revenue / total_revenue) * 100
        non_compliant_profit_percentage = (non_compliant_profit / total_profit) * 100
        return non_compliant_revenue_percentage, non_compliant_profit_percentage

    def retrieve_new_company_data(self, company_name):
        company = self.db.retrieve_company_data(company_name)
        company.total_BB_current = company.Noncurrent_BB_current + company.current_BB_current
        company.total_BB_previous = company.Noncurrent_BB_previous + company.current_BB_previous
        company.debt_percentage_current = self.calculate_debt_percentage(company.total_BB_current, company.TA_current)
        company.debt_percentage_previous = self.calculate_debt_percentage(company.total_BB_previous, company.TA_previous)
        company.cash_percentage_current = self.calculate_cash_percentage(company.CBB_current, company.TA_current)
        company.cash_percentage_previous = self.calculate_cash_percentage(company.CBB_previous, company.TA_previous)
        company.activity_percentage_current = self.calculate_cash_percentage(company.Revenue_current, company.TA_current)
        company.activity_percentage_previous = self.calculate_cash_percentage(company.Revenue_previous, company.TA_previous)

        return company

calculator = Calculation()
company_name = "MCOM HOLDINGS BERHAD"
company_data = calculator.retrieve_new_company_data(company_name)
print("Cash Percentage (Current): {:.2f}%".format(company_data.cash_percentage_current))
print("Debt Percentage (Current): {:.2f}%".format(company_data.debt_percentage_current))
