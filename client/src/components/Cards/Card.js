import { Link } from "react-router-dom";

export const Card = ({ card }) => {
    const linkUrl = `/card_menu/${card?.id}`

    return (
        <Link to={linkUrl} className="card bg-white dark:bg-foreground-black">
            <div className="cardImage" style={{backgroundColor: card.color}}></div>
            <div className="cardInfo">
                <div className="cardTitle">{card.title}</div>
                <div className="cardAmount">{card.amount}{card.currency}</div>
            </div>
        </Link>
    );
}
