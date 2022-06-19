import axios from "axios";

export const getUserCategories = async (token) => {
    const response = await axios({
        url: "/categories/",
        method: "GET",
        headers: {"Authorization": `Bearer ${token}`}
    });
    return response.data;
}

export const getTotalCosts = async (token) => {
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

export const getTotalIncomes = async (token) => {
    try {
        const response = await axios({
            url: "/incomes/total/",
            headers: {"Authorization": `Bearer ${token}`}
        })

        return response.data
    } catch (error) {
        return {total_incomes: 0}
    }
}
