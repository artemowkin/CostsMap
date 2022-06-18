import axios from "axios";

export const getUserCategories = async (token) => {
    const response = await axios({
        url: "/categories/",
        method: "GET",
        headers: {"Authorization": `Bearer ${token}`}
    });
    return response.data;
}