# SHL_AI

An AI-powered backend service built with **FastAPI** that processes SHL assessment data and exposes API endpoints for querying and interacting with the application.

## Features

* FastAPI-based REST API
* AI-powered processing
* Docker support
* Environment variable configuration
* Ready for deployment on Render

## Project Structure

```text
.
├── agent.py
├── catalog.json
├── Dockerfile
├── main.py
├── requirements.txt
├── scraper.py
├── .env.example
└── README.md
```

## Prerequisites

* Python 3.10 or later
* pip
* Git
* Docker (optional)

## Installation

Clone the repository:

```bash
git clone https://github.com/prashu2912/SHL_AI.git
cd SHL_AI/backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file using the provided template:

```bash
cp .env.example .env
```

Fill in all required environment variables before running the application.

## Running Locally

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive API documentation:

* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`

## Running with Docker

Build the Docker image:

```bash
docker build -t shl_ai .
```

Run the container:

```bash
docker run -p 8000:8000 shl_ai
```

## Deployment on Render

1. Push your latest code to GitHub.
2. Create a new **Web Service** on Render.
3. Connect your GitHub repository.
4. If your backend is inside the `backend` directory, set the **Root Directory** to:

```text
backend
```

5. Deploy the service.

Once deployed, your API will be available at your Render URL.

## API Endpoints

| Method | Endpoint | Description                    |
| ------ | -------- | ------------------------------ |
| GET    | `/`      | Health check / Welcome message |
| GET    | `/docs`  | Swagger API documentation      |
| GET    | `/redoc` | ReDoc API documentation        |

Additional endpoints are defined in `main.py`.

## Tech Stack

* Python
* FastAPI
* Uvicorn
* Docker
* Render

## Repository

GitHub:

https://github.com/prashu2912/SHL_AI

## License

This project is intended for educational and learning purposes.
