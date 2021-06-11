import React from 'react';
import './App.css';
import Header from './Header.js';

class App extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			user_key: localStorage.getItem('user_key')
		};
	}

	render() {
		if (this.state.user_key === null) {
			return (
				<div className="app">
					<Header />
					<section id="content"></section>
				</div>
			);
		} else {
			return (
				<div className="app">
					<Header />
				</div>
			);
		}
	}
}

export default App;
