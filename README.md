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
