import editImage from './edit.svg'
import deleteImage from './delete.svg'
import { Link, useNavigate, useParams } from 'react-router-dom'

import './CardMenu.css'
import axios from 'axios'

const deleteCard = async (cardId, token) => {
    const response = await axios({
        url: `/cards/${cardId}/`,
        method: "DELETE",
        headers: {"Authorization": `Bearer ${token}`}
    })

    return response.data
}

export const CardMenu = ({ token, setCards }) => {
    const { cardId } = useParams()
    const navigate = useNavigate()

    const deleteClick = (element) => {
        element.preventDefault()

        if (!window.confirm("Are you sure you want to delete this card?")) return

        deleteCard(cardId, token).then(() => {
            setCards((cards) => cards.filter((card) => card.id != cardId))
            navigate("/cards")
        })
    }

    return (
        <div className="cardMenuPopUp">
            <Link to="/cards" className="backLink" />
            <div className="cardMenuContainer bg-white dark:bg-foreground-black">
                <Link to="/cards" className="cardMenuContainerButton">
                    <div className="cardMenuImageContainer">
                        <img src={editImage} />
                    </div>
                    <div className="cardMenuButtonTitle">edit</div>
                </Link>
                <button onClick={deleteClick} className="cardMenuContainerButton">
                    <div className="cardMenuImageContainer">
                        <img src={deleteImage} />
                    </div>
                    <div className="cardMenuButtonTitle">delete</div>
                </button>
            </div>
        </div>
    )
}