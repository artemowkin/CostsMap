import axios from "axios"

export const getUserIncomes = async (token) => {
    const response = await axios({
        url: "/incomes/",
        headers: {"Authorization": `Bearer ${token}`}
    })

    return response.data
}