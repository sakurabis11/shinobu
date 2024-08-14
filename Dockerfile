# Use a lightweight Python base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your bot will listen on (if applicable)
EXPOSE 8080  # Replace with the actual port

# Command to run your bot
CMD ["python", "bot.py"]
