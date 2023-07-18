# Kubernetes-Deployable Webservice #

---
A Dockerized RESTful API implemented using Flask containing a counter which increments
everytime the API endpoint is hit. The count persists in a MySQL
database mounted to a persistent volume, hence surviving pod restarts.
The webservice and database are deployable in K8s and the manifests
are included in the project directory. 

## Usage ##

The webservice and database are deployable in K8s. These were tested on a local
```minikube``` cluster - this section will deal with deploying onto such a cluster, and can be 
used as a template for deploying onto any cluster.

### Setup ###

---

#### Secrets ####

The MySQL root user password is defined in ```secrets.yml``` and defaulted to
```p@ssw0rd1```. To define a new password, change the ```db_root_password```
field in ```secrets.yml``` (make sure your new password is Base64-encoded) and the ```password``` parameter of the ```mysql.connector.connect()```
calls in ```app.py``` (which is not encoded).

#### MySQL Server ####

The ```mysql-deployment.yml``` manifest utilizes the default
mysql image, so this should be pulled with ```$ docker pull mysql```.

#### RESTful API ####

Build the image of the API with ```$ docker build --tag opsviewapi-1 .```
in the project directory.

### Deployment ###

---

Deploy the API and database with 

```$ kubectl apply -f mysql-deployment.yml,opsviewapi.yml,persistent-volume.yml,secrets.yml```.

If on Minikube, access the service itself by running

```$ minikube service opsviewapi-service``` 

and accessing the returned endpoint. After recieving message ```app run successfully```, hit enpoint
```http://<URL>/initdb``` to initialize the database, and then hit endpoint
```http://<URL>/counter``` to increment the counter, as desired.

---

Copyright &copy; Alon Lavie 2022
