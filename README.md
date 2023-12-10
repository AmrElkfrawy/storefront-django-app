# storefront-django-app
Storefront is a Django web application designed for efficient management of products, collections, users, and orders. The application is built on the Django web framework and utilizes MySQL as the database backend. With integrated permissions for fine-grained control, automated testing using pytest, and performance testing with tools like Locust and Silk, and the integration of development emails and Redis caching. This readme explains how to use

## How to use:
1. **Clone the Repository:**

    ```bash
    git clone https://github.com/AmrElkfrawy/storefront-django-app.git
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Create the Database:**

    - Create a MySQL database for your project.

4. **Configure Environment Variables:**
    - To run the Storefront Django app, you need to set up your configuration file (e.g., `.env`).
        ```env
        DATABASE_NAME = your_database_name
        DATABASE_USER = your_database_user
        DATABASE_PASSWORD = your_database_password

        EMAIL_USERNAME = your_mailtrap_username
        EMAIL_PASSWORD = your_mailtrap_password
        EMAIL_HOST = your_email_host
        EMAIL_PORT = your_email_port
        EMAIL_FROM = your_email_from

        SECRET_KEY = your_secret_key


5. **Apply Migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a Superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

    Visit `http://localhost:8000` in your browser.


## Usage

### 1. Store API Endpoints

Visit [http://localhost:8000/store](http://localhost:8000/store) to access the root of the APIs for the store.

### 2. User Registration and Authentication

- **User Registration:**
  - Visit [http://127.0.0.1:8000/auth/users/](http://127.0.0.1:8000/auth/users/) to register a new user.

- **User Login and Tokens:**
  - Use [http://127.0.0.1:8000/auth/jwt/create](http://127.0.0.1:8000/auth/jwt/create) for login and to obtain access and refresh tokens.
  - To refresh the access token, visit [http://127.0.0.1:8000/auth/jwt/refresh](http://127.0.0.1:8000/auth/jwt/refresh).

### 3. Django Admin Panel

Access the customized Django admin panel by visiting http://localhost:8000/admin. Log in using the superuser credentials created during the installation process.

### 4. Automated Testing

Execute the following command in the terminal to run automated tests with pytest:

```bash
pytest
```

### 5. Performance Testing

Run Locust for performance testing by using the following command:

```bash
locust -f locustfiles/browsers_products.py
```
Access http://localhost:8089/ to interact with the Locust web interface.

### 6. Silk Profiling
To use Silk for profiling, first uncomment configurations in `settings.py`, including installed apps, middlewares, and URLs in `urls.py`. Then, access http://localhost:8000/silk after running the application.
I commented them beacuase they add overhead on the requests as a middleware

### 7. Redis Caching
Uncomment the line # @method_decorator(cache_page(5*60)) in the `playground/views.py` file to enable Redis caching. Ensure that a Redis server is running in Docker by executing the following command:

```bash
docker run -d -p 6379:6379 redis
```
caching is used at this endpoint http://127.0.0.1:8000/playground/hello/

### 7. Run on Waitress Server
To run the application on a faster server, use the following command:
```bash
waitress-serve --listen=*:8000 storefront.wsgi:application
```
