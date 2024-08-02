#using a python image from dockerhub that is light weight
FROM python:3-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory content into the container at /app
COPY . /app

# Install any needed packages sepcified in the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define Environment Variable. I didn't really use this though
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]