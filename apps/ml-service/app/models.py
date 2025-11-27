from pydantic import BaseModel
from typing import Optional

class CompanyFeatureRequest(BaseModel):
    inn: str

class CompanyFeatures(BaseModel):
    inn: str
    name: Optional[str]
    region: Optional[int]
    okved: Optional[int]
    status_active: Optional[float]
    status_terminated: Optional[float]
    status_bankruptcy: Optional[float]
    status_exclusion: Optional[float]
    status_reorganization: Optional[float]
    status_liquidation: Optional[float]
    purchases: Optional[float]
    year_2020: Optional[float]
    year_2021: Optional[float]
    year_2022: Optional[float]
    year_2023: Optional[float]
    year_2024: Optional[float]
    year_2025: Optional[float]
    sum_arrears: Optional[float]
    sum_debt: Optional[float]
    remaining_debt: Optional[float] 