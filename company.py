class Company:
    def __init__(self, CBB_current, CBB_previous, Noncurrent_BB_current, Noncurrent_BB_previous,
                 PL_Before_Tax_current, PL_Before_Tax_previous, Revenue_current, Revenue_previous,
                 TA_current, TA_previous, current_BB_current, current_BB_previous, name,
                 ):
        
        self.CBB_current = CBB_current
        self.CBB_previous = CBB_previous
        self.Noncurrent_BB_current = Noncurrent_BB_current
        self.Noncurrent_BB_previous = Noncurrent_BB_previous
        self.PL_Before_Tax_current = PL_Before_Tax_current
        self.PL_Before_Tax_previous = PL_Before_Tax_previous
        self.Revenue_current = Revenue_current
        self.Revenue_previous = Revenue_previous
        self.TA_current = TA_current
        self.TA_previous = TA_previous
        self.current_BB_current = current_BB_current
        self.current_BB_previous = current_BB_previous
        self.name = name

        # Calculated attribute
        self.total_BB_current = self.Noncurrent_BB_current + self.current_BB_current
        self.total_BB_previous = self.Noncurrent_BB_previous + self.Noncurrent_BB_previous
        self.debt_percentage_current = (self.total_BB_current / self.TA_current) * 100
        self.debt_percentage_previous = (self.total_BB_previous / self.TA_previous) * 100
        self.cash_percentage_current = (self.CBB_current / self.TA_current) * 100
        self.cash_percentage_previous = (self.CBB_previous/ self.TA_previous) * 100
        self.activity_percentage_current = (self.Revenue_current / self.TA_current) * 100
        self.activity_percentage_previous = (self.Revenue_previous / self.TA_previous) * 100