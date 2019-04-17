# Docker Image for Django App

### Requirements
----------------
1. Install [Docker](http://docker.io).
2. Install [Docker-compose](http://docs.docker.com/compose/install/).


### Technique Stacks
---------------------
* [Docker](https://www.docker.com/)
    - An open platform for distributed applications for developers and sysadmins.

* [Docker Compose](https://docs.docker.com/compose/)
    - Compose is a tool for defining and running multi-container Docker applications.


### Backend Frameworks
-----------------------
* [Django](https://www.djangoproject.com/)
    - Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.

* [psycopg2](https://pypi.python.org/pypi/psycopg2)
    - PostgreSQL database adapter for Python.

* [Requests](https://pypi.python.org/pypi/requests/2.11.1)
    - Requests is the only Non-GMO HTTP library for Python, safe for human consumption.

* [Django-Extensions](https://github.com/django-extensions/django-extensions)
    - Django Extensions is a collection of custom extensions for the Django Framework.

* [Djanog Rest Framework](https://www.django-rest-framework.org/)
    - Django REST framework is a powerful and flexible toolkit for building Web APIs.

### Database
-------------
* [PostgresSQL](https://www.postgresql.org/)
    - PostgreSQL is a powerful, open source object-relational database system. It has more than 15 years of active development and a proven architecture that has earned it a strong reputation for reliability, data integrity, and correctness.

### Usage
----------
- Build Django 2.1
    ```
    $cd devops
    $docker build -t nhatthai/django2.1:latest .
    ```

- Run containers
    ```
    $cd devops
    $docker-compose up
    ```

### Ingress
------------
#### Create Ingress
```
$ cd devops/manifest
$ kubectl create -f ingress.yml
```

#### Check Ingress status
```
kubectl describe ing
```

#### Start Ingress on Minkube
```
$ minikube addons enable ingress
```

#### Minikube Dashboard
```
minikube dashboard
```

#### Get IP
```
$ minikube ip
192.168.99.100
```

#### Add mysite.com into /etc/hosts
```
192.168.99.100 mysite.com
```

#### Check Django App
```
http://mysite.com/admin/
```


### HELM
---------

#### Install Helm
```
$ brew install kubernetes-helm
```
or

```
curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get > get_helm.sh
chmod 700 get_helm.sh
./get_helm.sh
```

#### Create template
```
helm create helm-django
```

#### Deploy Django with Helm
```
$ helm install --name web ./helm-django --set service.type=NodePort
```

### Reference
- [Setup Helm](https://docs.bitnami.com/kubernetes/get-started-kubernetes/#step-4-install-helm-and-tiller)
- [How to create the first helm chart](https://docs.bitnami.com/kubernetes/how-to/create-your-first-helm-chart/)
