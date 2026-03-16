# Test data module
from .mock_student import create_mock_student_data, MOCK_STUDENT_DATA
from .mock_timetable import create_mock_timetable, MOCK_TIMETABLE
from .mock_report_card import create_mock_report_card, MOCK_REPORT_CARD
from .mock_study_habits import create_mock_study_habits, MOCK_STUDY_HABITS

__all__ = [
    "create_mock_student_data",
    "MOCK_STUDENT_DATA",
    "create_mock_timetable",
    "MOCK_TIMETABLE",
    "create_mock_report_card",
    "MOCK_REPORT_CARD",
    "create_mock_study_habits",
    "MOCK_STUDY_HABITS",
]
