# Challenge Globant

This repository contains the solution to the challenge, implemented with a **frontend** and **backend** architecture.

## Description

The application consists of two parts:

- **Backend:** Developed in Python using **FastAPI** and **PostgreSQL** as the database.
- **Frontend:** Developed in **Vue.js** for the user interface.

The goal of this project is to demonstrate the integration between a RESTful API (FastAPI) and an interactive web application (Vue.js).

## Technologies Used

- **Backend:**
  - [FastAPI](https://fastapi.tiangolo.com/)
  - Python 3.8+
  - [PostgreSQL](https://www.postgresql.org/)
  - SQLAlchemy (or any ORM of your preference)
- **Frontend:**
  - [Vue.js](https://vuejs.org/)
  - Vuetify (if you use Material Design components)
- **Containerization:**
  - Docker

## Requirements

- [Python](https://www.python.org/downloads/) (version 3.8 or higher)
- [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/) or [yarn]
- [Docker](https://www.docker.com/) (optional, for containerized execution)
- PostgreSQL (for local development, or you can use Docker)

## Installation and Setup

### BACKEND

1. Clone the Repository

git clone https://github.com/franciscolozano01/challenge-globant.git
cd challenge-globant

2. Create and Activate a Virtual Environment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install Dependencies

pip install -r requirements.txt
4. Configure the Database

Set your database connection by defining the environment variable. For example, create a .env file or export the variable in your shell:

DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@IP:PORT/DATABASE
5. Run the Application

uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
The API will be available at http://localhost:8080.

### FRONTEND
1. Install Dependencies

Navigate to the frontend directory and run:

npm install
npm run serve
Optionally, install Vuetify for styling if needed.

2. Docker Setup Example

Below is an example of a docker-compose.yml file to run both the backend and frontend with Docker:

version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql+psycopg2://postgres:admin@db:5432/postgres
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend

  db:
    image: postgres
    restart: always
    environment:
      POSTGRES_USER: USER
      POSTGRES_PASSWORD: PASSWORD
      POSTGRES_DB: DATABASE
    ports:
      - "5433:5432"
To start the containers, run:

docker-compose up --build
Project Structure

The general structure of the project is as follows:

challenge-globant/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routes/
│   │   └── ... 
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   └── ...
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
Endpoints

The following endpoints have been implemented:

DELETE: To delete data from the tables.
GET: To retrieve data from the tables.
GET: To retrieve query 01 from section 2.
GET: To retrieve query 02 from section 2.
POST: To load a file into the database.
Contact

If you have any questions or suggestions, please contact franciscolozano001@gmail.com.


Feel free to adjust any section to fit your project specifics. This README provides a comprehensive guide for developers and users on how to set up, run, and understand the project.
