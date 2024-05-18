# Pull the Python image from Docker Hub
FROM python:latest

# Image Labels. Update values for each build
LABEL Name="skill-forge"
LABEL Version=1.3.2
LABEL Release="pre-release"
LABEL ReleaseDate="18-05-2024"
LABEL Description="Skill Forge is a open-source platform for learning and practicing programming languages."
LABEL Maintainer="Aleksandar Karastoyanov <karastoqnov.alexadar@gmail.com>"
LABEL License="GPL-3.0 license"
LABEL GitHub SourceCode="https://github.com/SoftUni-Discord-Community/skill_forge"



# Copy the Python app requirements file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the Python app requirements
RUN pip install -r requirements.txt --no-cache

# Install NodeJS interpreter, Mono runtime and OpenJDK 17 compilers
RUN apt update && apt install nodejs mono-complete openjdk-17-jdk-headless -y

# Expose port 5000
EXPOSE 5000

# Configure the container to run as an executable
ENTRYPOINT ["python"]

# Run the Python app
CMD ["app.py"]