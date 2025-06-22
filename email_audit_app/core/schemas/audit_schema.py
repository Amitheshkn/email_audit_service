from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class RuleBase(BaseModel):
    passed: bool = Field(..., title="Rule Pass Status")
    score: float = Field(..., ge=0, le=10, title="Rule Score")
    justification: str = Field(..., title="Rule Evaluation Justification")


class RuleResult(RuleBase):
    rule_name: str = Field(..., title="Rule Name", max_length=100)


class AuditStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


class AuditResult(BaseModel):
    status: AuditStatus = Field(..., title="Audit Status")
    overall_score: float = Field(default=None, ge=0, le=10, title="Overall Audit Score")
    rule_results: list[RuleResult] = Field(default=None, title="Individual Rule Results")
    error: Optional[str] = Field(default=None, title="Error Message", max_length=500,
                                 description="Optional error message if the audit failed")
