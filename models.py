from dataclasses import dataclass

@dataclass
class InstanceData:
    """In-memory representation of one knapsack instance and its reference optimum."""
    name: str
    item_count: int
    capacity: int
    values: list[int]
    weights: list[int]
    optimal: int

@dataclass
class SolutionData:
    """Binary solution vector together with its objective value."""
    solution: list[int]
    z: int

@dataclass
class ReportRow:
    """Metrics collected for one constructive/local-search combination on one instance."""
    constructive_name: str
    local_search_name: str
    initial_solution: int
    found_solution: int
    deviation: float
    runtime: float

@dataclass
class InstanceReport:
    """Set of report rows produced for a single instance."""
    instance: InstanceData
    rows: list[ReportRow]
