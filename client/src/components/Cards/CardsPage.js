import axios from "axios";
import { useEffect, useState } from "react"
import { Link } from "react-router-dom";
import { Nav } from "../Nav/Nav";
import { Card } from "./Card";

import './CardsPage.css';
import cardsIcon from '../../cards.svg';

const getUserCards = async (token) => {
    const response = await axios({
        url: "/cards/",
        method: "GET",
        headers: {"Authorization": `Bearer ${token}`}
    });
    return response.data;
}

export const CardsPage = ({ token, cards }) => {
    const [areCardsGetted, setAreCardsGetted] = useState(false);
    const [jsxCards, setJsxCards] = useState([]);

    useEffect(() => {
        getUserCards(token).then((userCards) => {
            const formattedCards = userCards.map((card) => <Card key={card.id} card={card} />)
            setJsxCards(formattedCards)
            setAreCardsGetted(true)
        });
    }, [token, cards]);

    if (areCardsGetted && jsxCards.length === 0)
        return (
            <>
                <div className="emptyPage">
                    <img src={cardsIcon} />
                    <h2>There are no cards</h2>
                </div>
                <div className="addCardButtonContainer">
                    <Link to="/" className="addCardButton bg-white dark:bg-background-black"><span>+ Card</span></Link>
                </div>
                <Nav />
            </>
        )

    return (
        <main className="cardsPage">
            <section className="cardsList">
                {jsxCards}
            </section>
            <div className="addCardButtonContainer">
                <Link to="/add_card" className="addCardButton bg-white dark:bg-background-black"><span>+ Card</span></Link>
            </div>
            <Nav />
        </main>
    )
}