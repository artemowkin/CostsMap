import { useEffect, useState } from "react"
import { Nav } from "../Nav/Nav"
import { Cost } from "./Cost"

import './CostsPage.css'

const getCosts = async (token) => {
    const response = await fetch("http://192.168.0.156:8000/api/v1/costs/", {
        headers: {"Authorization": `Bearer ${token}`}
    })

    if (response.status > 299) return []

    const responseJson = await response.json()

    return responseJson
}

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

    return dateCosts
}

const getJsxDatedCosts = (costs, user) => {
    const jsxDatedCosts = []

    for (let date in costs) {
        const jsxCosts = getJsxCosts(costs[date].costs, user)
        const formattedDate = new Date(date).toDateString();

        jsxDatedCosts.push(
            <div className="costsDateContainer">
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
        jsxCostsList.push(<Cost cost={cost} user={user} />)
    })

    return jsxCostsList
}

export const CostsPage = ({ token, user }) => {
    const [formattedCosts, setFormattedCosts] = useState([])
    const [jsxCosts, setJsxCosts] = useState([])

    useEffect(() => {
        getCosts(token).then((costs) => {
            const fmtCosts = getFormattedCosts(costs)
            setFormattedCosts(fmtCosts)
        })
    }, [user])

    useEffect(() => {
        const jsxDatedCosts = getJsxDatedCosts(formattedCosts, user)
        setJsxCosts(jsxDatedCosts)
    }, [formattedCosts])

    return (
        <>
            <div className="costsContainer">{jsxCosts}</div>
            <Nav />
        </>
    )
}