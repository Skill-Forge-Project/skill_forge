# This image should provide the javascript backend server to run the unit tests for the JS quests

# Get node image from docker hub
FROM node:14

# Set the working directory
WORKDIR /app

# Copy the local server to the image
COPY . .

# Open port 3000
EXPOSE 3000

# Install dependencies
RUN npm install body-parser chai mocha node-fetch express

# Run the server
CMD ["node", "server.js"]