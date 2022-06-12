export const Cost = ({ cost }) => {
    const costStyle = {backgroundColor: cost.category.color}

    return (
        <div key={cost.id} className="costCard bg-white dark:bg-foreground-black">
            <div className="costCardInfo">
                <div className="costCategoryImage" style={costStyle}>
                    <div className="costCategoryImageSymbol">{cost.card.currency}</div>
                </div>
                <div className="costCardText">
                    <div className="costCategoryTitle">{cost.category.title}</div>
                    <div className="costCardTitle">{cost.card.title}</div>
                </div>
            </div>
            <div className="costCardAmount">{cost.amount}{cost.card.currency}</div>
        </div>
    )
}