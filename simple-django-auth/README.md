# Simple Django Authentication 

A simple Django REST Framework (DRF) authentication API that includes user registration, login, logout, and password reset functionalities.

## Features
- User registration via API
- Token-based authentication
- User login/logout
- Password reset via email
- Secure authentication using Django REST Framework

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/amieecode/django-auth.git
   cd simple-django-auth
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Configuration
1. Update `settings.py` with your database and email configurations.
2. Ensure `REST_FRAMEWORK` is set up for authentication in `settings.py`:
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': (
           'rest_framework.authentication.TokenAuthentication',
       ),
   }
   ```
3. Run the following command to generate authentication tokens:
   ```bash
   python manage.py drf_create_token <your-username>
   ```

## API Endpoints

| Endpoint                  | Method | Description |
|---------------------------|--------|-------------|
| `/api/register/`          | POST   | Register a new user |
| `/api/login/`             | POST   | Obtain authentication token |
| `/api/logout/`            | POST   | Logout user |
| `/api/password-reset/`    | POST   | Request password reset |
| `/api/password-reset-confirm/` | POST | Confirm password reset |

## Technologies Used
- Django REST Framework
- Django
- SQLite (default, can be changed)
- Token Authentication

## License
This project is licensed under the MIT License.

## Contributions
Feel free to fork the repository and submit pull requests.

## Contact
For any inquiries, reach out at [your-email@example.com].

