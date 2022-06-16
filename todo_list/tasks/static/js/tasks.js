'use strict';
const e = React.createElement;

function App() {
	const [list, setList] = React.useState([]);
	const [pages, setPages] = React.useState([]);
	const [page, setPage] = React.useState(0);
	const [showModal, setShowModal] = React.useState(false);
	const [modalDescription, setModalDescription] = React.useState("");
	const [taskId, setTaskId] = React.useState(null);
	const [error, setError] = React.useState("");
	const [title, setTitle] = React.useState("");
	const [status, setStatus] = React.useState(0);
	
	const statusMap = {0: "Todo", 1: "In-Progress", 2: "Completed"};
	
	const success = (data) => {
		setList(data.results);
		const newPages = [];
		if (data.count > 10) {
			for (let i=2; i<=Math.ceil(data.count / 10); i++) {
				newPages.push({
					page: i,
				});
				console.log("page",i);
			}
			if (page > newPages.length-1) {
				setPage(page-1);
			}
		} else {
			setPage(0);
		}
		setPages(newPages);
	};
	
	const logout = async (e)=>{
		await localStorage.setItem("Token",null);
		window.location = "/login";
	};
	
	const getData = ()=> {
		get_task_api(page, success, (text) => {
			console.log("Error: ", text)
		});
	};
	
	const newTask = ()=>{
		setModalDescription("New Task");
		setTaskId(null);
		setTitle("");
		setStatus(0);
		setError("");
		setShowModal(true);
		const itemInput = document.getElementById("itemInput");
		setTimeout(()=>{itemInput && itemInput.focus()}, 1);
	};
	
	const editTask = (data)=>{
		setModalDescription("New Task");
		setTaskId(data.id);
		setTitle(data.title);
		setStatus(data.status);
		setError("");
		setShowModal(true);
		const itemInput = document.getElementById("itemInput");
		setTimeout(()=>{itemInput && itemInput.focus()}, 1);
	};
	
	const saveTask = (e)=>{
		e.preventDefault();
		setError("");
		console.log("saving new", title);
		if (title.length === 0)
			setError("Please enter title");
		else {
			if (taskId === null)
				post_task_api({title, status}, ()=>{getData();});
			else
				put_task_api(taskId, {title, status}, ()=>{getData();});
			setShowModal(false);
		}
	};
	
	const deleteTask = (TaskId)=>{
		Swal.fire({
			title: 'Are you sure?',
			text: "You won't be able to revert this!",
			icon: 'warning',
			showCancelButton: true,
			confirmButtonColor: '#3085d6',
			cancelButtonColor: '#d33',
			confirmButtonText: 'Yes, delete it!'
		}).then((result) => {
			if (result.isConfirmed) {
				delete_task_api(TaskId, ()=>{
					getData();
				});
			}
		});
	};
	
	const keyDownHandler = (e)=>{
		if (e.which === 27)
			setShowModal(false);
	};
	
	React.useEffect(()=>{
		getData();
	}, [page]);
	
	return (
		<div onKeyDown={keyDownHandler}>
			<div style={{background: "#00000060"}}
			     className={"modal " + (showModal?" show d-block":" d-none")} tabIndex="-1" role="dialog">
				<div className="modal-dialog shadow">
					<form method="post">
						<div className="modal-content">
							<div className="modal-header">
								<h5 className="modal-title">{modalDescription}</h5>
								<button type="button" className="btn-close" onClick={()=>{setShowModal(false)}} aria-label="Close"></button>
							</div>
							<div className="modal-body">
								<label>title name</label>
								<div className="form-group">
									<input type="text" className="form-control" name="title" id="itemInput"
									       value={title} onChange={(e)=>{setTitle(e.target.value)}}
									       placeholder="title"/>
								</div>
								<label style={{marginTop: "1em"}}>Status</label>
								<div className="form-group" >
									<select className="form-control" placeholder="status"
									        value={status} onChange={(e)=>{setStatus(e.target.value)}}
									        name="status">
										<option value="0">To-Do</option>
										<option value="1">In Progress</option>
										<option value="2">Done</option>
									</select>
								</div>
								<small className="form-text text-muted">{error}</small>
							</div>
							<div className="modal-footer">
								<button type="button" className="btn btn-secondary" onClick={()=>{setShowModal(false)}} data-bs-dismiss="modal">Close</button>
								<button type="submit" className="btn btn-primary" onClick={saveTask}>Save changes</button>
							</div>
						</div>
					</form>
				</div>
			</div>
			
			<div style={{maxWidth: "800px", margin: "auto", marginTop: "1em", marginBottom: "1em",
				padding: "1em"}} className="shadow">
				<div style={{display: "flex", flexDirection: "row"}}>
					<span>ToDo Tasks App</span>
					<a className="btn btn-light" style={{marginLeft: "auto"}} onClick={logout}>Logout</a>
				</div>
			</div>
			<div style={{maxWidth: "800px", margin: "auto", marginTop: "1em", marginBottom: "1em",
				padding: "1em"}} className="shadow">
				<div style={{display: "flex", flexDirection: "row", marginBottom: "5px"}}>
					{pages.length > 0 && <nav className="d-lg-flex justify-content-lg-end dataTables_paginate paging_simple_numbers">
						<ul className="pagination">
							<li className={"page-title " + (page === 0?"disabled":"")} onClick={(e)=>{
								e.preventDefault();
								setPage(Math.max(page-1,0));
							}}><a className="page-link" onClick={(e)=>getData()} aria-label="Previous"><span
								aria-hidden="true">«</span></a></li>
							{pages.map((el)=><li key={"page" + el.page} onClick={(e)=>{
								setPage(el.page);
							}} className={"page-title "+(page===el.page?"active":"")}>
								<a className="page-link" onClick={(e)=>getData()}>
									{el.page}
								</a></li>)}
							<li className={"page-title " + (page === pages.length-1?"disabled":"")} onClick={(e)=>{
								setPage(Math.min(page+1,pages.length-1));
							}}><a className="page-link" onClick={(e)=>getData()} aria-label="Next"><span
								aria-hidden="true">»</span></a></li>
						</ul>
					</nav>}
					<a className="btn btn-light" style={{marginLeft: "auto"}}
					   onClick={newTask}
					>Add New Task</a>
				</div>
				<table className="table table-hover caption-top">
					<thead className="table-light">
					<tr>
						<th>Title</th>
						<th>Created On</th>
						<th>Modified On</th>
						<th>Status</th>
						<th>Action</th>
					</tr>
					</thead>
					<tbody>
					{ list.map((row)=>
						<tr key={row.id}>
							<td>{row.title}</td>
							<td>{row.created}</td>
							<td>{row.modified}</td>
							<td>{statusMap[row.status]}</td>
							<td>
								<a className="btn btn-light" style={{marginLeft: "auto"}}
								   onClick={(e)=>{editTask(row)}}>Edit</a>{" "}
								<a className="btn btn-light" style={{marginLeft: "auto"}}
								   onClick={(e)=>{deleteTask(row.id)}}>Delete</a>
							</td>
						</tr>
					)}
					</tbody>
				</table>
			</div>
		</div>
	);
}

const domContainer = document.querySelector('#reactAppContainer');
ReactDOM.render(
	e(App),
	domContainer
);
