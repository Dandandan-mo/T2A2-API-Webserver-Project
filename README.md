# [Github Repo](https://github.com/Dandandan-mo/T2A2-API-Webserver-Project)
# R1 Problem to solve
This C2C e-commerce application aims to provide users an online platform for buying and selling thrift items. Some users who want to save money can find and purchase cost-saving second-hand products on this platform, while others with items they no longer need can sell the second-hand goods to give them a new life with the benefit of earning extra income. 
# R2 Why it needs solving
The resale market has been developing rapidly around the world, with second-hand goods gaining popularity among consumers, especially with the Gen X, Y, and Z. People with limited budget purchase second-hand products due to its most obvious benefit: saving money. In addition, buyers interested in vintage or unique items chose to buy second-hand products over new ones. In a seller's perspective, selling items no longer used is a great way to earn extra money. There are also a growing number of people who buy or sell second-hand items for the purpose of helping the environment and preserving natural resources. Selling the second-hand products is also a good way to deal with impluse purchases and avoide waste. The C2C e-commerce app is a flexible and easy-to-use platform that meets the needs mentioned above. Buying and selling is more convenient with the app and users can be both buyers and sellers and purchase products from each other. 
# R3 Why PostgreSQL
The database system chosen for this application is PostgreSQL. This application is devloped using the flask framework in Python, and Postgres's popular and advanced adapter Psycoog for Python enables Python to connect to PostgreSQL database and allows the access to PostgreSQL features with extensions. As a relational database system, PostgreSQL is scalable and shows a high quality of performance in fetching bulk data and operating complex queries when precise and structured data model are required, making it efficient for industrial applications. For developers, one advantage of PostgreSQL is the high level of support it offers. The comprehensive documentation and active community are helpful for developers to find solutions; the free source code and rich extension repository and powerful tools greatly reduce the effort of users. For businesses, PostgreSQL requires no associated licensing cost, allows unlimited number of deployment, and offers more profitable business model.

PostgreSQL also has some drawbacks. Designing and Normalising the database is time-consuming in PostgreSQL, and the complex queries and data structures make it harder to design and maintain the database, requiring higher level of professionalism of the developers compared with NoSQL and even other RDBM like MySQL. In comparison with another RDBM SQL Server, PostgreSQL has fewer native security features and thus is more vulnerable to attack. Compared with NoSQL such as MangoDB, PostgreSQL has a comparatively slower operation speed when inserting and updating queries. 
# R4 Key functionalities and benefits of an ORM
Object relational mapping (ORM) is a set of techniques that enables incompatible systems to cooperate, communicate, and exchange information. The ORM frameworks serve as a middle layer between object-oriented code and database operations, connecting both sides and facilitating communnication by converting data. ORMs perform tasks including adpating objects to database understandable forms, performing operations on both sides of the equation, creating virtual object database understandable by developers, and exposing a form of API so database operations could be performed at coding level. 

ORMs have many benefits: 
1. The automated conversion between object and table performed by ORM simplifies development, which greatly improves efficiency and reduces costs for development and maintanance. 
2. Compared to SQL or other ways to work with databases, ORM requires less and clearer code and enables developers to write in programming languages they are familiar with. 
3. ORM improves system performance by providing transparent chacing of objects on the client.
4. ORM abstract away the underlying database engine in terms of connectivity, making it flexible to work with different database systems. 

# R5 API endpoints documentation
## Authentication Routes
### Register an account
/auth/register/
- Methods: POST
- Arguments: None
- Description: register an account with personal details provided in request body and return account details.
- Authentication: None
- Sample URL: `http://127.0.0.1:5000/auth/register/`
- JSON Request Body: 
```json
{
    "email": "molly@email.com",
    "password": "Password123!",
    "phone_number": "0433333333",
    "first_name": "Dan",
    "last_name": "Mo"
}
```
- Sample Response:
```json
{
    "id": 3,
    "email": "molly@email.com",
    "first_name": "Dan",
    "last_name": "Mo",
    "phone_number": "0433333333",
    "products": []
}
```
### Login to an account
/auth/login/
- Methods: POST
- Arguments: None
- Description: login to an account with email and password (provided in request body) and create an access token for authentication. Return email and token.
- Authentication: None
- Sample URL: `http://127.0.0.1:5000/auth/login/`
- JSON Request Body: 
```json
{
    "email": "molly@email.com",
    "password": "Password123!"
}
```
- Sample Response:
```json
{
    "email": "molly@email.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODA3NzE2MSwianRpIjoiZTJkNTY4YzYtNDI4MC00Nzc1LTg2OTEtNmQ4ZmMyZWFkMWQwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjMiLCJuYmYiOjE2NjgwNzcxNjEsImV4cCI6MTY2ODE2MzU2MX0.BqYfc_vFvaHHeVnyp5eUdfv_TQ6_V6IZlZOrTmL6MTs"
}
```
## User Routes
### Get a list of all users
/users/
- Methods: GET
- Arguments: None
- Description: retrieve a list of all users
- Authentication: bearer token
- JSON Request Body: None
- Sample URL: `http://127.0.0.1:5000/users/`
- Sample Response:
```json
[
    {
        "id": 1,
        "email": "firstuser@email.com",
        "first_name": "Jimmy",
        "last_name": "OYang",
        "products": [
            {
                "id": 1,
                "name": "Apple iPhone 11",
                "description": "As new condition, 64GB, without contract.",
                "category": "Electronics",
                "price": 478.5,
                "quantity": 3
            },
            {
                "id": 2,
                "name": "Single Bunk Bed",
                "description": "Solid wooden bed frame, brand-new item in its original packaging; color: white; height: 152.2 cm.",
                "category": "Home",
                "price": 425.0,
                "quantity": 15
            }
        ]
    },
    {
        "id": 2,
        "email": "seconduser@email.com",
        "first_name": "Ali",
        "last_name": "Wong",
        "products": [
            {
                "id": 3,
                "name": "Mesh Beach Tote Bag",
                "description": "Lightweight bag made of Polyester, foldable and fast drying, perfect for travel.",
                "category": "Accessories",
                "price": 20.25,
                "quantity": 5
            },
            {
                "id": 4,
                "name": "Long Raincoat",
                "description": "Men waterproof black hooded trench jacket for outdoor hiking. Size L.",
                "category": "Clothing",
                "price": 24.0,
                "quantity": 2
            }
        ]
    },
    {
        "id": 3,
        "email": "molly@email.com",
        "first_name": "Dan",
        "last_name": "Mo",
        "products": []
    }
]
```
### Get a user
/users/{user_id}
- Methods: POST
- Arguments: user_id
- Description: retrieve a particular user with the user id
- Authentication: bearer token
- JSON Request Body: None
- Sample URL: `http://127.0.0.1:5000/users/1/`
- Sample Response:
```json
{
    "id": 1,
    "email": "firstuser@email.com",
    "first_name": "Jimmy",
    "last_name": "OYang",
    "products": [
        {
            "id": 1,
            "name": "Apple iPhone 11",
            "description": "As new condition, 64GB, without contract.",
            "category": "Electronics",
            "price": 478.5,
            "quantity": 3
        },
        {
            "id": 2,
            "name": "Single Bunk Bed",
            "description": "Solid wooden bed frame, brand-new item in its original packaging; color: white; height: 152.2 cm.",
            "category": "Home",
            "price": 425.0,
            "quantity": 15
        }
    ]
}
```
### Update user info
/users/update/
- Methods: PUT, PATCH
- Arguments: None
- Description: for users to update their own account information (provided in request body) and return user details.
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/users/update/`
- JSON Request Body: 
```json
{
    "email": "dan.mo@email.com"
}
```
- Sample Response:
```json
{
    "id": 3,
    "email": "dan.mo@email.com",
    "first_name": "Dan",
    "last_name": "Mo",
    "phone_number": "0433333333",
    "products": []
}
```
### Delete an account
/users/del_account/
- Methods: DELETE
- Arguments: None
- Description: for users to delete their own account and return a message.
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/users/del_account/`
- JSON Request Body: None
- Sample Response:
```json
{
    "message": "Account \"dan.mo@email.com\" deleted successfully."
}
```
## Address Routes
### Create an address
/addresses/new_addr
- Methods: POST
- Arguments: None
- Description: add a new address (details provided in request body) to account and return the new address.
- Authentication: None
- Sample URL: `http://127.0.0.1:5000/addresses/new_addr/`
- JSON Request Body: 
```json
{
    "street_number": "9",
    "street_name": "Bowen St.",
    "suburb": "Harrison",
    "postcode": "3444"
}
```
- Sample Response:
```json
{
    "id": 3,
    "street_number": "9",
    "street_name": "Bowen St.",
    "suburb": "Harrison",
    "postcode": "3444",
    "user_id": 4,
    "user": {
        "first_name": "Dan",
        "last_name": "Mo",
        "phone_number": "0433333333"
    }
}
```
### Get addresses
/addresses/
- Methods: GET
- Arguments: None
- Description: retrieve a list of addresses of the user
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/addresses/`
- JSON Request Body: None
- Sample Response:
```json
[
    {
        "id": 3,
        "street_number": "9",
        "street_name": "Bowen St.",
        "suburb": "Harrison",
        "postcode": "3444",
        "user_id": 4,
        "user": {
            "first_name": "Dan",
            "last_name": "Mo",
            "phone_number": "0433333333"
        }
    },
    {
        "id": 4,
        "street_number": "601",
        "street_name": "Wood Street",
        "suburb": "Turner",
        "postcode": "2000",
        "user_id": 4,
        "user": {
            "first_name": "Dan",
            "last_name": "Mo",
            "phone_number": "0433333333"
        }
    }
]
```
### Get a particular address
/addresses/{address_id}/
- Methods: GET
- Arguments: {address_id}
- Description: retrieve a paticular address with {address_id} of the user
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/addresses/3/`
- JSON Request Body: None
- Sample Response:
```json
[
    {
        "id": 3,
        "street_number": "9",
        "street_name": "Bowen St.",
        "suburb": "Harrison",
        "postcode": "3444",
        "user_id": 4,
        "user": {
            "first_name": "Dan",
            "last_name": "Mo",
            "phone_number": "0433333333"
        }
    }
]
```
### Update address
/addresses/{address_id}/update/
- Methods: PUT, PATCH
- Arguments: {address_id}
- Description: for users to edit an address with the {address_id} and return the address.
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/addresses/4/update`
- JSON Request Body: 
```json
{
    "street_number": "700",
    "street_name": "Jenbell Lane",
    "suburb": "Turner",
    "postcode": "2000"
}
```
- Sample Response:
```json
{
    "id": 3,
    "street_number": "700",
    "street_name": "Jenbell Lane",
    "suburb": "Turner",
    "postcode": "2000",
    "user_id": 4,
    "user": {
        "first_name": "Dan",
        "last_name": "Mo",
        "phone_number": "0433333333"
    }
}
```
### Delete an address
/addresses/{address_id}/del
- Methods: DELETE
- Arguments: {address_id}
- Description: delete user's address with the {address_id} and return a message.
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/addresses/3/del`
- JSON Request Body: None
- Sample Response:
```json
{
    "message": "Address 3 deleted successfully."
}
```
## Product Routes
### Create a product
/products/new_product/
- Methods: POST
- Arguments: None
- Description: for users to create a new product (details provided in request body)
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/products/new_product/`
- JSON Request Body: 
```json
{
    "name": "Sony In-ear Headphones",
    "description": "Model: MDRE9LP, Color: Blue, Connector Type: Wired",
    "category": "Electronics",
    "quantity": 1,
    "price": 5.5
}
```
- Sample Response:
```json
{
    "id": 5,
    "name": "Sony In-ear Headphones",
    "description": "Model: MDRE9LP, Color: Blue, Connector Type: Wired",
    "category": "Electronics",
    "price": 5.5,
    "quantity": 1,
    "user_id": 4,
    "user": {
        "first_name": "Dan",
        "last_name": "Mo"
    }
}
```
### Get all products
/products/
- Methods: GET
- Arguments: None
- Description: retrieve a list of all products
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/products/`
- JSON Request Body: None
- Sample Response:
```json
[
    {
        "id": 1,
        "name": "Apple iPhone 11",
        "description": "As new condition, 64GB, without contract.",
        "category": "Electronics",
        "price": 478.5,
        "quantity": 3,
        "user_id": 1,
        "user": {
            "first_name": "Jimmy",
            "last_name": "OYang"
        }
    },
    {
        "id": 2,
        "name": "Single Bunk Bed",
        "description": "Solid wooden bed frame, brand-new item in its original packaging; color: white; height: 152.2 cm.",
        "category": "Home",
        "price": 425.0,
        "quantity": 15,
        "user_id": 1,
        "user": {
            "first_name": "Jimmy",
            "last_name": "OYang"
        }
    },
    {
        "id": 3,
        "name": "Mesh Beach Tote Bag",
        "description": "Lightweight bag made of Polyester, foldable and fast drying, perfect for travel.",
        "category": "Accessories",
        "price": 20.25,
        "quantity": 5,
        "user_id": 2,
        "user": {
            "first_name": "Ali",
            "last_name": "Wong"
        }
    },
    {
        "id": 4,
        "name": "Long Raincoat",
        "description": "Men waterproof black hooded trench jacket for outdoor hiking. Size L.",
        "category": "Clothing",
        "price": 24.0,
        "quantity": 2,
        "user_id": 2,
        "user": {
            "first_name": "Ali",
            "last_name": "Wong"
        }
    },
    {
        "id": 5,
        "name": "Sony In-ear Headphones",
        "description": "Model: MDRE9LP, Color: Blue, Connector Type: Wired",
        "category": "Electronics",
        "price": 5.5,
        "quantity": 1,
        "user_id": 4,
        "user": {
            "first_name": "Dan",
            "last_name": "Mo"
        }
    }
]
```
### Filter products
/products/{category}/
- Methods: GET
- Arguments: {category}
- Description: retrieve a list of products in certain category {category}
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/products/Electronics/`
- JSON Request Body: None
- Sample Response:
```json
[
    {
        "id": 1,
        "name": "Apple iPhone 11",
        "description": "As new condition, 64GB, without contract.",
        "category": "Electronics",
        "price": 478.5,
        "quantity": 3,
        "user_id": 1,
        "user": {
            "first_name": "Jimmy",
            "last_name": "OYang"
        }
    },
    {
        "id": 5,
        "name": "Sony In-ear Headphones",
        "description": "Model: MDRE9LP, Color: Blue, Connector Type: Wired",
        "category": "Electronics",
        "price": 5.5,
        "quantity": 1,
        "user_id": 4,
        "user": {
            "first_name": "Dan",
            "last_name": "Mo"
        }
    }
]
```
### Get a particular product
/products/{product_id}
- Methods: GET
- Arguments: {product_id}
- Description: retrieve a particular product with the {product_id}
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/products/2/`
- JSON Request Body: None
- Sample Response:
```json
{
    "id": 2,
    "name": "Single Bunk Bed",
    "description": "Solid wooden bed frame, brand-new item in its original packaging; color: white; height: 152.2 cm.",
    "category": "Home",
    "price": 425.0,
    "quantity": 15,
    "user_id": 1,
    "user": {
        "first_name": "Jimmy",
        "last_name": "OYang"
    }
}
```
### Update product info
/products/{product_id}/update
- Methods: PUT, PATCH
- Arguments: {product_id}
- Description: update details (provided in request body) of a product posted by the user and return the product
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/products/5/update`
- JSON Request Body: 
```json
{
    "name": "Sony In-ear Headphones",
    "description": "Model: MDRE, Color: White, Connector Type: Wired",
    "price": 5
}
```
- Sample Response:
```json
{
    "id": 5,
    "name": "Sony In-ear Headphones",
    "description": "Model: MDRE, Color: White, Connector Type: Wired",
    "category": "Electronics",
    "price": 5.0,
    "quantity": 1,
    "user_id": 4,
    "user": {
        "first_name": "Dan",
        "last_name": "Mo"
    }
}
```
### Delete a product
/products/{product_id}/del
- Methods: DELETE
- Arguments: {product_id}
- Description: delete a product posted by the user and return a message.
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/products/5/del`
- JSON Request Body: None
- Sample Response:
```json
{
    "message": "Product \"Sony In-ear Headphones\" deleted successfully."
}
```
## Order Routes
### Create an order
/orders/new_order/
- Methods: POST
- Arguments: None
- Description: create a new order when the first product is selected (details provided in request body), and return the order.
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/orders/new_order/`
- JSON Request Body: 
```json
{
    "product_id": 3,
    "quantity": 2
}
```
- Sample Response:
```json
{
    "id": 3,
    "date": "2022-11-11",
    "user_id": 4,
    "user": {
        "first_name": "Dan",
        "last_name": "Mo"
    },
    "order_products": [
        {
            "product_id": 3,
            "product": {
                "name": "Mesh Beach Tote Bag"
            },
            "price": 20.25,
            "quantity": 2,
            "subtotal": 40.5
        }
    ],
    "total_payable": 40.5
}
```
### Add more products
/orders/{order_id}/add_product
- Methods: POST
- Arguments: {order_id}
- Description: add a product (details provided in request body) to an existing order and return the order
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/orders/3/add_product`
- JSON Request Body: 
```json
{
    "product_id": 4,
    "quantity": 1
}
```
- Sample Response:
```json
{
    "id": 3,
    "date": "2022-11-11",
    "user_id": 4,
    "user": {
        "first_name": "Dan",
        "last_name": "Mo"
    },
    "order_products": [
        {
            "product_id": 3,
            "product": {
                "name": "Mesh Beach Tote Bag"
            },
            "price": 20.25,
            "quantity": 2,
            "subtotal": 40.5
        },
        {
            "product_id": 4,
            "product": {
                "name": "Long Raincoat"
            },
            "price": 24.0,
            "quantity": 1,
            "subtotal": 24.0
        }
    ],
    "total_payable": 64.5
}
```
### Update an order
/orders/{order_id}/update
- Methods: PUT, PATCH
- Arguments: {order_id}
- Description: adjust quantity of a product (details provided in request body) added to an order and return the updated order
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/orders/3/update`
- JSON Request Body: 
```json
{
    "product_id": 3,
    "quantity": 1
}
```
- Sample Response:
```json
{
    "id": 3,
    "date": "2022-11-11",
    "user_id": 4,
    "user": {
        "first_name": "Dan",
        "last_name": "Mo"
    },
    "order_products": [
        {
            "product_id": 3,
            "product": {
                "name": "Mesh Beach Tote Bag"
            },
            "price": 20.25,
            "quantity": 1,
            "subtotal": 20.25
        },
        {
            "product_id": 4,
            "product": {
                "name": "Long Raincoat"
            },
            "price": 24.0,
            "quantity": 1,
            "subtotal": 24.0
        }
    ],
    "total_payable": 44.25
}
```
### Get orders
/orders/
- Methods: GET
- Arguments: None
- Description: retrieve a list of orders made by the user
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/orders/`
- JSON Request Body: None
- Sample Response:
```json
[
    {
        "id": 5,
        "date": "2022-11-11",
        "user_id": 4,
        "user": {
            "first_name": "Dan",
            "last_name": "Mo"
        },
        "order_products": [
            {
                "product_id": 2,
                "product": {
                    "name": "Single Bunk Bed"
                },
                "price": 425.0,
                "quantity": 1,
                "subtotal": 425.0
            }
        ],
        "total_payable": 425.0
    },
    {
        "id": 3,
        "date": "2022-11-11",
        "user_id": 4,
        "user": {
            "first_name": "Dan",
            "last_name": "Mo"
        },
        "order_products": [
            {
                "product_id": 3,
                "product": {
                    "name": "Mesh Beach Tote Bag"
                },
                "price": 20.25,
                "quantity": 1,
                "subtotal": 20.25
            },
            {
                "product_id": 4,
                "product": {
                    "name": "Long Raincoat"
                },
                "price": 24.0,
                "quantity": 1,
                "subtotal": 24.0
            }
        ],
        "total_payable": 44.25
    }
]
```
### Get an order
/orders/{order_id}/
- Methods: GET
- Arguments: {order_id}
- Description: retrieve user's order with {order_id}
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/orders/5/`
- JSON Request Body: None
- Sample Response:
```json
{
    "id": 5,
    "date": "2022-11-11",
    "user_id": 4,
    "user": {
        "first_name": "Dan",
        "last_name": "Mo"
    },
    "order_products": [
        {
            "product_id": 2,
            "product": {
                "name": "Single Bunk Bed"
            },
            "price": 425.0,
            "quantity": 1,
            "subtotal": 425.0
        }
    ],
    "total_payable": 425.0
}
```
### Delete order_product
/orders/{order_id}/del_product/
- Methods: DELETE
- Arguments: {order_id}
- Description: delete a selected product from an order with id {order_id} and return the order
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/orders/3/del_product`
- JSON Request Body: 
```json
{
    "product_id": 4
}
```
- Sample Response:
```json
{
    "id": 3,
    "date": "2022-11-11",
    "user_id": 4,
    "user": {
        "first_name": "Dan",
        "last_name": "Mo"
    },
    "order_products": [
        {
            "product_id": 3,
            "product": {
                "name": "Mesh Beach Tote Bag"
            },
            "price": 20.25,
            "quantity": 1,
            "subtotal": 20.25
        }
    ],
    "total_payable": 20.25
}
```
### Delete an order
/orders/{order_id}/del
- Methods: DELETE
- Arguments: {order_id}
- Description: delete an order history with {order_id} of the user and return a message.
- Authentication: bearer token
- Sample URL: `http://127.0.0.1:5000/orders/3/del`
- JSON Request Body: None
- Sample Response:
```json
{
    "message": "Order 3 deleted successfully."
}
```

# R6 ERD
![ERD](docs/ERD3.drawio%20(1).png)

# R7 Third party services
This application uses the following PyPI packages:
- Flask: Flask is a lightweight web application framework written in Python. Flask is based on the Werkzeg WSGI toolkit and the Jinja2 template engine. It features simple and scalable core and quick and easy start for development.
- Flask-SQLAlchemy: Flask-SQLAlchemy is an extension that supports and simplifies the use of SQLAlchemy with Flask. It provides user defaults and sets up common objects and patterns for the use of the objects.
- psycopg2: Psycopg is the most popular and advanced PostgreSQL adapter for Python. It is designed for heavily multithreaded applications that make bulk inserting or update concurrently. 
- Flask-Marshmallow: Flask-Marshmallow is a thin integration layer for Flask and marshmallow, the object serialisation and deserialisation library. It adds additional features to marshmallow and could integrates with Flask-SQLAlchemy.
- Flask-bcrypt: Flask-Bcrypt is a Flask extension that provides bcrypt hashing utilities for applications. Bcrypt is intentionally structured to be slow, making the hash harder to crack. It could be used to has sensitive data such as password in this application.
- flask-jwt-extended: Flask-JWT-Extended supports the use of JSON Web Tokens (JWT) in order to protect routes. It also supports many features that makes it easier to work with JWT. 
- python-dotenv: Python-dotenv helps set environment variables using the key-value pairs read from a .env file, avoid hard-coding variables like access credentials into code.

# R8 Project models
The project has five models: User, Address, Product, Order, and OrderPoduct. 

The addresses has a many optional to one mandatory relationship with the users, and thus a user_id field is defined as a foreign key in the Address model to associate Address with User. Relationship with the User model is also declared in the Address model. UserSchema has the 'first_name', 'last_name', and 'phone_number' fields nested in the AddressSchema.

The products also has a many optional to one mandatory relationship with the users. A user_id field is set as a foreign key in the Product model to to associate Product with User. Bidirectional behaviour is achieved by defining relationship with back_populates parameter used in definition of both models. Two fields of the UserSchema, 'first_name' and 'last_name' are nested in the ProductSchema and the ProductSchema is also nested in the UserSchema.

The orders has a many optional to one mandatory relationship with the users, and thus a user_id field is defined as a foreign key in the Order model referencing the users. Relationship with the User model is also declared in the Order model. UserSchema has the 'first_name' and 'last_name' fields nested in the OrderSchema. 

The relationship between products and order_products is one manditory to many optional. product_id field is set as a foreign key in the OrderProduct model referencing the products. Bidirectional behaviour is achieved by defining relationship with back_populates parameter used in definition of both Product and OrderProduct models. The 'name' field of the ProductSchema is nested in the OrderProductSchema.

The relationship between orders and order-products is a one manditory to many manditory. order_id field is set as a foreign key in the OrderProduct model to reference the orders. Bidirectional behaviour is achieved by declaring relationship with back_populates parameter used in definition of both Order and OrderProduct models. The list of OrderProductSchema excluding 'order_id' field is nested in the OrderSchema.
# R9 Database relations
There are five tables stored in the database: users, addresses, products, orders, and order_products. All tables except the order_products have an id column as a primary key that cannot be null. The users table has one mandatory to many optional relationships with three tables: the addresses table, the products table, and the orders table. This means not all users have an address, a product for sale, or an order, but for each row of address, product, or order record there must be a connected user. Thus all these related tables have the user_id as a not-null foreign key column with cascade delete. 

The relationship between products table and orders table is many to many, as a product can be in many orders and an order can have many products. Many to many relationship can't be dealt with by the relational database system, so a joining table order_products is created. The relationship between products and order_products is one manditory to many optional, because a product can be in many or none order_product record, but for each row of the order_products table there must be a product. The relationship between orders and order_products is one manditory to many manditory, as in each order there is at least one record of order_product. The order_products has a composite primary key consist of two foreign keys: product_id and order_id. 

# R10 Task allocation and tracking
This project is managed using [trello](https://trello.com/b/FfH4RHHD/t2a2-ecommerce-app). There are three columns on the trello board: To Do, Doing, and Done. The user stories that determines the functions to develop are recorded in the task cards each broken down into a checklist of model methods to be used to query database. Other steps of the development are also written in the card. All cards are labelled and sequenced based on their level of priority and estimated workload, and deadlines are set. All cards locate in the column To Do at the beginning of the project. When I start to work on the task on some cards, they are moved from To DO to Doing column, and once the tasks are done, the cards are dragged into the Done column. Tracking the tasks progressing from To Do to Done in the development process makes the tasks more organised and give me a clearer idea of what should be done first and how long I should spend on each task. 

![trello](docs/trello.png)

# How to run the app
1. clone the repo from Github
```
git clone git@github.com:Dandandan-mo/T2A2-API-Webserver-Project.git
```
2. change into the directory of the application in the terminal
3. create and activate a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

4. install all the packages in the requirements.txt
```
pip install -r requirements.txt
```
5. fill in the environment variables (DATABASE URL and JWT SECRET KEY) in the '.env.sample' file and change the file name into '.env'.
6. drop, create, and seed table
```
flask db drop
flask db create
flask db seed
```
7. run the app
```
flask run
```
8. send the url (http://127.0.0.1:5000) in Postman and follow the API endpoint documentation above in  R5 to use all functions.
