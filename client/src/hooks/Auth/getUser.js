export const getUser = async (token) => {
    if (!token) return null;

    const response = await fetch("http://192.168.0.156:8000/api/v1/auth/me/", {
        headers: {"Authorization": `Bearer ${token}`}
    })

    if (response.status > 299) return null;

    const user = await response.json();

    return user
}