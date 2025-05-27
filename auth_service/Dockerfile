FROM python:3.12.7

# Image Labels. Update values for each build
LABEL Name "Skill Forge Authentication Service"
LABEL Version "1.0.0"
LABEL Release "public"
LABEL ReleaseDate ""
LABEL Description "Skill Forge is a open-source platform for learning and practicing programming languages."
LABEL Maintainer "Aleksandar Karastoyanov <karastoqnov.alexadar@gmail.com>"
LABEL License "GNU GPL v3.0 license"
LABEL GitHub SourceCode "https://github.com/SoftUni-Discord-Community/skill_forge"

# Update repositories list
RUN apt update

# Set default timezone
ENV TZ=Europe/Sofia
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \ 
    && dpkg-reconfigure -f noninteractive tzdata

# Set the workdir
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the Python app requirements file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install the Python app requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache 

# Expose port 8000
EXPOSE 8001

# Run the Python app
CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:8001", "wsgi:app"]