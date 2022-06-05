import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginRequired } from '../../hooks/Auth/useAuth';
import { Nav } from '../Nav/Nav';
import './CategoriesPage.css';
import { Category } from './Category';

const getUserCategories = async (token) => {
    const response = await fetch("http://localhost:8000/api/v1/categories/", {
        method: "GET",
        headers: {"Authorization": `Bearer ${token}`}
    });
    const jsonCategories = await response.json();
    return jsonCategories;
}

export const CategoriesPage = ({ token }) => {
    const [jsxCategories, setJsxCategories] = useState([]);
    const navigate = useNavigate();

    useEffect(() => loginRequired(token, navigate));

    useEffect(() => {
        getUserCategories(token).then((userCategories) => {
            const formattedCategories = userCategories.map((category) => <Category category={category} />);
            setJsxCategories(formattedCategories);
        });
    }, []);

    return (
        <main className="categoriesPage">
            <section className="categoriesList">
                {jsxCategories}
            </section>
            <Nav />
        </main>
    );
}