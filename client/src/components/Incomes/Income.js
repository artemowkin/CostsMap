import { Link } from "react-router-dom"

export const Income = ({ income, currency }) => {
    const incomeCardImageStyle = {backgroundColor: income.card.color}
    const incomeUrl = `/incomes`

    return (
        <Link to={incomeUrl} className="incomeCard bg-white dark:bg-foreground-black">
            <div className="incomeCardInfo">
                <div className="incomeCardImage" style={incomeCardImageStyle} />
                <div className="incomeCardText">
                    <div className="costCategoryTitle">{income.card.title}</div>
                </div>
            </div>
            <div className="incomeCardAmount">{income.user_currency_amount}{currency}</div>
        </Link>
    )
}