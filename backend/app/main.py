import random
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import (
    HealthResponse,
    ScenariosResponse,
    ScenarioInfo,
    SimulateRequest,
    SimulationResult,
    TelemetrySeries,
    AnalyzeRequest,
    AnalyzeResponse,
    DiagnosisResult,
)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "service": "aegisnet",
        "version": "0.1"
    }


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok")


@app.get("/scenarios", response_model=ScenariosResponse)
def get_scenarios():
    scenarios = [
        ScenarioInfo(
            id="bgp_flap",
            name="BGP Flap",
            description="Border Gateway Protocol route flapping causing intermittent connectivity"
        ),
        ScenarioInfo(
            id="dns_outage",
            name="DNS Outage",
            description="Domain Name System resolution failure preventing name lookups"
        ),
        ScenarioInfo(
            id="interface_down",
            name="Interface Down",
            description="Network interface failure causing complete connectivity loss"
        ),
        ScenarioInfo(
            id="mtu_mismatch",
            name="MTU Mismatch",
            description="Maximum Transmission Unit mismatch causing packet fragmentation issues"
        ),
    ]
    return ScenariosResponse(scenarios=scenarios)


@app.post("/simulate", response_model=SimulationResult)
def simulate(request: SimulateRequest):
    # Use seed for deterministic output
    if request.seed is not None:
        random.seed(request.seed)
    
    timestamp = int(time.time())
    
    # Generate telemetry based on scenario
    telemetry = generate_telemetry(request.scenario)
    
    # Generate logs (4 to 8 lines)
    num_logs = random.randint(4, 8)
    logs = generate_logs(request.scenario, num_logs)
    
    return SimulationResult(
        scenario=request.scenario,
        timestamp=timestamp,
        telemetry=telemetry,
        logs=logs,
        ground_truth={}
    )


def generate_telemetry(scenario: str) -> TelemetrySeries:
    """Generate 20 telemetry points for each metric based on scenario"""
    
    if scenario == "bgp_flap":
        # High jitter and intermittent packet loss
        latency_ms = [random.uniform(10, 50) for _ in range(20)]
        packet_loss_pct = [random.uniform(0, 15) if i % 3 == 0 else 0.0 for i in range(20)]
        jitter_ms = [random.uniform(5, 25) for _ in range(20)]
        cpu_pct = [random.uniform(20, 40) for _ in range(20)]
        
    elif scenario == "dns_outage":
        # High latency, low packet loss
        latency_ms = [random.uniform(100, 500) for _ in range(20)]
        packet_loss_pct = [random.uniform(0, 2) for _ in range(20)]
        jitter_ms = [random.uniform(1, 5) for _ in range(20)]
        cpu_pct = [random.uniform(10, 30) for _ in range(20)]
        
    elif scenario == "interface_down":
        # Complete failure - high packet loss
        latency_ms = [0.0 for _ in range(20)]
        packet_loss_pct = [100.0 for _ in range(20)]
        jitter_ms = [0.0 for _ in range(20)]
        cpu_pct = [random.uniform(5, 15) for _ in range(20)]
        
    elif scenario == "mtu_mismatch":
        # Moderate latency and packet loss
        latency_ms = [random.uniform(30, 80) for _ in range(20)]
        packet_loss_pct = [random.uniform(5, 20) for _ in range(20)]
        jitter_ms = [random.uniform(3, 10) for _ in range(20)]
        cpu_pct = [random.uniform(15, 35) for _ in range(20)]
        
    else:
        # Default telemetry
        latency_ms = [random.uniform(10, 100) for _ in range(20)]
        packet_loss_pct = [random.uniform(0, 10) for _ in range(20)]
        jitter_ms = [random.uniform(1, 10) for _ in range(20)]
        cpu_pct = [random.uniform(10, 50) for _ in range(20)]
    
    return TelemetrySeries(
        latency_ms=latency_ms,
        packet_loss_pct=packet_loss_pct,
        jitter_ms=jitter_ms,
        cpu_pct=cpu_pct
    )


def generate_logs(scenario: str, num_logs: int) -> list[str]:
    """Generate realistic log entries based on scenario"""
    
    log_templates = {
        "bgp_flap": [
            "BGP: peer 10.0.0.1 state changed to Idle",
            "BGP: peer 10.0.0.1 state changed to Active",
            "BGP: received UPDATE from 10.0.0.1",
            "BGP: route 192.168.1.0/24 withdrawn",
            "BGP: route 192.168.1.0/24 learned via 10.0.0.1",
            "BGP: routing table unstable",
            "BGP: peer 10.0.0.1 flapping detected",
        ],
        "dns_outage": [
            "DNS: query timeout for example.com",
            "DNS: no response from server 8.8.8.8",
            "DNS: resolver failed to start",
            "DNS: cache miss for domain",
            "DNS: connection to nameserver failed",
            "DNS: lookup failed after 3 retries",
        ],
        "interface_down": [
            "Interface eth0: link down",
            "Interface eth0: carrier lost",
            "Interface eth0: no physical connection",
            "Routing: route via eth0 unreachable",
            "Interface eth0: administratively down",
            "Network: connectivity check failed",
        ],
        "mtu_mismatch": [
            "IP: fragmentation needed but DF set",
            "ICMP: packet too big received",
            "TCP: MSS mismatch detected",
            "IP: dropping oversized packet",
            "Interface: MTU 1500, peer MTU 1400",
            "Network: fragmentation errors increasing",
        ],
    }
    
    templates = log_templates.get(scenario, ["Log entry generated"])
    logs = []
    for i in range(num_logs):
        log = templates[i % len(templates)]
        logs.append(log)
    
    return logs


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    # Placeholder analyzer
    result = DiagnosisResult(
        diagnosis="unknown",
        root_cause="Analyzer not implemented yet",
        confidence=0.0,
        evidence=[],
        fix_steps=[]
    )
    return AnalyzeResponse(result=result)
