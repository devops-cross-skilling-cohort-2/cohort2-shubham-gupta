# Cohort Application

A Flask REST API with structured logging, modular architecture, comprehensive testing, containerised deployment, Kubernetes orchestration, and Helm packaging.

## Features

- **Structured Logging**: JSON-formatted logs for easy parsing and monitoring
- **Modular Architecture**: Clean separation of concerns with organised project structure
- **Health Check Endpoint**: Monitor application status and configuration
- **Environment Configuration**: Flexible runtime config via environment variables
- **Comprehensive Testing**: Unit tests with full coverage
- **Containerised**: Secure, efficient Docker image built on `python:3.12-slim`, runs as non-root user
- **CI/CD Pipelines**: Automated lint, test, helm validation, build, push, image scan, and verification via GitHub Actions
- **Kubernetes**: Deployed to K3D local cluster with probes, resource controls, and rolling updates
- **Helm**: Environment-aware release packaging with upgrade and rollback support across dev and prod

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
├── helm/
│   └── cohort2-app/                # Helm chart
│       ├── Chart.yaml              # Chart metadata
│       ├── values.yaml             # Shared defaults (all environments)
│       ├── values-dev.yaml         # Dev overrides (namespace, env, replicas=2)
│       ├── values-prod.yaml        # Prod overrides (namespace, env, replicas=3)
│       └── templates/
│           ├── _helpers.tpl        # Reusable name/label helpers
│           ├── deployment.yaml     # Parameterised deployment
│           ├── service.yaml        # Parameterised service
│           ├── configmap.yaml      # Config from .Values.config
│           ├── secret.yaml         # Secret from .Values.secret (b64enc)
│           └── NOTES.txt           # Post-install instructions
│
├── k8s/
│   ├── dev/                        # Flat manifests (superseded by Helm — kept for reference)
│   └── prod/                       # Flat manifests (superseded by Helm — kept for reference)
│
├── .github/
│   └── workflows/
│       ├── ci.yml                  # CI: lint → helm-validate → unit tests → health check
│       ├── cd.yml                  # CD: docker build → trivy scan → push → verify
│       ├── k8s-apply.yml           # Dev deploy: helm upgrade --install → verify
│       └── k8s-prod.yml            # Prod deploy: helm upgrade --install → verify
│
├── evidence_pack/
│   ├── week1_evidence_pack.md
│   ├── week2_evidence_pack.md
│   ├── week3_evidence_pack.md
│   ├── week4_evidence_pack.md
│   └── week5_evidence_pack.md
│
├── Dockerfile                      # Container image definition (python:3.12-slim)
├── .dockerignore                   # Files excluded from Docker build context
├── .env                            # Environment variables (create this, do not commit)
├── requirements.txt                # Python dependencies
└── README.md
```

---

## Prerequisites

- Python 3.12 or higher
- pip package manager
- Docker (for running the container)
- K3D + kubectl (for Kubernetes deployment)
- Helm 3 (for chart packaging and deployment)

Verify your installation:

```bash
python3 --version
pip --version
docker --version
k3d version
kubectl version --client
helm version
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
| Base image | `python:3.12-slim` |
| Runs as | Non-root user (`appuser`, UID 1001) |
| Exposed port | `5050` |
| Docker Hub | `shguptaee/cohort2-app` |

Runtime values are passed via environment variables at container start — nothing sensitive is baked into the image.

---

## CI/CD Pipelines

### CI (`ci.yml`)
Triggers on every push and pull request to any branch.

```
lint-validation → helm-validate → unit-tests → health-check
```

- `helm-validate`: runs `helm lint` and renders templates for dev and prod — catches broken chart syntax at PR time

### CD (`cd.yml`)
Triggers on merge to `main` (after CI passes) and on version tag pushes (`v*`).

```
docker-build-push → trivy-scan → verify-image
```

- Builds multi-platform image (amd64 + arm64) tagged with `:latest`, `:<git-sha>`, and `:<version>` on tag push
- Trivy vulnerability scan — reports findings to GitHub Security tab
- Pulls the pushed image on a fresh runner and verifies the `/health` endpoint

### K8s Dev Deploy (`k8s-apply.yml`)
Triggers after CD succeeds on `main`. Runs on self-hosted runner (macOS ARM64).

```
helm upgrade --install → verify pods → verify /health endpoint
```

- Deploys to `cohort-dev` namespace using `helm upgrade --install --atomic`
- Image tag pinned to commit SHA via `--set image.tag=`
- `--atomic` auto-rolls back on failure

### K8s Prod Deploy (`k8s-prod.yml`)
Triggers after CD succeeds on a version tag (`v*`). Runs on self-hosted runner (macOS ARM64).

```
helm upgrade --install → verify pods → verify /health endpoint
```

- Deploys to `cohort-prod` namespace using `helm upgrade --install --atomic`
- Image tag set to the version tag (e.g. `v1.0.0`) via `--set image.tag=`
- Supports `workflow_dispatch` with `image_tag` input for manual deploys and rollbacks

---

## Kubernetes + Helm

### Cluster
Local K3D cluster (`cohort-local`) — 1 server + 1 agent node.

```bash
k3d cluster create cohort-local --agents 1 --wait
```

### Deploy with Helm

**Dev:**
```bash
helm upgrade --install cohort2-app-dev ./helm/cohort2-app \
  -f helm/cohort2-app/values-dev.yaml \
  --set image.tag=<commit-sha> \
  --set secret.appSecretKey=<secret> \
  --namespace cohort-dev --create-namespace \
  --atomic --timeout 2m
```

**Prod:**
```bash
helm upgrade --install cohort2-app-prod ./helm/cohort2-app \
  -f helm/cohort2-app/values-prod.yaml \
  --set image.tag=<version-tag> \
  --set secret.appSecretKey=<secret> \
  --namespace cohort-prod --create-namespace \
  --atomic --timeout 3m
```

### Verify

```bash
# Dev
kubectl get pods -n cohort-dev
kubectl port-forward svc/cohort2-app-dev-svc 9091:80 -n cohort-dev &
curl http://localhost:9091/health

# Prod
kubectl get pods -n cohort-prod
kubectl port-forward svc/cohort2-app-prod-svc 9092:80 -n cohort-prod &
curl http://localhost:9092/health
```

### Rollback

```bash
helm history cohort2-app-prod -n cohort-prod    # view revision history
helm rollback cohort2-app-prod <revision> -n cohort-prod
```

### Deployment config

| Property | Dev | Prod |
|----------|-----|------|
| Namespace | `cohort-dev` | `cohort-prod` |
| Replicas | `2` | `3` |
| APP_ENVIRONMENT | `dev` | `prod` |
| Strategy | `RollingUpdate` | `RollingUpdate` |
| Readiness probe | `GET /health` — delay 5s, period 10s | same |
| Liveness probe | `GET /health` — delay 10s, period 15s | same |
| CPU requests/limits | `100m` / `250m` | same |
| Memory requests/limits | `128Mi` / `256Mi` | same |

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
- **Week 5 Evidence Pack**: See [evidence_pack/week5_evidence_pack.md](evidence_pack/week5_evidence_pack.md) for Helm packaging, multi-environment deployment, and rollback evidence