import { roundDecimal } from "../../utils/numbers"

export const TotalCosts = ({ user, monthCosts }) => {
    const roundedMonthCosts = roundDecimal(monthCosts)
    return (
        <div className="totalCosts">Month costs: <span>{roundedMonthCosts}{user.currency}</span></div>
    )
}