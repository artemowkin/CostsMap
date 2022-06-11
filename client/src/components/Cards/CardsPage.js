import { useEffect, useState } from "react"
import { Nav } from "../Nav/Nav";
import { Card } from "./Card";

import './CardsPage.css';

const getUserCards = async (token) => {
    const response = await fetch("http://192.168.0.156:8000/api/v1/cards/", {
        method: "GET",
        headers: {"Authorization": `Bearer ${token}`}
    });
    const jsonCategories = await response.json();
    return jsonCategories;
}

export const CardsPage = ({ token }) => {
    const [jsxCards, setJsxCards] = useState([]);

    useEffect(() => {
        getUserCards(token).then((userCards) => {
            const formattedCards = userCards.map((card) => <Card key={card.id} card={card} />);
            setJsxCards(formattedCards);
        });
    }, []);

    return (
        <main className="cardsPage">
            <section className="cardsList">
                {jsxCards}
            </section>
            <Nav />
        </main>
    )
}