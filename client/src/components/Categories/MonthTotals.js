import { roundDecimal } from "../../utils/numbers"

export const MonthTotals = ({ user, monthCosts, monthIncomes }) => {
    const roundedMonthCosts = roundDecimal(monthCosts)
    const roundedMonthIncomes = roundDecimal(monthIncomes)

    return (
        <div className="monthTotals">
            <div className="totalCosts">Month costs: <span>{roundedMonthCosts}{user.currency}</span></div>
            <div className="totalIncomes">Month incomes: <span>{roundedMonthIncomes}{user.currency}</span></div>
        </div>
    )
}