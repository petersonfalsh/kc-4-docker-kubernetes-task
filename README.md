

# Simple Web Application Deployment with Docker and Kubernetes

This project demonstrates how to create a simple web application using Python, containerize it with Docker, and deploy it to a Kubernetes cluster.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Application Setup](#application-setup)
- [Dockerization](#dockerization)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Testing the Deployment](#testing-the-deployment)
- [ConfigMap and Secret (Optional)](#configmap-and-secret-optional)
- [Challenges Faced](#challenges-faced)
- [Screenshots](#screenshots)

## Prerequisites

Before you begin, ensure you have the following installed:

- Docker
- Kubernetes (Minikube for local testing)
- kubectl
- Git

## Application Setup

1. Create a simple web application using Python.

```python
# app.py
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    message = os.getenv('WELCOME_MESSAGE', 'Hello, Welcome to KodeCamp DevOps Bootcamp!')
    return f"<h1>{message}</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

## Dockerization

1. Create a `Dockerfile` to containerize the application.

```Dockerfile
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

# Define Environment Variable. (optional)
ENV MESSAGE "Hello Default!"

# Run app.py when the container launches
CMD ["python", "app.py"]
```

2. Build the Docker image and tag it.

```bash
docker build -t simple-web-app .
docker tag simple-web-app YOUR_DOCKERHUB_USERNAME/simple-web-app:latest
```

![Docker build start](screenshots/docker%20build%20-%201.PNG)
![Docker build completed](screenshots/docker%20build%20-%203.PNG)



3. Push the Docker image to Docker Hub.

```bash
docker login
docker push YOUR_DOCKERHUB_USERNAME/simple-web-app:latest
```
![Docker login to enable me push to dockerhub](screenshots/docker%20login%20-%206.PNG)
![Docker push - to push to dockerhub](screenshots/Docker%20hub%20push.PNG)
![Dcoker image pushed to my dockerhub account](screenshots/docker%20-%20image%20now%20pushed%20to%20dockerhub%20-%207.PNG)


4. My docker image URL from Docker hub is: ![myDockerImageURL](https://hub.docker.com/layers/petersonfalsh/simple-web-app/latest/images/sha256-584572105282f54d511820708d3244d26a8708b6d0c5b561de20828353b280e0?context=repo)


5. Running container can be viewed from my browser - 
![Check the docker container running and working app through the browser](screenshots/docker%20-%20container%20running%20at%20port%204000%20-%20web%20browser.PNG)


## Kubernetes Deployment

1. Create a deployment manifest file (`deployment.yaml`).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: simple-web-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: simple-web-app
  template:
    metadata:
      labels:
        app: simple-web-app
    spec:
      containers:
        - name: simple-web-app
          image: YOUR_DOCKERHUB_USERNAME/simple-web-app:latest
          ports:
            - containerPort: 80
```

2. Create a service manifest file (`service.yaml`).

```yaml
apiVersion: v1
kind: Service
metadata:
  name: simple-web-app-service
spec:
  selector:
    app: simple-web-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP
```

3. Apply the Kubernetes manifests.

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

![Kubernetes manifest file applied - deployment file applied](screenshots/kubernetes%20deployment%20-%20watching.PNG)

![Kubernetes pods - running pods from 2 replicas in my deployment file](screenshots/kubernetes%20deployment%20-%20container%20running.PNG)


## Testing the Deployment

1. Port-forward the service to a local port and access it via a web browser.

```bash
kubectl port-forward service/simple-web-app-service 8080:80
```

Access the application at `http://localhost:8080`.


![Application deployed on Kubernetes cluster - view on web browser when port forwaded using the service.yaml file](screenshots/Kubernets%20deployment%20-%20deployment%20port%20forwarded%20and%20can%20be%20viewd%20in%20the%20browser.PNG)


## ConfigMap and Secret (Optional)


### ConfigMap

1. Create a `ConfigMap` to externalize the message.

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  MESSAGE: "Hello, Kubernetes!"
```

2. Update the application to read the message from the environment variable.

```python
# app.py
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    message = os.getenv('MESSAGE', 'Hello, Default!')
    return f"<h1>{message}</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

3. Update the deployment to use the `ConfigMap`.

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: simple-web-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: simple-web-app
  template:
    metadata:
      labels:
        app: simple-web-app
    spec:
      containers:
        - name: simple-web-app
          image: YOUR_DOCKERHUB_USERNAME/simple-web-app:latest
          ports:
            - containerPort: 80
          env:
            - name: MESSAGE
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: MESSAGE
```

4. Apply the `ConfigMap`.

```bash
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
```

### Secret

This was not done in my project because it's just a simple application that doesn't require password or any API key but if your applications does, this is how to go about it:

1. Create a `Secret` to store sensitive information.

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
data:
  PASSWORD: <base64_encoded_password>
```

2. Update the application to read the secret.

```python
# app.py
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    message = os.getenv('MESSAGE', 'Hello, Default!')
    password = os.getenv('PASSWORD', 'No Password')
    return f"<h1>{message}</h1><p>Password: {password}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

3. Update the deployment to use the `Secret`.

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: simple-web-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: simple-web-app
  template:
    metadata:
      labels:
        app: simple-web-app
    spec:
      containers:
        - name: simple-web-app
          image: YOUR_DOCKERHUB_USERNAME/simple-web-app:latest
          ports:
            - containerPort: 80
          env:
            - name: MESSAGE
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: MESSAGE
            - name: PASSWORD
              valueFrom:
                secretKeyRef:
                  name: app-secret
                  key: PASSWORD
```

4. Apply the `Secret`.

```bash
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
```

## Challenges Faced
The major challenge I faced is when I applied my configuration file, I got the error:
1. **Image Pull Backoff**: The Kubernetes pods were in an `ImagePullBackoff` state because the Docker image was not correctly tagged with `latest`. Adding `:latest` to the image tag resolved this issue.


## Screenshots

My working screenshots are here below:

![Docker build start](/screenshots/docker%20build%20-%201.PNG)

![Docker build completed](/screenshots/docker%20build%20-%203.PNG)

![Docker run screenshot to containerize the application](/screenshots/Docker%20run%20image%20as%20container%20-%205.PNG)

![Docker login to enable me push to dockerhub](screenshots/docker%20login%20-%206.PNG)

![Docker push - to push to dockerhub](screenshots/Docker%20hub%20push.PNG)

![Docker image pushed to my dockerhub account](screenshots/docker%20-%20image%20now%20pushed%20to%20dockerhub%20-%207.PNG)

![Check the docker container running and working app through the browser](screenshots/docker%20-%20container%20running%20at%20port%204000%20-%20web%20browser.PNG)

![Kubernetes manifest file applied - deployment file applied](screenshots/kubernetes%20deployment%20-%20watching.PNG)

![Kubernetes pods - running pods from 2 replicas in my deployment file](screenshots/kubernetes%20deployment%20-%20container%20running.PNG)


![Application deployed on Kubernetes cluster - view on web browser when port forwaded using the service.yaml file](screenshots/Kubernets%20deployment%20-%20deployment%20port%20forwarded%20and%20can%20be%20viewd%20in%20the%20browser.PNG)


## Conclusion

This project demonstrates the process of containerizing a simple web application using Docker and deploying it to a Kubernetes cluster. And optionally Using `ConfigMap` and `Secret` enhances configuration management and security, making the application more flexible and secure.

## Author

Petersonfalsh - Current KodeCamp Bootcamp student as at when this project is pushed - August 2024
```
```
# Simple Web Application Deployment with Docker and Kubernetes

## Screenshots

![Docker container running at port 4000 - web browser view](screenshots/docker%20-%20container%20running%20at%20port%204000%20-%20web%20browser.PNG)

![Image now pushed to Docker Hub](screenshots/docker%20-%20image%20now%20pushed%20to%20dockerhub%20-%207.PNG)

![Check the docker container running and working app through the browser](screenshots/docker%20-%20container%20running%20at%20port%204000%20-%20web%20browser.PNG)

![Kubernetes manifest file applied - deployment file applied](screenshots/kubernetes%20deployment%20-%20watching.PNG)

![Kubernetes pods - running pods from 2 replicas in my deployment file](screenshots/kubernetes%20deployment%20-%20container%20running.PNG)

![Application deployed on Kubernetes cluster - view on web browser when port forwarded using the service.yaml file](screenshots/Kubernets%20deployment%20-%20deployment%20port%20forwarded%20and%20can%20be%20viewed%20in%20the%20browser.PNG)

## Conclusion

This project demonstrates the process of containerizing a simple web application using Docker and deploying it to a Kubernetes cluster. And optionally Using `ConfigMap` and `Secret` enhances configuration management and security, making the application more flexible and secure.

## Author

Petersonfalsh - Current KodeCamp Bootcamp student as at when this project is pushed - August 2024
```
