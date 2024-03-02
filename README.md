# Social Arbjuration FastAPI & Selenium Project

This project demonstrates the use of FastAPI and Selenium within Docker containers for web scraping tasks. It's structured to allow for easy development and deployment, leveraging Docker Compose for service orchestration.

## Project Structure

- `app/`: Contains the FastAPI application code.
  - `scraper.py`: Module for web scraping logic using Selenium.
  - `main.py`: FastAPI app initialization and API route definitions.
- `Dockerfile`: Instructions for building the FastAPI application Docker image.
- `docker-compose.yml`: Defines the services, networks, and volumes for running the application and Selenium server in Docker.
- `requirements.txt`: Lists the Python package dependencies for the application.

## Prerequisites

- Docker: Ensure Docker and Docker Compose are installed on your system. For Windows users, Docker Desktop is recommended.
- WSL (Windows Subsystem for Linux): Recommended for Windows users to manage Docker and project files.

## Setup & Installation

1. **Clone the Repository**
   ```bash
   git clone https://social-arbjuration
   cd social-arbjuration
2. **Build and Run with Docker Compose**
    ```bash
    docker-compose up --build

3. **Usage**
   http://localhost/scrape?url=https://example.com


Contributions to the project are welcome! Please follow the standard fork and pull request workflow. If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.
