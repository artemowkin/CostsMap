export const Category = ({ category }) => {
    const categoryCostsSumStyle = category.costs_sum > category.costs_limit ? {color: "red"} : {}

    return (
        <div className="category" key={category.id}>
            <div className="categoryTitle">{category.title}</div>
            <div className="categoryCostsLimit">{category.costs_limit}</div>
            <div className="categoryImage" style={{backgroundColor: category.color}}>$</div>
            <div className="categoryCostsSum" style={categoryCostsSumStyle}>{category.costs_sum}</div>
        </div>
    );
}
