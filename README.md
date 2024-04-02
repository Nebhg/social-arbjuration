# Social Arbjuration FastAPI & Selenium Project

This project demonstrates the use of FastAPI and Selenium within Docker containers for web scraping tasks. It's structured to allow for easy development and deployment, leveraging Docker Compose for service orchestration.

## Project Structure

- `app/`: Contains the FastAPI application code.
  - `base_scraper.py`: Module for initialising selenium chrome web driver.
  - `generic_url_scraper.py`: Tries to grab the body of a url, for pages with js this doesent really work
  - `google_trends_scraper.py`: Currently this grabs the data for intrest of time over the last 30 days world wide for 1 search term on Google Trends (plans to extend this to concurrent scarping of multiple terms)
  - `google_search_scraper.py`: Currently grabs the organic search results from Google SERP (plans to extend this to ads, related queries, parametrise number of results)
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
    -For ease of use utilise the pre-exisitng dev-container files by pressing CTRL + SFHT + P
    Search for reopen in container and press ENTER
    - This should build the docker container and everything should now be ready to use

3. **Usage**
   -Ensure all ports are fordwarded so the dev container can interact with the host machine.
   - For the FastAPI open port 8000
   -To run the API Enter this command in the terminal 
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
   - Thats it! You should now be able to ineract with the API. Please refer to thhe Postman workspace to see the list of availible request methods


Contributions to the project are welcome! Please follow the standard fork and pull request workflow. If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.
