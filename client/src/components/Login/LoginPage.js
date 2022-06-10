import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';

const loginUser = async (email, password) => {
    const response = await fetch("http://192.168.0.156:8000/api/v1/auth/login/", {
        method: "POST",
        body: JSON.stringify({email, password}),
        headers: {'Content-Type': 'application/json'}
    });

    if (response.status > 299) return null;

    const tokenJson = await response.json();
    return tokenJson;
}

export const LoginPage = ({ token, setToken }) => {
    const [emailValue, setEmailValue] = useState("");
    const [passwordValue, setPasswordValue] = useState("");
    const [emailFieldStyle, setEmailFieldStyle] = useState({});
    const [passwordFieldStyle, setPasswordFieldStyle] = useState({});
    const [ErrorMessageStyle, setErrorMessageStyle] = useState({});

    const navigate = useNavigate();

    useEffect(() => {
        if (token) navigate("/", { replace: true });
    });

    const handleSubmit = (element) => {
        element.preventDefault();

        loginUser(emailValue, passwordValue).then(({ token, exptime }) => {
            if (!token) {
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
            <form onSubmit={handleSubmit} className="authForm">
                <h2>Authentication</h2>
                <div className="errorMessage" style={ErrorMessageStyle}>Error with sending request</div>
                <div className="authFormField">
                    <label>email</label>
                    <input onChange={emailChange} style={emailFieldStyle} type="email" />
                </div>
                <div className="authFormField">
                    <label>password</label>
                    <input onChange={passwordChange} style={passwordFieldStyle} type="password" />
                </div>
                <button type="submit">Log In</button>
            </form>
        </main>
    );
}
