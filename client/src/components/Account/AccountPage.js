import { Nav } from "../Nav/Nav"

import './AccountPage.css'

export const AccountPage = ({ token, user }) => {
    const changeTheme = () => {
        const currentTheme = document.documentElement.className ?? "white"
        const changingTheme = (currentTheme === "dark") ? "white" : "dark"

        localStorage.setItem("color-theme", changingTheme)
        document.documentElement.className = changingTheme
    }

    const setSystemTheme = () => {
        const isSystemDark = window.matchMedia('(prefers-color-scheme: dark)').matches

        localStorage.removeItem("color-theme")
        document.documentElement.className = isSystemDark ? "dark" : "white"
    }

    const setWhiteTheme = () => {
        localStorage.setItem("color-theme", "white")
        document.documentElement.className = "white"
    }

    const setDarkTheme = () => {
        localStorage.setItem("color-theme", "dark")
        document.documentElement.className = "dark"
    }

    return (
        <>
            <div className="accountPage">
                <p className="themeChoicer">
                    <div className="themeButtons bg-white dark:bg-background-black">
                        <button onClick={setSystemTheme} className="themeButton"></button>
                        <button onClick={setWhiteTheme} className="themeButton"></button>
                        <button onClick={setDarkTheme} className="themeButton"></button>
                    </div>
                </p>
            </div>
            <Nav />
        </>
    )
}