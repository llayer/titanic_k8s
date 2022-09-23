# titanic_k8s
Repository to test the deployment of a docker image to AKS

## 1. Clone the repository 
```
git clone https://github.com/llayer/titanic_k8s.git
```
 
## 2. Build docker image and run container
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
