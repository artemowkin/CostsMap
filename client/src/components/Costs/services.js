import axios from "axios"

export const getUserCosts = async (token) => {
    const response = await axios({
        url: "/costs/",
        headers: {"Authorization": `Bearer ${token}`}
    })

    return response.data
}