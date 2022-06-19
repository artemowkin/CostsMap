import axios from 'axios';
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const createCategory = async (payload, token) => {
    try {
        const response = await axios({
            url: "/categories/",
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            data: payload
        })

        return { status: response.status, category: response.data }
    } catch (error) {
        return { status: error.response.status, category: null }
    }
}

export const AddCategoryPopUp = ({ token, setCategories }) => {
    const [titleValue, setTitleValue] = useState("")
    const [titleStyle, setTitleStyle] = useState({})
    const [costsLimitValue, setCostsLimitValue] = useState("")
    const [costsLimitStyle, setCostsLimitStyle] = useState({})
    const [colorValue, setColorValue] = useState("#ff0000")
    const [uniqueMessageStyle, setUniqueMessageStyle] = useState({})
    const [errorMessageStyle, setErrorMessageStyle] = useState({})

    const navigate = useNavigate();

    const titleChange = (element) => {
        const elementValue = element.target.value

        setTitleValue(elementValue)

        if (elementValue.length < 1 || elementValue.length > 10) {
            setTitleStyle({color: "red"});
        } else {
            setTitleStyle({})
        }
    }

    const costsLimitChange = (element) => {
        const elementValue = element.target.value

        setCostsLimitValue(elementValue)

        if (elementValue !== "" && (elementValue < 1 || elementValue > 999999 || isNaN(elementValue))) {
            setCostsLimitStyle({color: "red"})
        } else {
            setCostsLimitStyle({})
        }
    }

    const colorChange = (element) => {
        const elementValue = element.target.value

        setColorValue(elementValue)
    }

    const formSubmit = (element) => {
        element.preventDefault()

        if (titleStyle.color || costsLimitStyle.color || !titleValue) return;

        const payload = {
            title: titleValue,
            color: colorValue,
        }

        if (costsLimitValue !== "") payload.costs_limit = costsLimitValue;

        createCategory(payload, token).then(({ status, category }) => {
            switch (status) {
                case 200:
                    setCategories((categories) => [...categories, category])
                    navigate('/')
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
            <Link to="/" className="backLink" />

            <form className="addForm bg-white dark:bg-background-black text-black dark:text-white" onSubmit={formSubmit}>
                <h2>Create category</h2>

                <div className="addFormErrorMessage" style={uniqueMessageStyle}>Category with this title already exists</div>
                <div className="addFormErrorMessage" style={errorMessageStyle}>Error with sending request</div>

                <input className="bg-white dark:bg-foreground-black" placeholder='Category Title' onChange={titleChange} style={titleStyle} value={titleValue} required maxLength="10" minLength="1" />
                <input className="bg-white dark:bg-foreground-black" placeholder='Costs Limit' onChange={costsLimitChange} style={costsLimitStyle} value={costsLimitValue} inputMode='numeric' min="1" max="999999" />
                <p><input onChange={colorChange} value={colorValue} type='color' required /><label>Color</label></p>
                <button type="submit">Create</button>
            </form>
        </div>
    )
}