export const Cost = ({ cost, user }) => {
    const costStyle = {backgroundColor: cost.category.color}

    return (
        <div key={cost.id} className="costCard bg-white bg-foreground-black">
            <div className="costCardInfo">
                <div className="costCategoryImage" style={costStyle}>
                    <div className="costCategoryImageSymbol">{user.currency}</div>
                </div>
                <div className="costCategoryTitle">{cost.category.title}</div>
            </div>
            <div className="costCardAmount">{cost.amount}</div>
        </div>
    )
}