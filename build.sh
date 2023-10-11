cd frontend
docker build -t sheep-frontend .
docker image tag sheep-frontend mreider/sheep-frontend:latest
docker image push mreider/sheep-frontend:latest
cd ../backend
docker build -t sheep-backend .
docker image tag sheep-backend mreider/sheep-backend:latest
docker image push mreider/sheep-backend:latest
cd ../generator
docker build -t sheep-generator .
docker image tag sheep-generator  mreider/sheep-generator:latest
docker image push mreider/sheep-generator:latest

