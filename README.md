# Daily-Expenses-Sharing-Application

## Index
## Overview

This is a backend application built with Django rest framework and SQLite for managing daily expenses. Users can create accounts, add expenses, and split them using different methods: equal amounts, exact amounts, and percentages. The application includes API endpoints for user and expense management, along with features to download balance sheets.

## Features

- User Management:
   - Create and manage user accounts.
   - Store user details (email, name, mobile number).
   
- Expense Management:
   - Add expenses with different splitting methods:
      - **Equal Split**: Divide the total equally among participants.
      - **Exact Amounts**: Specify exact amounts each participant owes.
      - **Percentage Split**: Specify percentages owed, ensuring they total 100%.

- Balance Sheet:
   - Track individual and overall expenses.
   - Downloadable balance sheet.

## Tech Stack

| Component       | Technology             |
|-----------------|------------------------|
| **Framework**   | Django                 |
| **Database**    | SQLite                 |
| **API**         | Django REST Framework  |
| **Authentication** | JWT (JSON Web Tokens) |

## Setup Instructions

1. **Clone the Repository**
   ```bash
  https://github.com/Niteshkushwaha89473/Daily-Expenses-Sharing-Application.git
   cd expenses_sharing
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Move to the Expenses Folder**
   ```bash
   cd expense_sharing
   ```

5. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Admin User**

   *IMPORTANT* -> Create this user to run admin-only API Endpoints.

   An admin user can be created using the Django admin panel or by running the following command:

   ```bash
   python manage.py createsuperuser
   ```

7. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

## Authentication

All endpoints except for Create User and Obtain Token require authentication using a JWT token. Include the token in the Authorization header as follows:

```
Authorization: Bearer <your_jwt_token>
```

Remember to replace placeholder values (like user IDs, amounts, etc.) with actual values when making requests.

## API Endpoints

### User Management

#### Create User
- **URL:** `/api/users/`
- **Method:** POST
- **Authorization:** Not Required ( **future work: Can add email or mobile-based OTP** )
- **Body:**
   ```json
   {
      "username": "Alok",
      "email": "alok@example.com",
      "password": "alok@123",
      "first_name": "Alok",
      "last_name": "Kumar"
   }
   ```

#### List Users
- **URL:** `/api/users/`
- **Method:** GET
- **Authentication:** Required (Admin Only)

#### Retrieve User
- **URL:** `/api/users/{id}/`
- **Method:** GET
- **Authentication:** Required

#### Update User Password
- **URL:** `/api/users/{id}/`
- **Method:** PUT
- **Authentication:** Required
- **Body:**
   ```json
   {
      "username": "Johnny",
      "password": "alok@1234"
   }
   ```

#### Delete User
- **URL:** `/api/users/{id}/`
- **Method:** DELETE
- **Authentication:** Required

### Authentication

#### Obtain Token
- **URL:** `/api/token/`
- **Method:** POST
- **Body:**
   ```json
   {
      "username": "alok",
      "password": "alok@123"
   }
   ```

#### Refresh Token
- **URL:** `/api/token/refresh/`
- **Method:** POST
- **Body:**
   ```json
   {
      "refresh": "your_refresh_token_here"
   }
   ```

### Expense Management

#### Create Expense
- **URL:** `/api/expenses/`
- **Method:** POST
- **Authentication:** Required
- **Body:**
   ```json
   {
      "title": "Dinner",
      "amount": "100.00",
      "split_type": "EQUAL",
      "splits": [
         {"user": 1},
         {"user": 2}
      ]
   }
   ```
   or
   ```json
   {
      "title": "Groceries",
      "amount": "80.00",
      "split_type": "EXACT",
      "splits": [
         {"user": 1, "amount": "40.00"},
         {"user": 2, "amount": "30.00"}
      ]
   }
   ```
   or
   ```json
   {
      "title": "Vacation",
      "amount": "1000.00",
      "split_type": "PERCENTAGE",
      "splits": [
         {"user": 1, "percentage": "60.00"},
         {"user": 2, "percentage": "40.00"}
      ]
   }
   ```

#### List All Expenses
- **URL:** `/api/expenses/overall_expenses/`
- **Method:** GET
- **Authentication:** Required (Admin Only)

#### Retrieve Expense
- **URL:** `/api/expenses/{id}/`
- **Method:** GET
- **Authentication:** Required

#### Update Expense
- **URL:** `/api/expenses/{id}/`
- **Method:** PUT
- **Authentication:** Required
- **Body:** (similar to Create Expense) (Admin Only)

#### Delete Expense
- **URL:** `/api/expenses/{id}/`
- **Method:** DELETE
- **Authentication:** Required (Admin Only)

#### User's Expenses
- **URL:** `/api/expenses/user_expenses/`
- **Method:** GET
- **Authentication:** Required

#### Download Balance Sheet
- **URL:** `/api/expenses/download_balance_sheet/`
- **Method:** GET
- **Authentication:** Required (Admin Only)
