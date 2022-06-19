import { useEffect, useState } from "react"
import { Nav } from "../Nav/Nav"
import { Income } from "./Income"

import './IncomePage.css'
import costsIcon from '../../costs.svg';
import { roundDecimal } from "../../utils/numbers";
import { CostsIncomesNav } from "../CostIncomesNav/CostsIncomesNav";

const getFormattedIncomes = (incomes) => {
    let dateIncomes = {};

    incomes.forEach((income) => {
        if (dateIncomes[income.date] === undefined) {
            dateIncomes[income.date] = {
                incomes: [income],
                sum: income.user_currency_amount
            }
        } else {
            dateIncomes[income.date].incomes.push(income)
            dateIncomes[income.date].sum += income.user_currency_amount
        }
    })

    const sortedIncomes = _sortFormattedIncomes(dateIncomes)

    return sortedIncomes
}

const _sortFormattedIncomes = (fmtIncomes) => {
    const sortingFunction = (date1, date2) => Date.parse(date2) - Date.parse(date1)

    const sortedIncomes = Object.keys(fmtIncomes).sort(sortingFunction).reduce(
        (obj, key) => {
            obj[key] = fmtIncomes[key]
            return obj
        }, {}
    )

    return sortedIncomes
}

const getJsxDatedIncomes = (incomes, currency) => {
    const jsxDatedIncomes = []

    for (let date in incomes) {
        const jsxIncomes = getJsxIncomes(incomes[date].incomes, currency)
        const formattedDate = new Date(date).toDateString();
        const roundedIncomesDateSum = roundDecimal(incomes[date].sum)

        jsxDatedIncomes.push(
            <div key={date} className="incomesDateContainer">
                <div className="incomesDateContainerHeader">
                    <div className="incomesDate">{formattedDate}</div>
                    <div className="incomesDateSum">{roundedIncomesDateSum}{currency}</div>
                </div>

                <div className="incomesDateList">{jsxIncomes}</div>
            </div>
        )
    }

    return jsxDatedIncomes
}

const getJsxIncomes = (incomes, currency) => {
    const jsxIncomesList = []

    incomes?.forEach((income) => {
        jsxIncomesList.push(<Income key={income.id} income={income} currency={currency} />)
    })

    return jsxIncomesList
}

export const IncomesPage = ({ incomes, user }) => {
    const [jsxIncomes, setJsxIncomes] = useState([])

    useEffect(() => {
        const fmtIncomes = getFormattedIncomes(incomes)
        const jsxDatedIncomes = getJsxDatedIncomes(fmtIncomes, user.currency)
        setJsxIncomes(jsxDatedIncomes)
    }, [incomes])

    if (incomes.length === 0)
        return (
            <>
                <div className="emptyPage">
                    <img src={costsIcon} />
                    <h2>There are no incomes for this month</h2>
                </div>
                <Nav />
            </>
        )

    return (
        <>
            <div className="incomesContainer">{jsxIncomes}</div>
            <CostsIncomesNav current="incomes" />
            <Nav />
        </>
    )
}