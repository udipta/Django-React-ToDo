# To-Do Task App
***

<h4> TechStack Used</h4>
1. Python (Programming Language)<br>
2. Django (Web Framework)<br>
3. Postgres (Database)<br>
5. ReactJS (Fronted Framework)<br>
5. Nginx <br>

***

<h5> Webpage ScreenShots</h5>
<h6> 1. Login </h6>
<img src="screenshots/login.png" alt="login page">

| Status  | Time  | Size  |
| ------- |-------|-------|
| 200 OK  | 95 ms | 823 B |


<h6> 2. Sign Up </h6>
<img src="screenshots/singup.png" alt="signup page">

| Status  | Time  | Size  |
| ------- |-------|-------|
| 201 OK  | 108ms | 800 B |

<h6> 3. Dashboard </h6>
<img src="screenshots/task.png" alt="signup page">

<h6> 4. Create Task </h6>
<img src="screenshots/create task.png" alt="create page">

<h6> 5. Edit Task </h6>
<img src="screenshots/update task.png" alt="edit page">

<h6> 6. Delete Task </h6>
<img src="screenshots/delete task.png" alt="delete page">

<h5><a href="https://www.getpostman.com/collections/f9cf7d85df46ac1d89a6"> Postman Collection</a></h5>

***

<h5> How to set up and run locally </h5>
<p>
  1. Clone the Repository <br>
  2. After activating the virtual enviornment, redirect to project base directory. <br>
  3. Build and run the docker-compose
</p>

    docker-compose up --build

<br>
  5. Create superuser for accessing the dashboard as admin

    $ docker exec -it todo_list bash
    $ python3 manage.py createsuperuser
<br>
  6. To access the dashboard checkout <a href="http://127.0.0.1/">here</a>
<br>
