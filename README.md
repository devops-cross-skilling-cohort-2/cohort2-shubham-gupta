# Cohort Application

A Flask REST API with structured logging, modular architecture, and comprehensive testing.

## Features

- **Structured Logging**: JSON-formatted logs for easy parsing and monitoring
- **Modular Architecture**: Clean separation of concerns with organized project structure
- **Health Check Endpoint**: Monitor application status and configuration
- **Environment Configuration**: Flexible configuration via environment variables
- **Comprehensive Testing**: Unit tests with full coverage

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
├── evidence_pack/
│   └── week1_evidence_pack.md      # Week 1 implementation evidence
│
├── .env                            # Environment variables (create this)
├── requirements.txt                # Python dependencies
└── README.md
```

---

## Prerequisites

- Python 3.10 or higher
- pip package manager

Verify your installation:

```bash
python3 --version
pip --version
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

Start the Flask server:

```bash
python src/app.py
```

The application will start on `http://localhost:5050`

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

## Dependencies

```txt
Flask==3.1.0
Werkzeug==3.1.3
python-dotenv==1.0.1
```

---

## Documentation

- **Week 1 Evidence Pack**: See [evidence_pack/week1_evidence_pack.md](evidence_pack/week1_evidence_pack.md) for detailed implementation evidence and testing results
