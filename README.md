## Installation

To install the required packages, use Python 3.11 to create a virtualenv,
then run `pip install -r requirements`.

Install node and npm as usual. You may have to run `npm install`.

## Starting the Django Server

To start the Django server in the backend, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the the backend folder.
3. Run the following command to start the server:
   ```
   python manage.py runserver
   ```
4. The server should now be running on `http://localhost:8000/`.

## Logging in to the Admin Panel

To log in to the admin panel, follow these steps:

1. Open a web browser.
2. Navigate to `http://localhost:8000/admin/`.
3. Enter your admin username and password.
4. Click the "Log in" button.
5. You should now be logged in to the admin panel.

## Starting the Frontend

To start the frontend, follow these steps:

1. Open a new terminal or command prompt.
2. Navigate to frontend/netflow_frontend.
3. Run the following command to start the frontend server:
   ```
   npm start
   ```
4. The frontend should now be running on `http://localhost:3000/`.

## Generating the OpenAPI Schema

To generate the schema.yml file, follow these steps:

 1. Open a terminal or command prompt.
 2. Navigate to the backend folder
 3. Execute the command below to generate the schema.yml file:
   ```
   python manage.py spectacular --file .\schema.yml
   ```
   
Note: It's recommended to regenerate the schema.yml file whenever changes are made to your Django models or API views to keep the API documentation up to date.