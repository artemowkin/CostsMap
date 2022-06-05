import { useNavigate } from "react-router-dom";

export const useAuth = () => {
    let tokenValue = localStorage.getItem("tokenValue");
    const tokenExpDate = localStorage.getItem("tokenExpDate");

    tokenValue = (Date.now() / 1000 >= tokenExpDate) ? "" : tokenValue;

    return { tokenValue, tokenExpDate };
}

export const loginRequired = (token, navigate) => {
    if (!token) navigate("/login", { replace: true });
}