
def calculate_cash_percentage(cash, total_assets):
    # Check if total_assets is zero to avoid division by zero error
    if total_assets == 0:
        return "Error: Total assets cannot be zero."

    # Calculate cash percentage
    cash_percentage = (cash / total_assets) * 100

    return cash_percentage


def calculate_debt_percentage(debt, total_assets):
    # Check if total_assets is zero to avoid division by zero error
    if total_assets == 0:
        return "Error: Total assets cannot be zero."

    # Calculate debt percentage
    debt_percentage = (debt / total_assets) * 100

    return debt_percentage


def calculate_non_compliant_percentage(non_compliant_revenue, non_compliant_profit, total_revenue, total_profit):
    # Calculate the percentage of revenue from non-compliant activities
    non_compliant_revenue_percentage = (non_compliant_revenue / total_revenue) * 100
    
    # Calculate the percentage of profit from non-compliant activities
    non_compliant_profit_percentage = (non_compliant_profit / total_profit) * 100
    
    return non_compliant_revenue_percentage, non_compliant_profit_percentage

