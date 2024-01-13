# Use the official Python image as a base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt


# Copy the bot code into the container at /app
COPY . /app/

# Set environment variable for Discord bot token
ENV TOKEN <>

# Expose the port the app runs on
EXPOSE 80

# Run the application
CMD ["python3", "main.py"]
