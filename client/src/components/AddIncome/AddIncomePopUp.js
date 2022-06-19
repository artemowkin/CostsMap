import axios from 'axios'
import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

const _convertDateToString = (date) => {
    return date.toISOString().split('T')[0]
}

const createIncome = async (payload, token) => {
    try {
        const response = await axios({
            url: "/incomes/",
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            data: payload
        })

        return { status: response.status, income: response.data }
    } catch (error) {
        return { status: error.response.status, income: {} }
    }
}

export const AddIncomePopUp = ({ token, setIncomes, setMonthIncomes, setCards, user, cards }) => {
    const [cardId, setCardId] = useState("")
    const [incomeAmount, setIncomeAmount] = useState("")
    const [incomeCardAmount, setIncomeCardAmount] = useState("")
    const [incomeAmountStyle, setIncomeAmountStyle] = useState({})
    const [incomeCardAmountStyle, setIncomeCardAmountStyle] = useState({})
    const [incomeDate, setIncomeDate] = useState(new Date())
    const [errorMessageStyle, setErrorMessageStyle] = useState({})
    const [jsxCards, setJsxCards] = useState([])

    const navigate = useNavigate()

    const selectedCard = cards.find((card) => card.id == cardId)

    useEffect(() => {
        const jsxCards = cards.map((card) => (
            <option key={card.id} value={card.id}>{card.title}</option>
        ))
        setJsxCards(jsxCards)
        setCardId(cards[0]?.id)
    }, [cards])

    const incomeCardChange = (element) => {
        const elementValue = element.target.value

        setCardId(Number(elementValue))
    }

    const incomeAmountChange = (element) => {
        const elementValue = element.target.value

        setIncomeAmount(elementValue)

        if (elementValue !== "" && (elementValue < 0.01 || elementValue > 10000000 || isNaN(elementValue))) {
            setIncomeAmountStyle({color: "red"})
        } else {
            setIncomeAmountStyle({})
        }
    }

    const incomeCardAmountChange = (element) => {
        const elementValue = element.target.value

        setIncomeCardAmount(elementValue)

        if (elementValue !== "" && (elementValue < 0.01 || elementValue > 10000000 || isNaN(elementValue))) {
            setIncomeCardAmountStyle({color: "red"})
        } else {
            setIncomeCardAmountStyle({})
        }
    }

    const incomeDateChange = (element) => {
        const elementValue = element.target.value

        const dateValue = new Date(elementValue)

        if (isNaN(dateValue)) {
            setIncomeDate(new Date())
        } else {
            setIncomeDate(dateValue)
        }
    }

    const formSubmit = (element) => {
        element.preventDefault()

        if (selectedCard.currency === user.currency) {
            if (incomeAmountStyle.color || !incomeAmount) return
        } else {
            if (incomeAmountStyle.color || incomeCardAmountStyle.color || !incomeAmount || !incomeCardAmount) return
        }

        const payload = {
            user_currency_amount: +incomeAmount,
            card_id: +cardId,
            date: _convertDateToString(incomeDate)
        }

        if (selectedCard.currency !== user.currency)
            payload.card_currency_amount = +incomeCardAmount

        createIncome(payload, token).then(({ status, income }) => {
            switch (status) {
                case 200:
                    if (incomeDate.getFullYear() == new Date().getFullYear() && incomeDate.getMonth() == new Date().getMonth()) {
                        setIncomes((incomes) => [income, ...incomes])
                        setMonthIncomes((monthIncomes) => +monthIncomes + +incomeAmount)

                        const newCards = cards.map((card) => {
                            if (card.id != cardId)
                                return card

                            if (selectedCard.currency === user.currency)
                                card.amount = +card.amount + +incomeAmount
                            else
                                card.amount = +card.amount + +incomeCardAmount

                            return card
                        })
                        setCards(newCards)
                    }

                    navigate('/')
                    break
                default:
                    setErrorMessageStyle({display: "block"});
                    break
            }
        })
    }

    let cardAmountInput = null

    if (selectedCard?.currency !== user.currency)
        cardAmountInput = (
            <input className="bg-white dark:bg-foreground-black" placeholder="Card Currency Amount" onChange={incomeCardAmountChange} style={incomeCardAmountStyle} value={incomeCardAmount} inputMode='decimal' min='0.01' max='10000000' required/>
        )

    return (
        <div className="addPopUpContainer">
            <Link to="/" className="backLink" />

            <form className="addForm bg-white dark:bg-background-black text-black dark:text-white" onSubmit={formSubmit}>
                <h2>Create income</h2>

                <div className="addFormErrorMessage" style={errorMessageStyle}>Error with sending request</div>

                <select className="bg-white dark:bg-foreground-black" onChange={incomeCardChange} required>
                    {jsxCards}
                </select>
                <input className="bg-white dark:bg-foreground-black" placeholder='Income Amount' onChange={incomeAmountChange} style={incomeAmountStyle} value={incomeAmount} inputMode='decimal' min="0.01" max="10000000" required />
                {cardAmountInput}
                <input className="bg-white dark:bg-foreground-black" onChange={incomeDateChange} value={_convertDateToString(incomeDate)} type="date" required />
                <button type="submit">Create</button>
            </form>
        </div>
    )
}