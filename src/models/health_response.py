from dataclasses import dataclass

@dataclass
class HealthResponse:
    status: str
    timestamp: str
    version: str
    environment: str