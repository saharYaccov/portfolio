class Payment():
    def __init__(self, income, outcome):
        self.income = income
        self.outcome = outcome

    @property
    def income(self):
        return self._income

    @income.setter
    def income(self, value):
        '''
        Sets the income of the payment.
        '''
        self._income = value

    @property
    def outcome(self):
        return self._outcome

    @outcome.setter
    def outcome(self, value):
        '''
        Sets the outcome of the payment.
        '''
        self._outcome = value
########################################################################################################################################
    def create_pay_report(self):
        """
                Creates a payment report that includes income, outcome, net profit, and ROI.
                ROI (Return on Investment) is calculated as:
                    ROI = (Net Profit / Outcome) * 100
                """
        net_profit = self.income - self.outcome  # חישוב רווח נקי
        roi = (net_profit / self.outcome * 100) if self.outcome != 0 else 0  # חישוב החזר השקעה (ROI)

        # יצירת הדוח
        report = (
            f"--- Payment Report ---\n"
            f"Income: {self.income}\n"
            f"Outcome: {self.outcome}\n"
            f"Net Profit: {net_profit}\n"
            f"ROI: {roi:.2f}%\n"
        )
        return report
    ########################################################################################################################################
    def __str__(self):
        return f"Payment(income={self.income}, outcome={self.outcome})"
