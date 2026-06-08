from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime


# ─────────────────────────────────────────
# INPUT VALIDATION
# ─────────────────────────────────────────

class ResearchInput(BaseModel):
    """User input validation model"""

    topic: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Research topic"
    )

    depth: Literal['quick', 'detailed', 'comprehensive'] = Field(
        default="detailed",
        description="Research depth level"
    )

    @field_validator('topic')
    @classmethod
    def validate_topic(cls, v):
        v = v.strip()

        if not v:
            raise ValueError("Topic cannot empty")

        if v.isdigit():
            raise ValueError("Topic cannot contain only numbers")

        return v


# ─────────────────────────────────────────
# OUTPUT VALIDATION
# ─────────────────────────────────────────

class ResearchOutput(BaseModel):
    """Final research output structure"""

    topic: str = Field(..., description="Research topic")
    report: str = Field(..., description="Final generated report")

    status: Literal["success", "error"] = Field(
        default="success",
        description="Response status"
    )

    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Report generation time"
    )

    word_count: Optional[int] = Field(
        default=None,
        description="Word count of report"
    )

    error_message: Optional[str] = Field(
        default=None,
        description="Error details if any"
    )

    @field_validator('report')
    @classmethod
    def validate_report(cls, v):
        if not v.strip():
            raise ValueError("Report cannot empty")
        return v


# ─────────────────────────────────────────
# ERROR RESPONSE
# ─────────────────────────────────────────

class ErrorResponse(BaseModel):
    """Structured error response"""

    status: Literal["error"] = "error"

    message: str = Field(..., description="Error message")

    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Error time"
    )