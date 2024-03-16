# Pull the Python image from Docker Hub
FROM python:latest

# Copy the Python app requirements file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Set the working directory in the container
WORKDIR /app

# Install the Python app requirements
RUN pip install -r requirements.txt --no-cache

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 5000
EXPOSE 5000

# Configure the container to run as an executable
ENTRYPOINT ["python"]

# Run the Python app
CMD ["app.py"]