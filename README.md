# Awesome e-commerce

This project is an e-commerce platform designed to facilitate online buying and selling. It provides a user-friendly interface for customers to browse products, add them to their cart, and securely complete their purchases. Sellers can manage their product listings, inventory, and sales through a dedicated dashboard.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)

## Overview

Here we're going to do awesome e-commerce

## Features

- User Authentication: Secure user registration and login system.
- Product Catalog: Browse and search a wide range of products with detailed descriptions.
- Shopping Cart: Add, remove, and manage items in the shopping cart.
- Checkout Process: Secure and intuitive process for completing purchases.
- Order Management: Users can view their order history and check the status of their orders.
- Seller Dashboard: Sellers can manage their product listings, view sales, and handle inventory.

## Prerequisites

Make sure you have the following software installed on your machine:

- Docker
- Docker Compose

## Getting Started

1. Clone the repository to your local machine:
    ```bash
    git clone git@github.com:Python-hobbits/Awesome_ecommerce.git
    ```
2. Install all dependencies
    ```bash
    poetry install
    ```
3. Install pre-commit
   ```bash
    pre-commit install
    ```
4. Create an .env file in the root directory of your project with the following content. Replace the values with your desired settings:

   `POSTGRES_DB` = postgres

   `POSTGRES_USER` = postgres

   `POSTGRES_PASSWORD` = password

   `SECRET_KEY` = your-secret-key

   `DB_HOST` = db

   `REDIS_CACHE_DB` = 0

   `REDIS_CACHE_HOST` = localhost (for Win)

   `REDIS_CACHE_HOST` = docker.for.mac.localhost (for Mac)

   `REDIS_CACHE_PORT` = 6379

   `MINIO_ENDPOINT` = http://127.0.0.1:9000

   `MINIO_ROOT_USER` = minioadmin

   `MINIO_ROOT_PASSWORD` = minioadmin

   `MINIO_BUCKET_NAME` = photos

   **For local development remove `DB_HOST` from .env file**

5. Open a terminal and navigate to your project's directory.

6. Build the Docker images by running:
    ```bash
    docker-compose build
    ```

7. Start the Docker containers:
    ```bash
    docker-compose up
    ```
   This will start the Django development server, database, and any other services defined in the docker-compose.yml file.

8. Access the application:
Open your web browser or Postman and navigate to http://localhost:8000/ or http://0.0.0.0:8000/.

9. When you're done, stop the containers by pressing Ctrl + C in the terminal where you started them. To remove the containers and associated resources, run:
    ```bash
    docker-compose down --volumes
    ```
