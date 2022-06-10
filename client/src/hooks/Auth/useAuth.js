export const useAuth = () => {
    let tokenValue = localStorage.getItem("tokenValue", null);
    const tokenExpDate = localStorage.getItem("tokenExpDate", null);

    tokenValue = (tokenExpDate !== null && Date.now() / 1000 >= tokenExpDate) ? "" : tokenValue;

    return { tokenValue, tokenExpDate };
}
