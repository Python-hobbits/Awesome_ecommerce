# Awesome e-commerce

Let me speak from the bottle of my heart

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)

## Overview

Here we're going to do awesome e-commerce

## Features

- The best is yet to come
    
## Prerequisites

Make sure you have the following software installed on your machine:

- Docker
- Docker Compose

## Getting Started

1. Clone the repository to your local machine:
    ```bash
    git clone git@github.com:Python-hobbits/Awesome_ecommerce.git    
    ```
   
2. Create an .env file in the root directory of your project with the following content. Replace the values with your desired settings:

   `POSTGRES_DB` = postgres
   
   `POSTGRES_USER` = postgres
   
   `POSTGRES_PASSWORD` = password
   
   `SECRET_KEY` = your-secret-key

   `DB_HOST` = db

   **For local development remove `DB_HOST` from .env file**

3. Open a terminal and navigate to your project's directory.

4. Build the Docker images by running:
    ```bash
    docker-compose build  
    ```

5. Start the Docker containers:
    ```bash
    docker-compose up
    ```
   This will start the Django development server, database, and any other services defined in the docker-compose.yml file.

6. Access the application:
Open your web browser or Postman and navigate to http://localhost:8000/ or http://0.0.0.0:8000/.

7. When you're done, stop the containers by pressing Ctrl + C in the terminal where you started them. To remove the containers and associated resources, run:
    ```bash
    docker-compose down --volumes
    ```