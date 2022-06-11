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
            <nav className="footerWrapper bg-white dark:bg-foreground-black text-black dark:text-white">
                <Link to="/">
                    <div className="footerIconBackground">
                        <img src={categories} alt="categories"/>
                    </div>
                    <div className="footerIconTitle text-black dark:text-white">categories</div>
                </Link>
                <Link to="/cards">
                    <div className="footerIconBackground">
                        <img src={cards} alt="cards"/>
                    </div>
                    <div className="footerIconTitle text-black dark:text-white">cards</div>
                </Link>
                <Link to="/costs">
                    <div className="footerIconBackground">
                        <img src={costs} alt="costs"/>
                    </div>
                    <div className="footerIconTitle text-black dark:text-white">costs</div>
                </Link>
                <Link to="/">
                    <div className="footerIconBackground">
                        <img src={statistic} alt="statistic"/>
                    </div>
                    <div className="footerIconTitle text-black dark:text-white">statistic</div>
                </Link>
                <Link to="/">
                    <div className="footerIconBackground">
                        <img src={account} alt="account"/>
                    </div>
                    <div className="footerIconTitle text-black dark:text-white">account</div>
                </Link>
            </nav>
        </footer>
    );
}