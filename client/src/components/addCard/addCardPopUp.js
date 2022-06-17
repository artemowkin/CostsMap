import axios from 'axios';
import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const getUserCurrencies = async (token) => {
    try {
        const response = await axios({
            url: "/auth/currencies/",
            method: "GET"
        })

        return response.data
    } catch (err) {
        return { currencies: [] }
    }
}

const createCard = async (payload, token) => {
    try {
        const response = await axios({
            url: "/cards/",
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            data: payload
        })

        return { status: response.status, card: response.data }
    } catch (error) {
        return { status: error.response.status, category: null }
    }
}

export const AddCardPopUp = ({ token, setCards, user }) => {
    const [userCurrenciesOptions, setUserCurrenciesOptions] = useState([])
    const [titleValue, setTitleValue] = useState("")
    const [titleStyle, setTitleStyle] = useState({})
    const [currencyValue, setCurrencyValue] = useState(user?.currency)
    const [colorValue, setColorValue] = useState("#ff0000")
    const [uniqueMessageStyle, setUniqueMessageStyle] = useState({})
    const [errorMessageStyle, setErrorMessageStyle] = useState({})

    const navigate = useNavigate();

    useEffect(() => {
        getUserCurrencies(token).then(({ currencies }) => {
            const currenciesOptions = currencies.map((currency) => <option key={currency} value={currency}>{currency}</option>)
            setUserCurrenciesOptions(currenciesOptions)
        })
    }, [token, user])

    const titleChange = (element) => {
        const elementValue = element.target.value

        setTitleValue(elementValue)

        if (elementValue.length < 1 || elementValue.length > 20) {
            setTitleStyle({color: "red"});
        } else {
            setTitleStyle({})
        }
    }

    const currencyChange = (element) => {
        const elementValue = element.target.options[element.target.selectedIndex].value;

        setCurrencyValue(elementValue)
    }

    const colorChange = (element) => {
        const elementValue = element.target.value

        setColorValue(elementValue)
    }

    const formSubmit = (element) => {
        element.preventDefault()

        if (titleStyle.color || !titleValue) return;

        const payload = {
            title: titleValue,
            currency: currencyValue,
            color: colorValue,
        }

        createCard(payload, token).then(({ status, card }) => {
            switch (status) {
                case 200:
                    setCards((cards) => [...cards, card])
                    navigate('/cards')
                    break
                case 400:
                    setErrorMessageStyle({})
                    setUniqueMessageStyle({display: "block"})
                    break
                default:
                    setUniqueMessageStyle({})
                    setErrorMessageStyle({display: "block"});
                    break
            }
        })
    }

    return (
        <div className="addPopUpContainer">
            <Link to="/cards" className="backLink" />

            <form className="addForm bg-white dark:bg-background-black text-black dark:text-white" onSubmit={formSubmit}>
                <h2>Create card</h2>

                <div className="addFormErrorMessage" style={uniqueMessageStyle}>Card with this title already exists</div>
                <div className="addFormErrorMessage" style={errorMessageStyle}>Error with sending request</div>

                <input className="bg-white dark:bg-foreground-black" placeholder='Card Title' onChange={titleChange} style={titleStyle} value={titleValue} required maxLength="20" minLength="1" />
                <select className="bg-white dark:bg-foreground-black" placeholder='Card Currency' onChange={currencyChange} value={currencyValue || user?.currency || ""} required>
                    {userCurrenciesOptions}
                </select>
                <p><input onChange={colorChange} value={colorValue} type='color' required /><label>Color</label></p>
                <button type="submit">Create</button>
            </form>
        </div>
    )
}