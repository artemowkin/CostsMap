import React from 'react';
import ReactDOM from 'react-dom';
import './App.css';
import DayCosts from './Costs.js';

class Header extends React.Component {

	constructor(props) {
		super(props);

		this.state = {
			page: props.page
		}

		this.costsClick = this.costsClick.bind(this);
		this.categoriesClick = this.categoriesClick.bind(this);
		this.statisticClick = this.statisticClick.bind(this);
		this.historyClick = this.historyClick.bind(this);
	}

	costsClick() {
		if (Boolean(this.props.user_key) && this.state.page !== 1) {
			ReactDOM.render(
				<DayCosts user_key={this.props.user_key}/>,
				document.getElementById('content')
			);
			this.setState({page: 1});
		}
	}

	categoriesClick() {
		if (Boolean(this.props.user_key) && this.state.page !== 2) {
			ReactDOM.render(
				<h1>Hello Categories</h1>,
				document.getElementById('content')
			);
			this.setState({page: 2});
		}
	}

	statisticClick() {
		if (Boolean(this.props.user_key) && this.state.page !== 3) {
			ReactDOM.render(
				<h1>Hello Statistic</h1>,
				document.getElementById('content')
			);
			this.setState({page: 3});
		}
	}

	historyClick() {
		if (Boolean(this.props.user_key) && this.state.page !== 4) {
			ReactDOM.render(
				<h1>Hello History</h1>,
				document.getElementById('content')
			);
			this.setState({page: 4});
		}
	}

	render() {
		return (
			<div className="header">
				<header className="app_header">
					<div className="logo">CostsMap</div>
					<nav className="navigation_bar">
						<button
							className="navigation_link"
							onClick={this.costsClick}
						>Costs</button>
						<button
							className="navigation_link"
							onClick={this.categoriesClick}
						>Categories</button>
						<button
							className="navigation_link"
							onClick={this.statisticClick}
						>Statistic</button>
						<button
							className="navigation_link"
							onClick={this.historyClick}
						>History</button>
					</nav>
				</header>
			</div>
		);
	}
}

export default Header;