import axios from "axios"
import { useEffect, useState } from "react"

const getTotalCosts = async (token) => {
    try {
        const response = await axios({
            url: "/costs/total/",
            headers: {"Authorization": `Bearer ${token}`}
        })

        return response.data
    } catch (error) {
        return {total_costs: 0}
    }
}

export const TotalCosts = ({ token, user }) => {
    const [totalCosts, setTotalCosts] = useState(0);

    useEffect(() => {
        getTotalCosts(token).then((response) => setTotalCosts(response.total_costs))
    }, [])

    return (
        <div className="totalCosts">Month costs: <span>{totalCosts}{user.currency}</span></div>
    )
}