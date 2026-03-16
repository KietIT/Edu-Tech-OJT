"""
Student profile and academic data schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum


class GradeLevel(str, Enum):
    """Grade levels from 9-12 (THPT) and university"""
    GRADE_9 = "9"
    GRADE_10 = "10"
    GRADE_11 = "11"
    GRADE_12 = "12"
    UNIVERSITY_1 = "dai_hoc_1"
    UNIVERSITY_2 = "dai_hoc_2"
    UNIVERSITY_3 = "dai_hoc_3"
    UNIVERSITY_4 = "dai_hoc_4"
    GRADUATE = "sau_dai_hoc"


class ExamBlock(str, Enum):
    """Vietnamese exam blocks (khoi thi)"""
    A00 = "A00"  # Toan, Ly, Hoa
    A01 = "A01"  # Toan, Ly, Anh
    B00 = "B00"  # Toan, Hoa, Sinh
    C00 = "C00"  # Van, Su, Dia
    D01 = "D01"  # Toan, Van, Anh
    D07 = "D07"  # Toan, Hoa, Anh
    # Add more as needed


class Subject(str, Enum):
    """School subjects"""
    TOAN = "toan"
    VAN = "van"
    ANH = "anh"
    LY = "ly"
    HOA = "hoa"
    SINH = "sinh"
    SU = "su"
    DIA = "dia"
    GDCD = "gdcd"
    TIN = "tin"
    CONG_NGHE = "cong_nghe"


# Tên hiển thị tiếng Việt có dấu cho các môn học
SUBJECT_DISPLAY_NAMES = {
    "toan": "Toán",
    "van": "Văn",
    "anh": "Anh",
    "ly": "Lý",
    "hoa": "Hóa",
    "sinh": "Sinh",
    "su": "Sử",
    "dia": "Địa",
    "gdcd": "GDCD",
    "tin": "Tin",
    "cong_nghe": "Công nghệ",
}


def get_subject_display_name(subject_value: str) -> str:
    """Lấy tên hiển thị tiếng Việt có dấu từ giá trị enum môn học"""
    return SUBJECT_DISPLAY_NAMES.get(subject_value, subject_value)


# Subject mapping for exam blocks
EXAM_BLOCK_SUBJECTS = {
    ExamBlock.A00: [Subject.TOAN, Subject.LY, Subject.HOA],
    ExamBlock.A01: [Subject.TOAN, Subject.LY, Subject.ANH],
    ExamBlock.B00: [Subject.TOAN, Subject.HOA, Subject.SINH],
    ExamBlock.C00: [Subject.VAN, Subject.SU, Subject.DIA],
    ExamBlock.D01: [Subject.TOAN, Subject.VAN, Subject.ANH],
    ExamBlock.D07: [Subject.TOAN, Subject.HOA, Subject.ANH],
}

# Mandatory subjects for THPT
MANDATORY_SUBJECTS = [Subject.TOAN, Subject.VAN]


class TopicScore(BaseModel):
    """Score for a specific topic within a subject"""
    topic_id: str
    topic_name: str
    score: float = Field(ge=0, le=10)
    max_score: float = Field(default=10)
    is_core_topic: bool = Field(default=False, description="Whether this is a foundational/core topic")
    exam_frequency: float = Field(
        default=0.5,
        ge=0,
        le=1,
        description="How frequently this topic appears in exams (0-1)"
    )


class SubjectScore(BaseModel):
    """Aggregated score for a subject"""
    subject: Subject
    average_score: float = Field(ge=0, le=10)
    topic_scores: List[TopicScore] = Field(default_factory=list)
    test_count: int = Field(default=0)


class TestResult(BaseModel):
    """Individual test/exam result"""
    test_id: str
    subject: Subject
    topic_id: Optional[str] = None
    topic_name: Optional[str] = None
    score: float = Field(ge=0, le=10)
    max_score: float = Field(default=10)
    difficulty: str = Field(default="medium", description="easy, medium, hard")
    test_date: date
    test_type: str = Field(default="quiz", description="quiz, midterm, final, mock_exam")


class AcademicData(BaseModel):
    """Complete academic data for a student"""
    test_results: List[TestResult] = Field(default_factory=list)
    subject_scores: List[SubjectScore] = Field(default_factory=list)
    gpa: Optional[float] = Field(default=None, ge=0, le=10)
    class_rank: Optional[int] = None
    total_students_in_class: Optional[int] = None


class CareerGoal(BaseModel):
    """Student's career/academic goal"""
    field: str = Field(description="e.g., 'AI', 'Y khoa', 'Kinh te'")
    target_university: Optional[str] = None
    target_score: Optional[float] = Field(default=None, ge=0, le=30)  # Total score for 3 subjects


class StudentProfile(BaseModel):
    """Complete student profile"""
    student_id: str
    name: str
    date_of_birth: Optional[date] = None
    grade_level: GradeLevel
    exam_block: Optional[ExamBlock] = None
    career_goal: Optional[CareerGoal] = None
    current_skills: List[str] = Field(default_factory=list, description="Current skills like programming, English, etc.")
    available_study_hours_per_week: float = Field(default=20, ge=0)
