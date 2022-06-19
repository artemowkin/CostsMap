import { Link } from "react-router-dom";
import { roundDecimal } from "../../utils/numbers";

export const Category = ({ category, user }) => {
    const roundedCostsSum = roundDecimal(category.costs_sum)
    const categoryCostsSumStyle = (category.costs_limit !== null && roundedCostsSum > category.costs_limit) ? {color: "red"} : {}

    const addCostUrl = `/add_cost/${category?.id}`

    return (
        <Link to={addCostUrl} className="category">
            <div className="categoryTitle">{category.title}</div>
            <div className="categoryCostsLimit">{category.costs_limit ?? 0}{user.currency}</div>
            <div className="categoryImage" style={{backgroundColor: category.color}}><div className="categoryImageCurrency">{user.currency}</div></div>
            <div className="categoryCostsSum" style={categoryCostsSumStyle}>{roundedCostsSum}{user.currency}</div>
        </Link>
    );
}
