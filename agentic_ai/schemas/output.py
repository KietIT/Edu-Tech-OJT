"""
Output schemas for the Timetable Analyzer system.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

from .paths import WeeklyStudySchedule


class WeakSubjectInfo(BaseModel):
    """Information about an identified weak subject"""
    subject: str = Field(description="Subject display name, e.g. 'Lý', 'Hóa'")
    average_score: float = Field(ge=0, le=10)
    gap: float = Field(description="How far below the threshold (threshold - score)")
    weak_topics: List[str] = Field(default_factory=list, description="Specific weak topic names")
    source: str = Field(default="academic_data", description="'academic_data' or 'report_card'")
    classification: Optional[str] = Field(default=None, description="e.g. 'Trung bình', 'Khá'")


class AnalysisResult(BaseModel):
    """
    Output from the TimetableAnalyzer.

    This is the complete JSON structure returned to frontend/backend.
    The primary output is the weekly_study_schedule.
    """
    student_id: str
    student_name: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # PRIMARY OUTPUT: the supplementary study timetable
    weekly_study_schedule: Optional[WeeklyStudySchedule] = Field(
        default=None,
        description="Concrete weekly schedule for supplementary study, avoids school hours"
    )

    # Analysis details
    weak_subjects_analysis: List[WeakSubjectInfo] = Field(
        default_factory=list,
        description="List of identified weak subjects with details"
    )

    # AI summary (FUTURE — currently always None)
    ai_summary: Optional[str] = Field(
        default=None,
        description="AI-generated study tips and summary (reserved for future use)"
    )

    # Metadata
    processing_time_seconds: float = Field(default=0.0)
    version: str = Field(default="2.0.0")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AgentOutput(BaseModel):
    """Generic agent output wrapper (kept for internal compatibility)"""
    agent_name: str
    success: bool
    data: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    execution_time_seconds: float = Field(default=0.0)
    logs: List[str] = Field(default_factory=list)
