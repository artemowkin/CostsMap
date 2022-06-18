import axios from "axios";

export const getUserCards = async (token) => {
    const response = await axios({
        url: "/cards/",
        method: "GET",
        headers: {"Authorization": `Bearer ${token}`}
    });
    return response.data;
}