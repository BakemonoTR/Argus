from pydantic import BaseModel
from typing import List

class SecurityFinding(BaseModel):
    issue: str           # Sorunun açıklaması
    severity: int        # 1-10 arası önem skoru
    line: int            # Kaçıncı satırda
    suggestion: str      # Ne yapılmalı

class SecurityReport(BaseModel):
    findings: List[SecurityFinding]   # Tüm bulgular listesi
    summary: str                       # Genel özet