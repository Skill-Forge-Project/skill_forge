# Use the base image containing Python 3.8, NodeJS, npm, mono-complete compiler and java compiler
FROM karastoyanov/skill-forge-baseimage

# Image Labels. Update values for each build
LABEL Name="Skill-Forge"
LABEL Version=1.3.16
LABEL Release="pre-release"
LABEL ReleaseDate="15.09.2024"
LABEL Description="Skill Forge is a open-source platform for learning and practicing programming languages."
LABEL Maintainer="Aleksandar Karastoyanov <karastoqnov.alexadar@gmail.com>"
LABEL License="GNU GPL v3.0 license"
LABEL GitHub SourceCode="https://github.com/SoftUni-Discord-Community/skill_forge"

# Set the working directory in the container
WORKDIR /app

# Copy the Python app requirements file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install the Python app requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache 

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8000
EXPOSE 8000

# Run the Python app
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:8000", "wsgi:app"]
