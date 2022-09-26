# titanic_k8s
Repository to test the deployment of a docker image to AKS

## 0. Prerequsites
To run this tutorial you need to have 
- Docker Desktop running locally
- a Bash shell that has the Azure CLI and kubectl installed
- an Azure Subscription

## 1. Clone the repository and develop locally
```
git clone https://github.com/llayer/titanic_k8s.git
```
Install the pipfile (requires a python3.7 version) and open the shell:
```
cd titanic_k8s/deploy
pipenv install
pipenv shell
```
Run the app:
```
python api.py
```
 
## 2. Build docker image and test locally
```
docker build --tag html-sklearn-app deploy
docker run -it --rm --name html-sklearn-app -p 5000:5000 -d html-sklearn-app
docker ps
```
The HTML GUI can then be accessed on localhost:5000 \
It is also possible to make a request from the CLI:
```
 curl http://localhost:5000/titanic/v1/predict_api --request POST --header 'Content-Type: application/json' --data '{"Pclass": [1], "Sex": ["female"], "Age": [20], "SibSp": [1], "Parch": [0], "Fare": [100], "Embarked": ["S"]}'
```
To stop the container run:
```
docker stop html-sklearn-app
```

## 3. Upload image to Azure Container Registry (ACR)
Login to Azure via a Webbrowser and if not yet done create Resource Group
```
az login
az group create --name ak8_knowledge_transfer --location westeurope
```
then create an ACR instance and login
```
az acr create --resource-group ak8_knowledge_transfer --name ak8acr --sku Basic
az acr login --name ak8acr
```
Figure out the acrLoginServer-adress of the ACR:
```
az acr list --resource-group ak8_knowledge_transfer --query "[].{acrLoginServer:loginServer}" --output table
```
Then tag the local docker image with the acrLoginServer-adress (here 'ak8acr.azurecr.io') and push the image to the ACR
```
docker images
docker tag html-sklearn-app:latest ak8acr.azurecr.io/html-sklearn-app:v1
docker push ak8acr.azurecr.io/html-sklearn-app:v1
```
The images on ACR can be listed with:
```
az acr repository list --name ak8acr --output table
```

## 4. Deploy to Kubernetes
Start a Kubernetes Cluster
```
az aks create --resource-group ak8_knowledge_transfer --name ak8sklearn --node-count 2 --generate-ssh-keys --attach-acr ak8acr
```
Note you need to have Admin/Owner rights to be able to connect to ACR or you need to create a Service Principal \
To configure kubectl run:
```
az aks get-credentials --resource-group ak8_knowledge_transfer --name ak8sklearn
```
The connection to the cluster can be checked with:
```
kubectl get nodes
```
The image can then be deployed with the commands:
```
kubectl create deployment html-sklearn-app --image=ak8acr.azurecr.io/html-sklearn-app:v1
kubectl expose deployment html-sklearn-app --port 5000 --type=LoadBalancer --name html-sklearn-app-lb
```
The status of the pods can be checked with
```
kubectl get pods
```
Find the public IP:
```
kubectl get service html-sklearn-app-lb --watch
```
The HTML API can the be accessed via the IP at port 5000, e.g. navigate in the browser to http://20.23.18.73:5000/ \
A request can also be made via the CLI:
```
curl http://20.23.18.73:5000/titanic/v1/predict_api --request POST --header 'Content-Type: application/json' --request POST --header 'Content-Type: application/json'   --data '{"Pclass": [1], "Sex": ["male"], "Age": [32], "SibSp": [1], "Parch": [0], "Fare": [100], "Embarked": ["S"]}'
```
Once the Cluster is not needed any more, it can be stopped or deleted with:
```
az aks stop --name ak8sklearn --resource-group ak8_knowledge_transfer
az aks delete --name ak8sklearn --resource-group ak8_knowledge_transfer
```

## 5. Scale and update the app
To update the image locally after changes to the code, remove the old one and build a new one
```
docker image rm html-sklearn-app
docker build --tag html-sklearn-app deploy
```
Then tag the new image version and push to the ACR:
```
docker tag html-sklearn-app:latest ak8acr.azurecr.io/html-sklearn-app:v2
docker push ak8acr.azurecr.io/html-sklearn-app:v2
```
To keep the deployment stable, it is required to scale the pods:
```
kubectl scale --replicas=3 deployment/html-sklearn-app
kubectl get pods
```
The new image can then be set via:
```
kubectl set image deployment html-sklearn-app html-sklearn-app=ak8acr.azurecr.io/html-sklearn-app:v2
kubectl get pods
kubectl scale --replicas=1 deployment/html-sklearn-app
```
The public IP can then be obtained via:
```
kubectl get service html-sklearn-app-lb --watch
```


