# DoodleRecognitionAPI
Doodle Recognition API

# Git commands to intialize and create repo on GitHub:

- git init
- gh repo create
- git remote -v
- git add .
- git commit -m "Initial commit"
- git push origin master

# Docker commands to create docker image and run container:

- sudo service docker start
- sudo docker build --tag=doodle-recognition-api .
- sudo docker images
- sudo docker run -e PORT=8000 -p 8000:8000 doodle-recognition-api
- ...
- sudo docker run -it -e PORT=8000 -p 8000:8000 doodle-recognition-api sh
- sudo docker ps
- sudo docker stop CONTAINER ID
- sudo docker kill CONTAINER ID 

# Gcloud commands to push and run docker container on GCP:
- sudo gcloud auth login
- sudo gcloud auth list
- sudo gcloud config set project doodlerecognition-307108
- sudo gcloud config list
- export PROJECT_ID=doodlerecognition-307108
- gcloud config set project $PROJECT_ID
- export DOCKER_IMAGE_NAME=doodle-recognition-api
- sudo docker build -t eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME .
- sudo docker run -e PORT=8000 -p 8000:8000 eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME # Let’s make sure that our image runs correctly
- sudo usermod -a -G docker ${USER}
- sudo gcloud docker -- push eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME
- sudo gcloud run deploy --image eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME --platform managed --region europe-west1
