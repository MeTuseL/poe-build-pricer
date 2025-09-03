### 1. Doc API
The doc API is available at the following address after launching the server : 
````http://localhost:8000/api/docs/````

### 2. Basic instructions on launching BACKEND server locally :

Launch those commands :
- ````cd backend````: Go to backend folder
- ````python -m venv venv````: Create a virtual environment
- ````source venv/bin/activate````: Activate the virtual environment
- ou ````.\venv\Scripts\activate```` on Windows
- ````pip install -r requirements.txt````: Install dependencies
- ````python manage.py migrate````: Migrate the database from "migrations" files
- ````python manage.py runserver````: Launch the server

### 3. Temporary setting for .env to launch PostgreSQL Serveur :
- Always have PostgreSQL Launched
- Create a PostgreSQL server locally
- Add the following line in a file named ".env" in "backend/" :
    ````
    # Database configuration with PostgreSQL
    POSTGRES_HOST=localhost
    POSTGRES_DB=your_db
    POSTGRES_USER=your_user
    POSTGRES_PASSWORD=your_password
    POSTGRES_PORT=5432
    ````
Configure your .env as you need, in particular :
- "POSTGRES_DB": the name of your database created in Postgre
- "POSTGRES_USER": the name of the user used to connect to your database
- "POSTGRES_PASSWORD": the password of the user used to connect to your database

### 4. Test

````python -m pytest -v````: run test from backend

### 5. Useful commands :

- ````python manage.py makemigrations````: create migration files for your models to apply to database
- ````python manage.py createsuperuser````: create a superuser to access to admin page

### 6. Example of response from routes :
Two examples of response from routes are given in the folder "route_response_exemple". They correspond to the response of the routes "price_pob" and "decode_pob", name in the endpoint "Pricer" and "Parser".
