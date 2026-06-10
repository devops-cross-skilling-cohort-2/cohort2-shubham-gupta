# Cohort Application

A Flask REST API with structured logging, modular architecture, comprehensive testing, containerised deployment, and Kubernetes orchestration.

## Features

- **Structured Logging**: JSON-formatted logs for easy parsing and monitoring
- **Modular Architecture**: Clean separation of concerns with organised project structure
- **Health Check Endpoint**: Monitor application status and configuration
- **Environment Configuration**: Flexible runtime config via environment variables
- **Comprehensive Testing**: Unit tests with full coverage
- **Containerised**: Secure, efficient Docker image built on `python:3.10-slim`, runs as non-root user
- **CI/CD Pipelines**: Automated lint, test, build, push, and image verification via GitHub Actions
- **Kubernetes**: Deployed to K3D local cluster with probes, resource controls, and rolling updates

---

## Project Structure

```text
cohort-app/
│
├── src/
│   ├── app.py                      # Application entry point
│   ├── config/
│   │   └── settings.py             # Configuration management
│   ├── models/
│   │   └── health_response.py      # Response models
│   ├── routes/
│   │   └── health_routes.py        # API route definitions
│   └── utils/
│       └── logger_config.py        # Logging configuration
│
├── tests/
│   └── test_app.py                 # Unit tests
│
├── k8s/
│   └── dev/
│       ├── namespace.yaml          # cohort-dev namespace
│       ├── configmap.yaml          # Runtime config (version, env, port)
│       ├── secret.yaml             # Secret resource (placeholder)
│       ├── deployment.yaml         # 2 replicas, probes, resource limits
│       └── service.yaml            # ClusterIP service
│
├── .github/
│   └── workflows/
│       ├── ci.yml                  # CI: lint → unit tests → health check
│       ├── cd.yml                  # CD: docker build → push → verify
│       └── k8s-apply.yml           # K8s: apply manifests → rollout → verify
│
├── evidence_pack/
│   ├── week1_evidence_pack.md
│   ├── week2_evidence_pack.md
│   ├── week3_evidence_pack.md
│   └── week4_evidence_pack.md
│
├── Dockerfile                      # Container image definition
├── .dockerignore                   # Files excluded from Docker build context
├── .env                            # Environment variables (create this, do not commit)
├── requirements.txt                # Python dependencies
└── README.md
```

---

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Docker (for running the container)
- K3D + kubectl (for Kubernetes deployment)

Verify your installation:

```bash
python3 --version
pip --version
docker --version
k3d version
kubectl version --client
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd cohort-app-shgupta
```

### 2. Set Up Virtual Environment

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
APP_VERSION=1.0.0
APP_ENVIRONMENT=dev
APP_PORT=5050
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Locally

```bash
python -m src.app
```

The application will start on `http://localhost:5050`

### With Docker

**Pull from Docker Hub:**
```bash
docker pull shguptaee/cohort2-app:latest
```

**Run the container:**
```bash
docker run -p 5050:5050 \
  -e APP_VERSION=1.0.0 \
  -e APP_ENVIRONMENT=dev \
  -e APP_PORT=5050 \
  shguptaee/cohort2-app:latest
```

The application will start on `http://localhost:5050`

**Build locally:**
```bash
docker build -t cohort2-app:latest .
docker run -p 5050:5050 cohort2-app:latest
```

---

## API Endpoints

### Health Check

**Endpoint:** `GET /health`

**Example:**
```bash
curl http://localhost:5050/health
```

**Response:**
```json
{
  "status": "running",
  "timestamp": "2026-05-16T06:10:15.123456+00:00",
  "version": "1.0.0",
  "environment": "dev"
}
```

---

## Testing

Run the test suite:

```bash
python -m unittest discover tests
```

**Test Coverage:**
- Health endpoint success response
- Invalid endpoint handling (404)
- Method not allowed handling (405)

---

## Docker Image

| Property | Value |
|----------|-------|
| Base image | `python:3.10-slim` |
| Runs as | Non-root user (`appuser`, UID 1001) |
| Exposed port | `5050` |
| Docker Hub | `shguptaee/cohort2-app` |

Runtime values are passed via environment variables at container start — nothing sensitive is baked into the image.

---

## CI/CD Pipelines

### CI (`ci.yml`)
Triggers on every push and pull request to any branch.

```
lint-validation → unit-tests → health-check
```

### CD (`cd.yml`)
Triggers on merge to `main` (after CI passes).

```
docker-build-push → verify-image
```

- Builds and pushes image to Docker Hub tagged with `:latest` and `:<git-sha>`
- Pulls the pushed image on a fresh runner and verifies the `/health` endpoint

### K8s Apply (`k8s-apply.yml`)
Triggers after CD pipeline succeeds on `main`. Runs on a self-hosted runner (macOS ARM64) with local K3D cluster access.

```
apply manifests → wait for rollout → verify /health endpoint
```

- Applies Namespace, ConfigMap, Secret, Deployment, Service to `cohort-dev` namespace
- Waits for rollout to complete (2 minute timeout)
- Verifies `/health` endpoint returns HTTP 200 via `kubectl port-forward`

---

## Kubernetes

### Cluster
Local K3D cluster (`cohort-local`) — 1 server + 1 agent node.

```bash
k3d cluster create cohort-local --agents 1 --wait
```

### Deploy to dev

```bash
kubectl apply -f k8s/dev/
kubectl rollout status deployment/cohort2-app -n cohort-dev
```

### Verify

```bash
kubectl get pods -n cohort-dev
kubectl port-forward svc/cohort2-app-svc 9090:80 -n cohort-dev &
curl http://localhost:9090/health
```

### Deployment config

| Property | Value |
|----------|-------|
| Namespace | `cohort-dev` |
| Replicas | 2 |
| Strategy | `RollingUpdate` |
| Readiness probe | `GET /health` — delay 5s, period 10s |
| Liveness probe | `GET /health` — delay 10s, period 15s |
| CPU requests/limits | `100m` / `250m` |
| Memory requests/limits | `128Mi` / `256Mi` |

---

## Dependencies

```txt
Flask==3.1.0
Werkzeug==3.1.3
python-dotenv==1.0.1
```

---

## Documentation

- **Week 1 Evidence Pack**: See [evidence_pack/week1_evidence_pack.md](evidence_pack/week1_evidence_pack.md) for Flask API implementation evidence
- **Week 2 Evidence Pack**: See [evidence_pack/week2_evidence_pack.md](evidence_pack/week2_evidence_pack.md) for GitHub Actions CI pipeline evidence
- **Week 3 Evidence Pack**: See [evidence_pack/week3_evidence_pack.md](evidence_pack/week3_evidence_pack.md) for Docker containerisation and CD pipeline evidence
- **Week 4 Evidence Pack**: See [evidence_pack/week4_evidence_pack.md](evidence_pack/week4_evidence_pack.md) for Kubernetes deployment and CI apply evidence