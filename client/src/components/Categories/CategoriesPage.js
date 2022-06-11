import axios from 'axios';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Nav } from '../Nav/Nav';
import './CategoriesPage.css';
import { Category } from './Category';

const getUserCategories = async (token) => {
    const response = await axios({
        url: "/categories/",
        method: "GET",
        headers: {"Authorization": `Bearer ${token}`}
    });
    return response.data;
}

export const CategoriesPage = ({ token, categories, user }) => {
    const [jsxCategories, setJsxCategories] = useState([]);

    useEffect(() => {
        getUserCategories(token).then((userCategories) => {
            const formattedCategories = userCategories.map((category) => <Category key={category.id} category={category} user={user}/>);
            setJsxCategories(formattedCategories);
        });
    }, [categories, user]);

    return (
        <main className="categoriesPage">
            <section className="categoriesList">
                {jsxCategories}
                <Link className="addCategoryButton" to="/add_category">
                    <div className="addCategoryButtonImage">+</div>
                    <div className="addCategoryButtonTitle">Add</div>
                </Link>
                <div className="addIncomeButtonContainer">
                    <Link className="addIncomeButton" to="/">+ Income</Link>
                </div>
            </section>
            <Nav />
        </main>
    );
}
