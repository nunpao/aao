from dataclasses import dataclass

@dataclass
class InstanceData:
    name: str
    item_count: int
    capacity: int
    values: list[int]
    weights: list[int]
    optimal: int

@dataclass
class SolutionData:
    solution: list[int]
    z: int

@dataclass
class ReportRow:
    constructive_name: str
    local_search_name: str
    initial_solution: int
    found_solution: int
    deviation: float
    runtime: float

@dataclass
class InstanceReport:
    instance: InstanceData
    rows: list[ReportRow]