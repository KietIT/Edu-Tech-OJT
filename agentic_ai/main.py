"""
Main entry point for the Timetable Analyzer system.

Simplified from the 3-agent architecture to a single analyzer
that produces a supplementary study schedule for weak subjects.
"""
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from .agents import TimetableAnalyzer, AgentContext
from .schemas.student import StudentProfile, AcademicData
from .schemas.psychology import PsychologyData

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_learning_path(
    student_profile: StudentProfile,
    academic_data: AcademicData,
    psychology_data: PsychologyData,
    timetable: Optional[Dict[str, Any]] = None,
    report_card: Optional[Dict[str, Any]] = None,
    study_habits: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze student data and generate a supplementary study schedule.

    This is the main API for the system. It:
    1. Creates a context from the 3 input fields
    2. Runs the TimetableAnalyzer (deterministic analysis)
    3. Returns the weekly study schedule + weak subjects analysis

    Args:
        student_profile: Student profile (name, grade, exam block, etc.)
        academic_data: Academic records (test results, subject scores)
        psychology_data: Psychology assessment results
        timetable: School timetable (thời khóa biểu)
        report_card: Current semester grades (bảng điểm)
        study_habits: Study habits and available time slots

    Returns:
        Dict containing:
        - student_id, student_name, generated_at
        - weekly_study_schedule: the supplementary timetable
        - weak_subjects_analysis: identified weak subjects
        - ai_summary: None (reserved for future use)
        - processing_time_seconds
    """
    logger.info(f"Starting analysis for student: {student_profile.student_id}")

    # Create context
    context = AgentContext(
        student_profile=student_profile,
        academic_data=academic_data,
        psychology_data=psychology_data,
        timetable=timetable,
        report_card=report_card,
        study_habits=study_habits,
        request_id=request_id or f"req_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        timestamp=datetime.utcnow()
    )

    # Run analyzer
    analyzer = TimetableAnalyzer()
    result = analyzer.analyze(context)

    logger.info(f"Analysis completed for student: {student_profile.student_id}")
    return result


def generate_learning_path_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate analysis from dictionary input.

    Convenience function for API integration where data comes as JSON/dict.

    Args:
        data: Dict containing:
            - student_profile: Student profile data
            - academic_data: Academic records
            - psychology_data: Psychology assessment
            - timetable: School timetable (optional)
            - report_card: Current grades (optional)
            - study_habits: Study habits and time slots (optional)

    Returns:
        Same as generate_learning_path()
    """
    student_profile = StudentProfile(**data["student_profile"])
    academic_data = AcademicData(**data["academic_data"])
    psychology_data = PsychologyData(**data["psychology_data"])

    return generate_learning_path(
        student_profile=student_profile,
        academic_data=academic_data,
        psychology_data=psychology_data,
        timetable=data.get("timetable"),
        report_card=data.get("report_card"),
        study_habits=data.get("study_habits"),
        request_id=data.get("request_id")
    )


# Export main functions
__all__ = [
    "generate_learning_path",
    "generate_learning_path_from_dict",
]
