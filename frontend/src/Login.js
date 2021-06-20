import React from 'react';
import axios from 'axios';
import ReactDOM from 'react-dom';
import DayCosts from './Costs';

class Login extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			error: false,
			email: '',
			password: '',
		};

		this.handleEmailChange = this.handleEmailChange.bind(this);
		this.handlePasswordChange = this.handlePasswordChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleSubmit(event) {
		axios.post('http://localhost:8000/accounts/login/', {
			email: this.state.email,
			password: this.state.password
		}).then((response) => {
			let user_key = response.data.key;
			localStorage.setItem('user_key', user_key);
			ReactDOM.render(
				<DayCosts user_key={user_key}/>,
				document.getElementById('content')
			);
		}).catch((error) => this.setState({error: true}));
		event.preventDefault();
	}

	handleEmailChange(event) {
		this.setState({email: event.target.value});
	}

	handlePasswordChange(event) {
		this.setState({password: event.target.value});
	}

	render() {
		if (this.state.error === true) {
			return (
				<form onSubmit={this.handleSubmit} className="login_form">
					<h1>Log In</h1>
					<p className="form_error">The e-mail address and/or password you specified are not correct.</p>
					<p>
						<label>Email:</label>
						<input type="email" value={this.state.email} onChange={this.handleEmailChange} placeholder="E-mail address"/>
					</p>
					<p>
						<label>Password:</label>
						<input type="password" value={this.state.password}onChange={this.handlePasswordChange} placeholder="Password"/>
					</p>
					<p><button type="submit">Log In</button></p>
				</form>
			);
		}

		return (
			<form onSubmit={this.handleSubmit} className="login_form">
				<h1>Log In</h1>
				<p>
					<label>Email:</label>
					<input type="email" value={this.state.email} onChange={this.handleEmailChange} placeholder="E-mail address"/>
				</p>
				<p>
					<label>Password:</label>
					<input type="password" value={this.state.password}onChange={this.handlePasswordChange} placeholder="Password"/>
				</p>
				<p><button type="submit">Log In</button></p>
			</form>
		);
	}
}

export default Login;