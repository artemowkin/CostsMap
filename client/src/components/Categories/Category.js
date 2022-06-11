export const Category = ({ category }) => {
    const categoryCostsSumStyle = category.costs_sum > category.costs_limit ? {color: "red"} : {}

    return (
        <div className="category">
            <div className="categoryTitle">{category.title}</div>
            <div className="categoryCostsLimit">{category.costs_limit}</div>
            <div className="categoryImage" style={{backgroundColor: category.color}}><div className="categoryImageCurrency">$</div></div>
            <div className="categoryCostsSum" style={categoryCostsSumStyle}>{category.costs_sum}</div>
        </div>
    );
}
