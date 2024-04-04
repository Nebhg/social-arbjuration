FROM python:3.8

# Copy only what you need to run the application
# It's a good practice to be selective with what you COPY to reduce build context size
COPY requirements.txt /app/
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Install Redis CLI
RUN apt-get update && \
    apt-get install -y redis-tools
# Copy the rest of your application code
COPY . /app
