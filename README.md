# titanic_k8s
Repository to test the deployment of a docker image to AKS

## 1. Clone the repository 
```
git clone https://github.com/llayer/titanic_k8s.git
```
 
## 2. Build docker image and test locally
```
docker build --tag html-sklearn-app deploy
docker run -it --rm --name html-sklearn-app -p 5000:5000 -d html-sklearn-app
```
The HTML GUI can then be accessed on localhost:5000 \
It is also possible to make a request from the CLI:
```
 curl http://localhost:5000/titanic/v1/predict_api --request POST --header 'Content-Type: application/json'  \       
 --data '{"Pclass": [1], "Sex": ["female"], "Age": [20], "SibSp": [1], "Parch": [0], "Fare": [100], "Embarked": ["S"]}'
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
docker tag test-ml-score-api:latest ak8acr.azurecr.io/test-ml-score-api:v1
docker push ak8acr.azurecr.io/test-ml-score-api:v1
```


