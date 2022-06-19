import editImage from '../../edit.svg'
import deleteImage from '../../delete.svg'
import { Link, useNavigate, useParams } from 'react-router-dom'

import axios from 'axios'
import { useState } from 'react'

const deleteCard = async (cardId, token) => {
    const response = await axios({
        url: `/cards/${cardId}/`,
        method: "DELETE",
        headers: {"Authorization": `Bearer ${token}`}
    })

    return response.data
}

export const CardMenu = ({ token, setCards, setCosts, setIncomes, setMonthCosts, setMonthIncomes }) => {
    const { cardId } = useParams()

    const navigate = useNavigate()

    const deleteClick = (element) => {
        element.preventDefault()

        if (!window.confirm("Are you sure you want to delete this card?")) return

        deleteCard(cardId, token).then(() => {
            setCards((cards) => cards.filter((card) => card.id != cardId))

            let totalDeletedCosts = 0
            let totalDeletedIncomes = 0

            setCosts((costs) => {
                const deletingCosts = costs.filter((cost) => cost.card.id == cardId)
                const deletingCostsAmounts = deletingCosts.map((cost) => cost.amount)
                totalDeletedCosts = deletingCostsAmounts.reduce((a, b) => a + b, 0)

                return costs.filter((cost) => cost.card.id != cardId)
            })

            setIncomes((incomes) => {
                const deletingIncomes = incomes.filter((income) => income.card.id == cardId)
                const deletingIncomesAmounts = deletingIncomes.map((income) => income.user_currency_amount)
                totalDeletedIncomes = deletingIncomesAmounts.reduce((a, b) => a + b, 0)

                return incomes.filter((income) => income.card.id != cardId)
            })

            setMonthCosts((monthCosts) => monthCosts - totalDeletedCosts)
            setMonthIncomes((monthIncomes) => monthIncomes - totalDeletedIncomes)

            navigate("/cards")
        })
    }

    return (
        <div className="menuPopUp">
            <Link to="/cards" className="backLink" />
            <div className="menuContainer bg-white dark:bg-foreground-black">
                <Link to="/cards" className="menuContainerButton">
                    <div className="menuImageContainer">
                        <img src={editImage} />
                    </div>
                    <div className="menuButtonTitle">edit</div>
                </Link>
                <button onClick={deleteClick} className="menuContainerButton">
                    <div className="menuImageContainer">
                        <img src={deleteImage} />
                    </div>
                    <div className="menuButtonTitle">delete</div>
                </button>
            </div>
        </div>
    )
}