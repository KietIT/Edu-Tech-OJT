"""
Learning path schemas for the 3 agents' outputs.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import date


class ResourceType(str, Enum):
    """Types of learning resources"""
    VIDEO = "video"
    DOCUMENT = "document"
    EXERCISE = "exercise"
    PRACTICE_TEST = "practice_test"
    INTERACTIVE = "interactive"
    MINDMAP = "mindmap"
    FLASHCARD = "flashcard"
    PROJECT = "project"


class Priority(str, Enum):
    """Priority levels for subjects/tasks"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class LearningResource(BaseModel):
    """A learning resource recommendation"""
    resource_id: Optional[str] = None
    title: str
    resource_type: ResourceType
    url: Optional[str] = None
    description: Optional[str] = None
    estimated_duration_minutes: int = Field(default=30)
    difficulty: str = Field(default="medium")
    matches_learning_style: bool = Field(default=False)


class Checkpoint(BaseModel):
    """Assessment checkpoint in a learning path"""
    checkpoint_id: str
    name: str
    type: str = Field(description="quiz, test, project, self_assessment")
    topics_covered: List[str] = Field(default_factory=list)
    passing_score: float = Field(default=7.0, description="Điểm đạt trên thang 10")
    estimated_duration_minutes: int = Field(default=30)


class StudySlot(BaseModel):
    """A recommended study time slot"""
    day: str = Field(description="e.g., 'thu_2', 'thu_7', 'chu_nhat'")
    start: str = Field(description="e.g., '19:30'")
    end: str = Field(description="e.g., '22:00'")
    quality: str = Field(default="trung bình", description="'tốt' or 'trung bình'")


class ScheduleEntry(BaseModel):
    """A single entry in the weekly supplementary study schedule"""
    day: str = Field(description="e.g., 'Thứ 2', 'Thứ 7', 'Chủ Nhật'")
    day_key: str = Field(description="e.g., 'thu_2', 'thu_7', 'chu_nhat'")
    start: str = Field(description="Start time, e.g., '19:30'")
    end: str = Field(description="End time, e.g., '21:30'")
    subject: str = Field(description="Subject to study, e.g., 'Vật Lý'")
    topics: List[str] = Field(default_factory=list, description="Specific topics to focus on")
    activity: str = Field(default="Tự học", description="e.g., 'Tự học', 'Làm bài tập', 'Ôn tập'")
    duration_minutes: int = Field(default=90)
    slot_quality: str = Field(default="trung bình", description="Concentration quality for this slot")
    notes: str = Field(default="")


class WeeklyStudySchedule(BaseModel):
    """
    Concrete weekly supplementary study schedule.
    This is the PRIMARY OUTPUT required by the new requirements:
    a schedule that avoids school class times and arranges
    study sessions for weak subjects at available times.
    """
    schedule_id: str
    student_name: str
    entries: List[ScheduleEntry] = Field(default_factory=list)
    total_supplementary_hours: float = Field(default=0.0)
    weak_subjects_covered: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class WeeklyPlan(BaseModel):
    """Weekly plan for remedial path"""
    week_number: int
    learning_goals: List[str]
    topics_to_cover: List[str]
    resources: List[LearningResource] = Field(default_factory=list)
    checkpoints: List[Checkpoint] = Field(default_factory=list)
    estimated_hours: float = Field(default=5.0)
    psychology_adaptations: List[str] = Field(
        default_factory=list,
        description="Specific adaptations based on psychology profile"
    )
    recommended_study_slots: List[StudySlot] = Field(
        default_factory=list,
        description="Best time slots for studying based on student habits"
    )


class SubjectRemedialPlan(BaseModel):
    """Remedial plan for a specific subject"""
    subject: str
    current_score: float
    target_score: float
    weak_topics: List[str]
    weekly_plans: List[WeeklyPlan] = Field(default_factory=list)
    estimated_improvement: str = Field(description="e.g., '+20-30 points after 4 weeks'")


class RemedialPath(BaseModel):
    """
    Remedial Path Agent output.
    Short-term path (4-8 weeks) to address weak subjects/topics.
    """
    path_id: str
    duration_weeks: int = Field(ge=0, le=8, description="0 nếu không cần khắc phục, 4-8 tuần nếu cần")
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    weekly_study_schedule: Optional[WeeklyStudySchedule] = Field(
        default=None,
        description="Concrete weekly schedule: which day/time to study which weak subject"
    )
    subject_plans: List[SubjectRemedialPlan] = Field(default_factory=list)
    overall_goals: List[str] = Field(default_factory=list)
    psychology_considerations: Dict[str, str] = Field(
        default_factory=dict,
        description="How psychology profile influences this path"
    )
    success_metrics: List[str] = Field(default_factory=list)


class SubjectPriority(BaseModel):
    """Subject priority in strategic path"""
    subject: str
    priority: Priority
    is_exam_subject: bool
    current_score: float
    target_score: float
    gap: float = Field(description="target_score - current_score")
    weekly_hours_recommended: float


class PhaseMilestone(BaseModel):
    """Milestone within a phase"""
    milestone_id: str
    name: str
    target_date: Optional[date] = None
    criteria: List[str]
    is_completed: bool = Field(default=False)


class PhasePlan(BaseModel):
    """Plan for a phase (quarter/semester) in strategic path"""
    phase_number: int
    phase_name: str = Field(description="e.g., 'Q1 2024', 'Semester 1'")
    duration_months: int = Field(default=3)
    subject_targets: Dict[str, float] = Field(
        default_factory=dict,
        description="Subject -> target score mapping"
    )
    weekly_hours_by_subject: Dict[str, float] = Field(default_factory=dict)
    milestones: List[PhaseMilestone] = Field(default_factory=list)
    focus_areas: List[str] = Field(default_factory=list)
    psychology_adaptations: List[str] = Field(default_factory=list)


class GapAnalysis(BaseModel):
    """Gap analysis for strategic path"""
    current_total_score: float
    target_total_score: float
    gap: float
    target_university: Optional[str] = None
    target_major: Optional[str] = None
    competitiveness: str = Field(description="e.g., 'achievable', 'challenging', 'stretch'")


class StrategicPath(BaseModel):
    """
    Strategic THPT Path Agent output.
    Long-term path (12-24 months) for exam preparation.
    """
    path_id: str
    duration_months: int = Field(ge=0, le=24, description="0 nếu không áp dụng, 12-24 tháng nếu cần")
    exam_block: str
    subject_priorities: List[SubjectPriority] = Field(default_factory=list)
    phases: List[PhasePlan] = Field(default_factory=list)
    gap_analysis: Optional[GapAnalysis] = None
    critical_success_factors: List[str] = Field(default_factory=list)
    psychology_considerations: Dict[str, str] = Field(default_factory=dict)


class Prerequisite(BaseModel):
    """Prerequisite for career path"""
    name: str
    category: str = Field(description="e.g., 'knowledge', 'skill', 'certification'")
    status: str = Field(description="'achieved', 'in_progress', 'not_started'")
    current_level: Optional[str] = None
    target_level: Optional[str] = None
    resources: List[LearningResource] = Field(default_factory=list)


class CareerPhase(str, Enum):
    """Phases in career path"""
    THPT = "thpt"
    PRE_UNIVERSITY = "pre_university"
    UNIVERSITY_YEAR_1 = "university_year_1"
    UNIVERSITY_YEAR_2 = "university_year_2"
    UNIVERSITY_YEAR_3 = "university_year_3"
    UNIVERSITY_YEAR_4 = "university_year_4"
    GRADUATE = "graduate"


class CareerPhasePlan(BaseModel):
    """Plan for a career phase"""
    phase: CareerPhase
    phase_name: str
    duration_months: int
    objectives: List[str]
    key_courses: List[str] = Field(default_factory=list)
    recommended_projects: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    skills_to_develop: List[str] = Field(default_factory=list)
    milestones: List[PhaseMilestone] = Field(default_factory=list)
    resources: List[LearningResource] = Field(default_factory=list)


class Milestone(BaseModel):
    """General milestone"""
    milestone_id: str
    name: str
    description: Optional[str] = None
    phase: Optional[str] = None
    target_date: Optional[date] = None
    criteria: List[str] = Field(default_factory=list)


class CareerPath(BaseModel):
    """
    Career Path Agent output.
    Path for career/major preparation (especially for university and beyond).
    """
    path_id: str
    target_career: str
    target_field: str = Field(description="e.g., 'AI', 'Medicine', 'Economics'")
    prerequisites: List[Prerequisite] = Field(default_factory=list)
    phase_plans: List[CareerPhasePlan] = Field(default_factory=list)
    recommended_universities: List[str] = Field(default_factory=list)
    industry_insights: List[str] = Field(default_factory=list)
    psychology_fit: Dict[str, str] = Field(
        default_factory=dict,
        description="How personality traits align with career"
    )
    long_term_milestones: List[Milestone] = Field(default_factory=list)
