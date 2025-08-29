### Temporary setting for .env to launch PostgreSQL Serveur :

- Always have PostgreSQL Launched
- Create a PostgreSQL server locally.
- Add the following line in a file named ".env" in "backend/" :
    ````
    # Database configuration with PostgreSQL
    POSTGRES_HOST=localhost
    POSTGRES_DB=your_db
    POSTGRES_USER=your_user
    POSTGRES_PASSWORD=your_password
    POSTGRES_PORT=5432
    ````
  Configure your .env as you need, in particular "POSTGRES_DB", "POSTGRES_USER" and "POSTGRES_PASSWORD".
