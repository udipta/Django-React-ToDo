'use strict';
const e = React.createElement;

function App() {
	const [username, setUsername] = React.useState("");
	const [password1, setPassword1] = React.useState("");
	const [password2, setPassword2] = React.useState("");
	const [message, setMessage] = React.useState("");
	
	const routeChange = async (e) => {
		e.preventDefault();
		window.location = "/login";
	}
	
	const success = async (text) => {
		console.log("Yeah! Signup!");
		await localStorage.setItem("Token", text["auth_token"]);
		window.location = "/";
	};
	
	const trySignup = async (e) => {
		e.preventDefault();
		console.log("Signup in with", username, password1);
		await signup_api(username, password1, password2, success, (text) => {
			setMessage(text)
		});
	};
	
	return (
		<div style={{
			width: "400px", margin: "auto", marginTop: "200px",
			boxShadow: "5px 5px 20px #cccccccc",
			padding: "1em"
		}}>
			<form>
				<div className="mb-3">
					<label htmlFor="username" className="form-label">Username</label>
					<input autoFocus type="text" className="form-control" id="username" placeholder="username"
					       autoComplete="off"
					       onChange={(e) => {
						       setUsername(e.target.value)
					       }} value={username}/>
				</div>
				<div className="mb-3">
					<label htmlFor="password" className="form-label">Password</label>
					<input type="password" className="form-control" id="password1" placeholder="password"
					       autoComplete="off"
					       onChange={(e) => {
						       setPassword1(e.target.value)
					       }} value={password1}/>
				</div>
				<div className="mb-3">
					<label htmlFor="password" className="form-label">Repeat Password</label>
					<input type="password" className="form-control" id="password2" placeholder="repeat password"
					       autoComplete="off"
					       onChange={(e) => {
						       setPassword2(e.target.value)
					       }} value={password2}/>
				</div>
				<div style={{margin: "1em", color: "red"}}>{message}</div>
				<button type="submit" className="btn btn-primary" onClick={trySignup}>Signup</button>
				<button type="submit" className="btn btn-secondary" onClick={routeChange}>Login</button>
			</form>
		</div>
	);
}

const domContainer = document.querySelector('#reactAppContainer');
ReactDOM.render(
	e(App),
	domContainer
);