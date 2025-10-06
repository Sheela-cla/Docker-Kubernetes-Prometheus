# Complete Deployment Guide: Django Calculator (Docker, ACR, Istio)
This guide provides step-by-step instructions for deploying the Python/Django Calculator application, which uses a PostgreSQL database, from your local machine to a Kubernetes cluster managed by Istio.

The final application will be accessible at: **` https://calculator.dazzle.zebrain.se.`**

## 1. Local Development (Docker & Docker Compose)
Before deploying, ensure your application runs locally.

### Prerequisites:
You will need the following tools installed and configured:

| Tool | Purpose | 
| --- | --- | 
| **Docker** & **Docker Compose** | Building and running containers locally. | 
| **Azure CLI** | Logging into and pushing images to Azure Container Registry (ACR). | 
| **Kubernetes CLI (`kubectl`)** | Interacting with the Kubernetes cluster. | 
| **Istio** | Service mesh installed and configured in your target cluster. | 

## 2. Local Setup & Development
The application uses `docker-compose` to manage the Django web server and the PostgreSQL database simultaneously.

#### Steps:
 Build Images: Compile the Django application image and set up the PostgreSQL database container.

**` docker-compose build `**

Run Migrations: Initialize the database schema.

# This runs the web container briefly to apply migrations
**` docker-compose run --rm web python manage.py migrate `**

Start Application: Run both the web and database services.

**` docker-compose up `**

The application is now accessible for testing at: **` http://localhost:8000. `**

## 3. Containerization and Image Push (ACR)
To deploy the application, the Kubernetes cluster must be able to pull the image from a private registry (Azure Container Registry is used here).

#### Steps:
**Log in to ACR:** Use the Azure CLI to authenticate Docker.

` az acr login --name ngorongoro.azurecr.io `

**Tag the Image:** Give your local image the correct name and tag for the registry.

` docker tag calculator_app:v1.7 ngorongoro.azurecr.io/calculator_app:v1.7 `

**Push the Image:** Upload the image to ACR.

` docker push ngorongoro.azurecr.io/calculator_app:v1.7 `

## 4. Kubernetes and Istio Deployment
The final deployment is managed by a single YAML manifest that defines seven separate resources: database, application, and networking components.

**Key Deployment Features:**
Namespace: All resources are deployed to the sheela namespace.

**Init Containers:** The application deployment uses two initContainers to wait for PostgreSQL and then run Django migrations before the main web app starts, ensuring stability.

**Istio Routing:** An Istio VirtualService routes external traffic from the ingress-gateway to the internal calculator-app-service.

**Automatic HTTPS:** Traffic is automatically secured and redirected to HTTPS by a pre-configured platform layer, so no manual TLS configuration (like Cert-Manager) is needed.

### **Deployment Manifest:**

**Deployment Steps:**
Ensure Pre-requisite Secret: Verify the acr-secret (for image pulling) exists in the sheela `namespace`.

**Apply the Manifest:** Deploy all components to the cluster.

` kubectl apply -f kubernetes_manifests_istio.yaml -n sheela `

**Verify:** Check the status of your Pods in the sheela namespace.

` kubectl get pods -n sheela `

Once all Pods are running, the application is live and secured by **Istio**.