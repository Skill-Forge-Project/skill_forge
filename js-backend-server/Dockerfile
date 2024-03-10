# This image should provide the javascript backend server to run the unit tests for the JS quests

# Get node image from docker hub
FROM node:14

# Set the working directory
WORKDIR /app

# Copy the local server to the image
COPY server.js .

# Open port 3000
EXPOSE 3000

# Install express library
RUN npm install express

# Install Jtest
RUN npm install jtest
RUN npm install jest-cli

# Run the server
CMD ["node", "server.js"]