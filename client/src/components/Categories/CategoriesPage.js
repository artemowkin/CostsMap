import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Nav } from '../Nav/Nav';
import './CategoriesPage.css';
import { Category } from './Category';

const getUserCategories = async (token) => {
    const response = await fetch("http://192.168.0.156:8000/api/v1/categories/", {
        method: "GET",
        headers: {"Authorization": `Bearer ${token}`}
    });
    const jsonCategories = await response.json();
    return jsonCategories;
}

export const CategoriesPage = ({ token }) => {
    const [jsxCategories, setJsxCategories] = useState([]);

    useEffect(() => {
        getUserCategories(token).then((userCategories) => {
            const formattedCategories = userCategories.map((category) => <Category key={category.id} category={category} />);
            setJsxCategories(formattedCategories);
        });
    }, []);

    return (
        <main className="categoriesPage">
            <section className="categoriesList">
                {jsxCategories}
                <Link className="addButton" to="/">
                    <div className="addButtonImage">+</div>
                    <div className="addButtonTitle">Add</div>
                </Link>
            </section>
            <Nav />
        </main>
    );
}
