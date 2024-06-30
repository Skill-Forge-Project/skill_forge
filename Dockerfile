# Use the base image containing Python 3.8, NodeJS, npm, mono-complete compiler and java compiler
FROM karastoyanov/skill-forge-baseimage

# Image Labels. Update values for each build
LABEL Name="Skill-Forge"
LABEL Version=1.3.8
LABEL Release="pre-release"
LABEL ReleaseDate="30.06-2024"
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

# Install the node modules
RUN npm install

# Buld the dependencies
RUN npm run build

# Expose port 5000
EXPOSE 5000

# Run the Python app
CMD ["python", "run.py"]
