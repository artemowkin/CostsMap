import { Link } from "react-router-dom"

import './CostsIncomesNav.css'

export const CostsIncomesNav = ({ current }) => {
    if (current === "costs")
        return (
            <div className="costsIncomesNavContainer">
                <div className="costsIncomesNavButtons bg-white dark:bg-background-black">
                    <div className="costsIncomesNavButton costsIncomesNavButtonCosts">Costs</div>
                    <Link to="/incomes" className="costsIncomesNavButton">Incomes</Link>
                </div>
            </div>
        )

    return (
        <div className="costsIncomesNavContainer">
            <div className="costsIncomesNavButtons bg-white dark:bg-background-black">
                <Link to="/costs" className="costsIncomesNavButton">Costs</Link>
                <div className="costsIncomesNavButton costsIncomesNavButtonIncomes">Incomes</div>
            </div>
        </div>
    )
}