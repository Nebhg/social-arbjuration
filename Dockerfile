FROM python:3.8

# Copy only what you need to run the application
# It's a good practice to be selective with what you COPY to reduce build context size
COPY requirements.txt /app/
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of your application code
COPY . /app

# This CMD command can be overridden by docker-compose or docker run commands
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
