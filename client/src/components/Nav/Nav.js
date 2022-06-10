import { Link } from "react-router-dom";

import categories from '../../categories.svg';
import cards from '../../cards.svg';
import costs from '../../costs.svg';
import statistic from '../../statistic.svg';
import account from '../../account.svg';

import './Nav.css';

export const Nav = () => {
    return (
        <footer>
            <nav className="footerWrapper">
                <Link to="/"><img src={categories} alt="categories"/></Link>
                <Link to="/cards"><img src={cards} alt="cards"/></Link>
                <Link to="/"><img src={costs} alt="costs"/></Link>
                <Link to="/"><img src={statistic} alt="statistic"/></Link>
                <Link to="/"><img src={account} alt="account"/></Link>
            </nav>
        </footer>
    );
}