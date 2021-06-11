import './App.css';

function Header() {
	return (
		<div className="header">
			<header className="app_header">
				<div className="logo">CostsMap</div>
				<nav className="navigation_bar">
					<a className="navigation_link" href="#">Costs</a>
					<a className="navigation_link" href="#">Categories</a>
					<a className="navigation_link" href="#">Statistic</a>
					<a className="navigation_link" href="#">History</a>
				</nav>
			</header>
		</div>
	);
}

export default Header;