import editImage from '../../edit.svg'
import deleteImage from '../../delete.svg'
import { Link, useNavigate, useParams } from 'react-router-dom'

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