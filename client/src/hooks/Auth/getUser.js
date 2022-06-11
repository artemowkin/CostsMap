import axios from "axios";

export const getUser = async (token) => {
    if (!token) return null;

    const response = await axios({
        url: "/auth/me/",
        headers: {"Authorization": `Bearer ${token}`}
    })

    return response.data
}