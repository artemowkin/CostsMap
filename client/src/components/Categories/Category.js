export const Category = ({ category }) => {
    return (
        <div className="category" key={category.id}>
            <div className="categoryTitle">{category.title}</div>
            <div className="categoryImage" style={{backgroundColor: category.color}}>$</div>
            <div className="categoryCostsLimit">{category.costs_limit}</div>
        </div>
    );
}