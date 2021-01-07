from services.commands import GetStatisticBaseCommand


class GetIncomesStatisticCommand(GetStatisticBaseCommand):
    """Command to return incomes statistic"""

    def get_dict_statistic(self):
        """Return incomes statistic in dict format"""
        return {
            'incomes': self.month_incomes,
            'costs': self.month_costs,
            'date': self.context_date,
            'total_sum': self.total_incomes,
            'profit': self.profit,
            'average_costs': self.average_costs,
        }
