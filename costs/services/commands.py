from services.commands import GetStatisticBaseCommand


class GetCostsStatisticCommand(GetStatisticBaseCommand):
    """Command to return costs statistic"""

    def get_dict_statistic(self):
        """Return costs statistic in dict format"""
        return {
            'costs': self.month_costs,
            'date': self.context_date,
            'total_sum': self.total_costs,
            'profit': self.profit,
            'average_costs': self.average_costs,
        }
