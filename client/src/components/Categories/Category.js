export const Category = ({ category, user }) => {
    const categoryCostsSumStyle = category.costs_sum > category.costs_limit ? {color: "red"} : {}

    return (
        <div className="category">
            <div className="categoryTitle">{category.title}</div>
            <div className="categoryCostsLimit">{category.costs_limit ?? 0}{user.currency}</div>
            <div className="categoryImage" style={{backgroundColor: category.color}}><div className="categoryImageCurrency">{user.currency}</div></div>
            <div className="categoryCostsSum" style={categoryCostsSumStyle}>{category.costs_sum ?? 0}{user.currency}</div>
        </div>
    );
}
