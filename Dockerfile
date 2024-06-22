# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variables
ENV TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
ENV OMDB_API_KEY=YOUR_OMDB_API_KEY

# Run movie_bot.py when the container launches
CMD ["python", "./movie_bot.py"]
