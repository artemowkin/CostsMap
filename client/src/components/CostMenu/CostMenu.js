import editImage from '../../edit.svg'
import deleteImage from '../../delete.svg'
import { Link, useNavigate, useParams } from 'react-router-dom'

import axios from 'axios'

const deleteCost = async (costId, token) => {
    const response = await axios({
        url: `/costs/${costId}/`,
        method: "DELETE",
        headers: {"Authorization": `Bearer ${token}`}
    })

    return response.data
}

export const CostMenu = ({ token, costs, cards, categories, setCosts, setCards, setCategories, setMonthCosts }) => {
    const { costId } = useParams()

    const navigate = useNavigate()

    const selectedCost = costs.find((cost) => cost.id == costId)

    const deleteClick = (element) => {
        element.preventDefault()

        if (!window.confirm("Are you sure you want to delete this cost?")) return

        deleteCost(costId, token).then(() => {
            const newCosts = costs.filter((cost) => cost.id != costId)

            setCosts(newCosts)

            const newCards = cards.map((card) => {
                if (card.id != selectedCost.card.id) return card

                card.amount = card.amount + selectedCost.amount
                return card
            })
            setCards(newCards)

            const newCategories = categories.map((category) => {
                if (category.id != selectedCost.category.id) return category

                category.costs_sum = category.costs_sum - selectedCost.amount
                return category
            })
            setCategories(newCategories)

            setMonthCosts((monthCosts) => monthCosts - selectedCost.amount)

            navigate("/costs")
        })
    }

    return (
        <div className="menuPopUp">
            <Link to="/costs" className="backLink" />
            <div className="menuContainer bg-white dark:bg-foreground-black">
                <Link to="/costs" className="menuContainerButton">
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