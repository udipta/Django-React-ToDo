const signup_api = async (username, password, confirm_password, success, fail) => {
	const response = await fetch(
		`/auth/signup/`,
		{
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				"username": username,
				"password": password,
				"confirm_password": confirm_password
			})
		}
	);
	const text = await response.text();
	if (response.status === 400) {
		console.log("Username/Password not valid");
		window.location = "/signup";
		return [];
	}
	if (response.status === 201) {
		console.log("success", JSON.parse(text));
		success(JSON.parse(text));
	} else {
		console.log("failed", text);
		Object.entries(JSON.parse(text)).forEach(([key, value])=>{
			fail(`${key}: ${value}`);
		});
	}
};

const login_api = async (username, password, success, fail) => {
	const response = await fetch(
		`/auth/login/`,
		{
			method: 'POST',
			headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				"username": username,
				"password": password,
			})
		}
	);
	const text = await response.text();
	
	if (response.status === 401) {
		console.log("Token not valid");
		window.location = "/login";
		return [];
	}
	if (response.status === 200) {
		console.log("success", JSON.parse(text));
		success(JSON.parse(text));
	} else {
		console.log("failed", text);
		Object.entries(JSON.parse(text)).forEach(([key, value])=>{
			fail(`${key}: ${value}`);
		});
	}
};

const get_task_api = async (pageNo, success, fail) => {
	const [token] = await Promise.all([localStorage.getItem("Token")]);
	if (token === null) {
		console.log("No credentials found, redirecting...");
		window.location = "/login";
		return [];
	}
	console.log("Page No", pageNo);
	const response = await fetch(
		(pageNo > 1) ? `/task/?page=${pageNo}` : `/task/`,
		{
			method: 'GET',
			headers: {
				'Content-Type': 'Application/JSON',
				'Authorization': `Token ${token}`,
			}
		}
	);
	
	const data = await response.json();
	if (response.status === 401) {
	    console.log("Token not valid");
	    window.location = "/login";
	    return [];
    }
	if (response.status === 200) {
		console.log("success", data);
		success(data);
	} else {
		console.log("failed", data);
		Object.entries(data).forEach(([key, value])=>{
			fail(`${key}: ${value}`);
		});
		return [];
	}
};

const post_task_api = async (data, success) => {
	const token = localStorage.getItem("Token");
	if (token === null) {
		console.log("No credentials found, redirecting...");
		window.location = "/login";
		return [];
	}
	const response = await fetch(
		`/task/`,
		{
			method: 'POST',
			headers: {
				'Content-Type': 'Application/JSON',
				'Authorization': `Token ${token}`,
			},
			body: JSON.stringify(data)
		}
	);
	const text = await response.text();
	if (response.status === 401) {
		console.log("Token not valid");
		window.location = "/login";
		return [];
	}
	if (response.status === 201) {
		console.log("success", JSON.parse(text));
		success(JSON.parse(text));
	} else {
		console.log("failed", text);
		Object.entries(JSON.parse(text)).forEach(([key, value])=>{
			fail(`${key}: ${value}`);
		});
	}
};

const put_task_api = async (taskId, data, success) => {
	const token = localStorage.getItem("Token");
	if (token === null) {
		console.log("No credentials found, redirecting...");
		window.location = "/login";
		return [];
	}
	const response = await fetch(
		`/task/${taskId}/`,
		{
			method: 'PUT',
			headers: {
				'Content-Type': 'Application/JSON',
				'Authorization': `Token ${token}`,
			},
			body: JSON.stringify(data)
		}
	);
	const text = await response.text();
	if (response.status === 401) {
		console.log("Token not valid");
		window.location = "/login";
		return [];
	}
	if (response.status === 202) {
		console.log("success", JSON.parse(text));
		success(JSON.parse(text));
	} else {
		console.log("failed", text);
		Object.entries(JSON.parse(text)).forEach(([key, value])=>{
			fail(`${key}: ${value}`);
		});
	}
};

const delete_task_api = async (taskId) => {
	const token = localStorage.getItem("Token");
	if (token === null) {
		console.log("No credentials found, redirecting...");
		window.location = "/login";
		return [];
	}
	const response = await fetch(
		`/task/${taskId}/`,
		{
			method: 'DELETE',
			headers: {
				'Content-Type': 'Application/JSON',
				'Authorization': `Token ${token}`,
			}
		}
	);
	const text = await response.text();
	if (response.status === 401) {
		console.log("Token not valid");
		window.location = "/login";
		return [];
	}
  if (response.status === 204 ) {
	  console.log("success");
	  window.location = "/";
	  return [];
  } else {
	  console.log("failed", text);
	  Object.entries(JSON.parse(text)).forEach(([key, value]) => {
		  fail(`${key}: ${value}`);
	  });
  }
};