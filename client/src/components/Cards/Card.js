export const Card = ({ card }) => {
    return (
        <div className="card bg-white dark:bg-foreground-black">
            <div className="cardImage" style={{backgroundColor: card.color}}></div>
            <div className="cardInfo">
                <div className="cardTitle">{card.title}</div>
                <div className="cardAmount">{card.amount}{card.currency}</div>
            </div>
        </div>
    );
}
