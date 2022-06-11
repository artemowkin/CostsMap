import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './addCategoryPopUp.css';

const createCategory = async (payload, token) => {
    const response = await fetch("http://192.168.0.156:8000/api/v1/categories/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    })

    if (response.status > 299) return { status: response.status, category: null }

    const createdCategory = await response.json()

    return { status: response.status, category: createdCategory }
}

export const AddCategoryPopUp = ({ token, setCategories }) => {
    const [titleValue, setTitleValue] = useState("")
    const [titleStyle, setTitleStyle] = useState({})
    const [costsLimitValue, setCostsLimitValue] = useState("")
    const [costsLimitStyle, setCostsLimitStyle] = useState({})
    const [colorValue, setColorValue] = useState("#000000")
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

        if (costsLimitValue) payload.costs_limit = costsLimitValue;

        createCategory(payload, token).then(({ status, category }) => {
            switch (status) {
                case 200:
                    setCategories((categories) => categories.push(category))
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
        <div className="addCategoryPopUpContainer">
            <Link to="/" className="backLink" />

            <form className="addCategoryForm" onSubmit={formSubmit}>
                <h2>Create category</h2>

                <div className="categoryErrorMessage" style={uniqueMessageStyle}>Category with this title already exists</div>
                <div className="categoryErrorMessage" style={errorMessageStyle}>Error with sending request</div>

                <input placeholder='Category Title' autoFocus onChange={titleChange} style={titleStyle} value={titleValue} required maxLength="10" minLength="1" />
                <input placeholder='Costs Limit' onChange={costsLimitChange} style={costsLimitStyle} value={costsLimitValue} inputMode='numeric' min="1" max="999999" />
                <p><input onChange={colorChange} value={colorValue} type='color' required /><label>Color</label></p>
                <button type="submit">Create</button>
            </form>
        </div>
    )
}