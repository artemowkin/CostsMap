import { Nav } from "../Nav/Nav"

import './AccountPage.css'

import systemTheme from "./system-theme.svg"
import darkTheme from "./theme-dark.svg"
import lightTheme from "./theme-light.svg"

export const AccountPage = ({ token, user }) => {
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
                <div className="themeChoicer">
                    <div className="themeChoiceTitle">Theme:</div>
                    <div className="themeButtons bg-white dark:bg-background-black">
                        <button onClick={setSystemTheme} className="themeButton"><img src={systemTheme} /></button>
                        <button onClick={setWhiteTheme} className="themeButton"><img src={lightTheme} /></button>
                        <button onClick={setDarkTheme} className="themeButton"><img src={darkTheme} /></button>
                    </div>
                </div>
            </div>
            <Nav />
        </>
    )
}