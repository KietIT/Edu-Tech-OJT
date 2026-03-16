"""
Mock school timetable (thời khóa biểu) for student Trịnh Vỹ Kiệt.

This simulates the parsed school schedule data that will be received
from the backend in production (originally from TKB.xlsx).

INPUT FIELD #1: School Timetable (Thời khóa biểu cố định)
- Purpose: Know which time slots are OCCUPIED by school classes
- Source: Backend API (parsed from school's .xlsx timetable)
- Contains: Day-by-day, session-by-session class schedule
"""
from typing import Dict, Any, List


def create_mock_timetable() -> Dict[str, Any]:
    """
    Create mock timetable data for Trịnh Vỹ Kiệt (12A2).

    Parsed from TKB.xlsx. Structure:
    - Thứ 2-7 (Monday=2 to Saturday=7)
    - Buổi S (Sáng/Morning 7:00-11:30), C (Chiều/Afternoon 13:00-17:00)
    - Tiết 1-5 (periods)

    Subject code mapping:
    - TO = Toán, VL = Vật Lý, NV = Ngữ Văn, TA = Tiếng Anh
    - KTPL = Kinh tế Pháp luật, SU = Lịch Sử, TI = Tin học
    - TD = Thể dục, CNNN = Công nghệ, QP = Quốc phòng
    - GDDP = Giáo dục địa phương, HDTT = Hoạt động trải nghiệm
    - TrN = Trải nghiệm
    """
    return {
        "student_id": "STU_2024_001",
        "student_name": "Trịnh Vỹ Kiệt",
        "class": "12A2",
        "school_year": "2025-2026",
        "semester": 1,

        # Time definitions for each session
        "session_times": {
            "S": {"start": "07:00", "end": "11:30", "label": "Buổi sáng"},
            "C": {"start": "13:00", "end": "17:00", "label": "Buổi chiều"},
        },

        # Period time mapping
        "period_times": {
            "S": {
                1: {"start": "07:00", "end": "07:45"},
                2: {"start": "07:55", "end": "08:40"},
                3: {"start": "09:00", "end": "09:45"},
                4: {"start": "09:55", "end": "10:40"},
                5: {"start": "10:50", "end": "11:30"},
            },
            "C": {
                1: {"start": "13:00", "end": "13:45"},
                2: {"start": "13:55", "end": "14:40"},
                3: {"start": "15:00", "end": "15:45"},
                4: {"start": "15:55", "end": "16:40"},
                5: {"start": "16:50", "end": "17:30"},
            },
        },

        # Weekly schedule: day -> session -> list of (period, subject_code, subject_name)
        "schedule": {
            "thu_2": {
                "S": [
                    {"period": 1, "code": "HDTT", "name": "Hoạt động trải nghiệm"},
                    {"period": 2, "code": "GDDP", "name": "Giáo dục địa phương"},
                    {"period": 3, "code": "TrN", "name": "Trải nghiệm"},
                    {"period": 4, "code": "TrN", "name": "Trải nghiệm"},
                ],
                "C": [
                    {"period": 3, "code": "TA", "name": "Tiếng Anh"},
                    {"period": 4, "code": "TA", "name": "Tiếng Anh"},
                    {"period": 5, "code": "KTPL", "name": "Kinh tế Pháp luật"},
                ],
            },
            "thu_3": {
                "S": [
                    {"period": 1, "code": "TD", "name": "Thể dục"},
                    {"period": 2, "code": "KTPL", "name": "Kinh tế Pháp luật"},
                    {"period": 3, "code": "SU", "name": "Lịch Sử"},
                    {"period": 4, "code": "TO", "name": "Toán"},
                    {"period": 5, "code": "TO", "name": "Toán"},
                ],
                "C": [
                    {"period": 3, "code": "TA", "name": "Tiếng Anh"},
                    {"period": 4, "code": "TA", "name": "Tiếng Anh"},
                    {"period": 5, "code": "QP", "name": "Quốc phòng"},
                ],
            },
            "thu_4": {
                "S": [
                    {"period": 1, "code": "VL", "name": "Vật Lý"},
                    {"period": 2, "code": "TO", "name": "Toán"},
                    {"period": 3, "code": "TO", "name": "Toán"},
                    {"period": 4, "code": "TI", "name": "Tin học"},
                    {"period": 5, "code": "TI", "name": "Tin học"},
                ],
                "C": [
                    {"period": 3, "code": "CNNN", "name": "Công nghệ"},
                    {"period": 4, "code": "CNNN", "name": "Công nghệ"},
                    {"period": 5, "code": "NV", "name": "Ngữ Văn"},
                ],
            },
            "thu_5": {
                "S": [
                    {"period": 1, "code": "TD", "name": "Thể dục"},
                    {"period": 2, "code": "TA", "name": "Tiếng Anh"},
                    {"period": 3, "code": "TA", "name": "Tiếng Anh"},
                    {"period": 4, "code": "VL", "name": "Vật Lý"},
                    {"period": 5, "code": "VL", "name": "Vật Lý"},
                ],
                "C": [
                    {"period": 3, "code": "NV", "name": "Ngữ Văn"},
                    {"period": 4, "code": "NV", "name": "Ngữ Văn"},
                ],
            },
            "thu_6": {
                "S": [
                    {"period": 1, "code": "NV", "name": "Ngữ Văn"},
                    {"period": 2, "code": "TO", "name": "Toán"},
                    {"period": 3, "code": "TO", "name": "Toán"},
                    {"period": 4, "code": "GDDP", "name": "Giáo dục địa phương"},
                    {"period": 5, "code": "TrN", "name": "Trải nghiệm"},
                ],
                "C": [],
            },
            "thu_7": {
                "S": [],
                "C": [],
            },
            "chu_nhat": {
                "S": [],
                "C": [],
            },
        },
    }


# Convenience constant
MOCK_TIMETABLE = create_mock_timetable()
