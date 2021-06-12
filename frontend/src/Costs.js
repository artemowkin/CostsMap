import React from 'react';
import axios from 'axios';

class CostsList extends React.Component {

	render() {
		if (this.props.costs === null) {
			return this.renderNoCosts();
		} else {
			return this.renderCosts()
		}
	}

	renderNoCosts() {
		return (<p>Loading...</p>);
	}

	renderCosts() {
		if (this.props.costs.length === 0) {
			return (<p>There is no costs for this date :(</p>);
		} else {
			let costsItems = this.props.costs.map((cost) =>
				<div key={cost.pk} className="cost">
					<div className="cost_left">
						<div className="cost_image"></div>
						<div className="cost_description">
							<div className="cost_title">{cost.title}</div>
							<div className="cost_category">
								{cost.category.title}
							</div>
						</div>
					</div>
					<div className="cost_right">
						<div className="costs_sum">- {cost.costs_sum} ₽</div>
						<button className="cost_edit_button"></button>
					</div>
				</div>
			);
			return (
				<div className="day_costs">
					<div className="total_sum_container">
						<div className="total_sum">Total sum: {this.props.total_sum} ₽</div>
					</div>
					<div id="costs_list">{costsItems}</div>
				</div>
			);
		}
	}
}

class DayCosts extends React.Component {

	constructor(props) {
		super(props);

		this.state = {
			date: new Date(),
			costs: null,
			total_sum: 0
		};

		this.decrementDate = this.decrementDate.bind(this);
		this.incrementDate = this.incrementDate.bind(this);
	}

	requestCosts(date_obj) {
		let url = `http://localhost:8000/costs/${date_obj.getFullYear()}/` +
			`${date_obj.getMonth()+1}/${date_obj.getDate()}`

		axios.get(url, {
			headers: {
				'Authorization': `Token ${this.props.user_key}`
			}
		}).then((response) => this.setState({
			costs: response.data.costs,
			total_sum: response.data.total_sum
		}))
	}

	componentDidMount() {
		this.requestCosts(this.state.date);
	}

	render() {
		return (
			<div className="costs">
				<div className="dates">
					<button className="dates_button" onClick={this.decrementDate}>&lt;</button>
					<div className="dates_current_date">{this.state.date.toDateString()}</div>
					<button className="dates_button" onClick={this.incrementDate}>&gt;</button>
				</div>
				<section id="costs_list">
					<CostsList
						user_key={this.props.user_key}
						date={this.state.date}
						costs={this.state.costs}
						total_sum={this.state.total_sum}
					/>
				</section>
			</div>
		);
	}

	decrementDate() {
		let currentDate = this.state.date;
		currentDate.setDate(this.state.date.getDate() - 1);
		this.setState({date: currentDate});
		this.requestCosts(this.state.date);
	}

	incrementDate() {
		let currentDate = this.state.date;
		currentDate.setDate(this.state.date.getDate() + 1);
		this.setState({date: currentDate});
		this.requestCosts(this.state.date);
	}
}

export default DayCosts;