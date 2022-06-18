import { useEffect, useState } from "react"
import { Nav } from "../Nav/Nav"
import { Cost } from "./Cost"

import './CostsPage.css'
import costsIcon from '../../costs.svg';

const getFormattedCosts = (costs) => {
    let dateCosts = {};

    costs.forEach((cost) => {
        if (dateCosts[cost.date] === undefined) {
            dateCosts[cost.date] = {
                costs: [cost],
                sum: cost.amount
            }
        } else {
            dateCosts[cost.date].costs.push(cost)
            dateCosts[cost.date].sum += cost.amount
        }
    })

    const sortedCosts = _sortFormattedCosts(dateCosts)

    return sortedCosts
}

const _sortFormattedCosts = (fmtCosts) => {
    const sortingFunction = (date1, date2) => Date.parse(date2) - Date.parse(date1)

    const sortedCosts = Object.keys(fmtCosts).sort(sortingFunction).reduce(
        (obj, key) => {
            obj[key] = fmtCosts[key]
            return obj
        }, {}
    )

    return sortedCosts
}

const getJsxDatedCosts = (costs, user) => {
    const jsxDatedCosts = []

    for (let date in costs) {
        const jsxCosts = getJsxCosts(costs[date].costs, user)
        const formattedDate = new Date(date).toDateString();

        jsxDatedCosts.push(
            <div key={date} className="costsDateContainer">
                <div className="costsDateContainerHeader">
                    <div className="costsDate">{formattedDate}</div>
                    <div className="costsDateSum">{costs[date].sum}{user.currency}</div>
                </div>

                <div className="costsDateList">{jsxCosts}</div>
            </div>
        )
    }

    return jsxDatedCosts
}

const getJsxCosts = (costs, user) => {
    const jsxCostsList = []


    costs.forEach((cost) => {
        jsxCostsList.push(<Cost key={cost.id} cost={cost} user={user} />)
    })

    return jsxCostsList
}

export const CostsPage = ({ user, costs }) => {
    const [jsxCosts, setJsxCosts] = useState([])

    useEffect(() => {
        const fmtCosts = getFormattedCosts(costs)
        const jsxDatedCosts = getJsxDatedCosts(fmtCosts, user)
        setJsxCosts(jsxDatedCosts)
    }, [user, costs])

    if (costs.length === 0)
        return (
            <>
                <div className="emptyPage">
                    <img src={costsIcon} />
                    <h2>There are no costs for this month</h2>
                </div>
                <Nav />
            </>
        )

    return (
        <>
            <div className="costsContainer">{jsxCosts}</div>
            <Nav />
        </>
    )
}