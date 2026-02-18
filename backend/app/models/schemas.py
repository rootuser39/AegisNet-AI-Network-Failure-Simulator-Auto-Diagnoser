from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class ScenarioInfo(BaseModel):
    id: str
    name: str
    description: str


class ScenariosResponse(BaseModel):
    scenarios: list[ScenarioInfo]


class TelemetrySeries(BaseModel):
    latency_ms: list[float]
    packet_loss_pct: list[float]
    jitter_ms: list[float]
    cpu_pct: list[float]


class SimulationResult(BaseModel):
    scenario: str
    timestamp: int
    telemetry: TelemetrySeries
    logs: list[str]
    ground_truth: dict[str, Any]


class SimulateRequest(BaseModel):
    scenario: str
    seed: int | None = None


class DiagnosisResult(BaseModel):
    diagnosis: str
    root_cause: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: list[str]
    fix_steps: list[str]


class AnalyzeRequest(BaseModel):
    simulation: SimulationResult


class AnalyzeResponse(BaseModel):
    result: DiagnosisResult
