from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class Period:
    startTime: datetime
    endTime: datetime

@dataclass
class EnergyMeter:
    total: float
    byTariffHeading: Dict[str, float]

@dataclass
class Cost:
    total: float
    standingCharge: float
    standingChargeByComponents: Dict[str, float]
    byTariffHeading: Dict[str, float]

@dataclass
class Consumption:
    period: Period
    energyMeter: EnergyMeter
    cost: Cost
    quality: float
    errorFlags: List[str]
    indexNatures: List[str]
    status: str
    nature: str
    aggregated: bool
    usingLoadCurve: bool

@dataclass
class GlobalConsumption:
    period: Period
    energyMeter: EnergyMeter
    cost: Cost
    quality: float
    errorFlags: List[str]
    indexNatures: List[str]
    status: str
    nature: str
    aggregated: bool
    usingLoadCurve: bool

@dataclass
class DataInterface:
    period: Period
    step: str
    units: Dict[str, str]
    consumptions: List[Consumption]
    globalConsumption: GlobalConsumption