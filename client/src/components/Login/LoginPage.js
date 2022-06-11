import axios from 'axios';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';

const loginUser = async (email, password) => {
    try {
        const response = await axios({
            url: "/auth/login/",
            method: "POST",
            data: {email, password},
            headers: {'Content-Type': 'application/json'}
        });

        return { status: response.status, ...response.data }
    } catch (error) {
        return { status: error.response.status, token: null, exptime: null }
    }
}

export const LoginPage = ({ token, setToken }) => {
    const [emailValue, setEmailValue] = useState("");
    const [passwordValue, setPasswordValue] = useState("");
    const [emailFieldStyle, setEmailFieldStyle] = useState({});
    const [passwordFieldStyle, setPasswordFieldStyle] = useState({});
    const [errorMessageStyle, setErrorMessageStyle] = useState({});
    const [errorMessageValue, setErrorMessageValue] = useState()

    const navigate = useNavigate();

    useEffect(() => {
        if (token) navigate("/", { replace: true });
    });

    const handleSubmit = (element) => {
        element.preventDefault();

        if (!passwordValue || !emailValue || emailFieldStyle.display) return

        loginUser(emailValue, passwordValue).then(({ status, token, exptime }) => {
            if (status >= 400 && status < 500) {
                setErrorMessageValue("Incorrect password or email")
                setErrorMessageStyle({display: "block"});
                return
            }

            if (!token) {
                setErrorMessageValue("Error with sending request")
                setErrorMessageStyle({display: "block"});
                return;
            }

            localStorage.setItem("tokenValue", token);
            localStorage.setItem("tokenExpDate", exptime);
            setToken(token);
            navigate("/", { replace: true });
        });
    };

    const emailChange = (element) => {
        setErrorMessageStyle({display: ""});
        let emailRegexp = /.+@.+\..+/;
        let emailValue = element.target.value;

        if (!emailValue.match(emailRegexp)) {
            setEmailFieldStyle({color: "#ff0000"});
        } else {
            setEmailFieldStyle({});
        }

        setEmailValue(emailValue);
    }

    const passwordChange = (element) => {
        setErrorMessageStyle({display: ""});
        setPasswordValue(element.target.value);
    }

    return (
        <main className="authentication">
            <form onSubmit={handleSubmit} className="authForm bg-white dark:bg-foreground-black">
                <h2>Authentication</h2>
                <div className="errorMessage" style={errorMessageStyle}>{errorMessageValue}</div>
                <div className="authFormField">
                    <label className="bg-white dark:bg-foreground-black">email</label>
                    <input className="bg-white dark:bg-foreground-black" onChange={emailChange} style={emailFieldStyle} type="email" placeholder='example@mail.com' />
                </div>
                <div className="authFormField">
                    <label className="bg-white dark:bg-foreground-black">password</label>
                    <input className="bg-white dark:bg-foreground-black" onChange={passwordChange} style={passwordFieldStyle} type="password" placeholder='password' />
                </div>
                <button type="submit">Log In</button>
            </form>
        </main>
    );
}
