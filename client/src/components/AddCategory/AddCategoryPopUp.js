import { useState } from 'react';
import { Link } from 'react-router-dom';
import './addCategoryPopUp.css';

const createCategory = async (payload, token) => {
    const response = await fetch("http://192.168.0.156:800/api/v1/categories/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    })
}

export const AddCategoryPopUp = ({ token }) => {
    const [titleValue, setTitleValue] = useState("")
    const [titleStyle, setTitleStyle] = useState({})
    const [costsLimitValue, setCostsLimitValue] = useState("");
    const [costsLimitStyle, setCostsLimitStyle] = useState({});

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

        if (elementValue !== "" && (elementValue < 1 || elementValue > 999999)) {
            setCostsLimitStyle({color: "red"})
        } else {
            setCostsLimitStyle({});
        }
    }

    return (
        <div className="addCategoryPopUpContainer">
            <Link to="/" className="backLink" />
            <form className="addCategoryForm">
                <h2>Create category</h2>
                <input placeholder='Category Title' onChange={titleChange} style={titleStyle} value={titleValue} required maxLength="10" minLength="1" />
                <input placeholder='Costs Limit' onChange={costsLimitChange} style={costsLimitStyle} value={costsLimitValue} inputMode='numeric' min="1" max="999999" />
                <p><input placeholder='Costs Limit' type='color' required /><label>Color</label></p>
                <button type="submit">Create</button>
            </form>
        </div>
    )
}