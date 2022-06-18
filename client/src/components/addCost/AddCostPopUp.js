import axios from 'axios';
import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';

const _convertDateToString = (date) => {
    return date.toISOString().split('T')[0]
}

const createCost = async (payload, token) => {
    try {
        const response = await axios({
            url: "/costs/",
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            data: payload
        })

        return { status: response.status, cost: response.data }
    } catch (error) {
        return { status: error.response.status, cost: {} }
    }
}

export const AddCostPopUp = ({ token, setCosts, setCategories, setMonthCosts, user, categories, cards }) => {
    const [cardId, setCardId] = useState("")
    const [costSumValue, setCostSumValue] = useState("")
    const [costSumStyle, setCostSumStyle] = useState({})
    const [costDate, setCostDate] = useState(new Date())
    const [errorMessageStyle, setErrorMessageStyle] = useState({})
    const [jsxCards, setJsxCards] = useState([])

    const navigate = useNavigate()

    const { categoryId } = useParams()
    const selectedCategory = categories?.find((category) => category.id == categoryId)

    useEffect(() => {
        const availableCards = cards.filter((card) => card?.currency === user?.currency)
        const availableJsxCards = availableCards.map((card) => (
            <option key={card.id} value={card.id}>{card.title}</option>
        ))
        setJsxCards(availableJsxCards)
        setCardId(cards[0]?.id)
    }, [cards, user])

    const costCardChange = (element) => {
        const elementValue = element.target.value

        setCardId(Number(elementValue))
    }

    const costSumChange = (element) => {
        const elementValue = element.target.value

        setCostSumValue(elementValue)

        if (elementValue !== "" && (elementValue < 0.01 || elementValue > 10000000 || isNaN(elementValue))) {
            setCostSumStyle({color: "red"})
        } else {
            setCostSumStyle({})
        }
    }

    const costDateChange = (element) => {
        const elementValue = element.target.value

        const dateValue = new Date(elementValue)

        if (isNaN(dateValue)) {
            setCostDate(new Date())
        } else {
            setCostDate(dateValue)
        }
    }

    const formSubmit = (element) => {
        element.preventDefault()

        if (costSumStyle.color || !costSumValue) return;

        const payload = {
            amount: costSumValue,
            category_id: categoryId,
            card_id: cardId,
            date: _convertDateToString(costDate)
        }

        createCost(payload, token).then(({ status, cost }) => {
            switch (status) {
                case 200:
                    if (costDate.getFullYear() == new Date().getFullYear() && costDate.getMonth() == new Date().getMonth()) {
                        setCosts((costs) => [...costs, cost])
                        setMonthCosts((monthCosts) => +monthCosts + +costSumValue)

                        const changedCategories = categories.map((category) => {
                            if (category.id != categoryId) return category

                            category.costs_sum = +category.costs_sum + +costSumValue
                            return category
                        })

                        setCategories(changedCategories)
                    }

                    navigate('/')
                    break
                default:
                    setErrorMessageStyle({display: "block"});
                    break
            }
        })
    }

    return (
        <div className="addPopUpContainer">
            <Link to="/" className="backLink" />

            <form className="addForm bg-white dark:bg-background-black text-black dark:text-white" onSubmit={formSubmit}>
                <h2>Create cost for "{selectedCategory?.title}"</h2>

                <div className="addFormErrorMessage" style={errorMessageStyle}>Error with sending request</div>

                <select className="bg-white dark:bg-foreground-black" onChange={costCardChange} required>
                    {jsxCards}
                </select>
                <input className="bg-white dark:bg-foreground-black" placeholder='Cost Sum' onChange={costSumChange} style={costSumStyle} value={costSumValue} inputMode='decimal' min="0.01" max="10000000" required />
                <input className="bg-white dark:bg-foreground-black" onChange={costDateChange} value={_convertDateToString(costDate)} type="date" required />
                <button type="submit">Create</button>
            </form>
        </div>
    )
}