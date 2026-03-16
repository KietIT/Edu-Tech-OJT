"""
Mock study habits and available time slots for student Trịnh Vỹ Kiệt.

This simulates the student's study preferences and free time data
that will be received from the backend in production.

INPUT FIELD #3: Study Habits & Time Slots (Thói quen học tập & khung giờ)
- Purpose: Know when the student can concentrate best on studying
- Source: Backend API (from student survey/questionnaire)
- Contains: Preferred study times, concentration patterns, habits
"""
from typing import Dict, Any, List


def create_mock_study_habits() -> Dict[str, Any]:
    """
    Create mock study habits and time slot data for Trịnh Vỹ Kiệt (12A2).

    Time slots are expressed as available windows outside of school hours.
    School schedule reference (from TKB.xlsx):
    - Morning session (Buổi sáng): ~7:00 - 11:30
    - Afternoon session (Buổi chiều): ~13:00 - 17:00
    """
    return {
        "student_id": "STU_2024_001",
        "student_name": "Trịnh Vỹ Kiệt",

        # --- Study Preferences ---
        "study_preferences": {
            "preferred_study_duration_minutes": 45,
            "preferred_break_duration_minutes": 10,
            "max_continuous_study_hours": 2.0,
            "preferred_study_environment": "Phòng riêng, yên tĩnh",
            "preferred_study_method": [
                "Làm bài tập",
                "Xem video bài giảng",
                "Ghi chú tóm tắt",
            ],
            "learns_best_time_of_day": "tối",  # sáng / chiều / tối
        },

        # --- Concentration Patterns ---
        "concentration": {
            "best_focus_time": "20:00-22:00",
            "average_focus_duration_minutes": 40,
            "easily_distracted_by": ["Điện thoại", "Mạng xã hội"],
            "focus_rating_self_assessed": 6,  # 1-10
        },

        # --- Weekly Available Time Slots ---
        # Each day lists free time windows when the student CAN study
        # (already excluding school timetable from TKB.xlsx)
        "weekly_available_slots": {
            "thu_2": {
                "school_sessions": ["S", "C"],  # Both morning and afternoon
                "free_slots": [
                    {"start": "17:30", "end": "19:00", "quality": "trung bình"},
                    {"start": "19:30", "end": "22:00", "quality": "tốt"},
                ],
                "total_free_study_hours": 3.0,
            },
            "thu_3": {
                "school_sessions": ["S", "C"],
                "free_slots": [
                    {"start": "17:30", "end": "19:00", "quality": "trung bình"},
                    {"start": "19:30", "end": "22:00", "quality": "tốt"},
                ],
                "total_free_study_hours": 3.0,
            },
            "thu_4": {
                "school_sessions": ["S", "C"],
                "free_slots": [
                    {"start": "17:30", "end": "19:00", "quality": "trung bình"},
                    {"start": "19:30", "end": "22:00", "quality": "tốt"},
                ],
                "total_free_study_hours": 3.0,
            },
            "thu_5": {
                "school_sessions": ["S", "C"],
                "free_slots": [
                    {"start": "17:30", "end": "19:00", "quality": "trung bình"},
                    {"start": "19:30", "end": "22:00", "quality": "tốt"},
                ],
                "total_free_study_hours": 3.0,
            },
            "thu_6": {
                "school_sessions": ["S"],  # Only morning, afternoon free
                "free_slots": [
                    {"start": "13:00", "end": "15:00", "quality": "trung bình"},
                    {"start": "15:30", "end": "17:00", "quality": "trung bình"},
                    {"start": "19:30", "end": "22:00", "quality": "tốt"},
                ],
                "total_free_study_hours": 5.0,
            },
            "thu_7": {
                "school_sessions": [],  # Completely free
                "free_slots": [
                    {"start": "08:00", "end": "11:00", "quality": "tốt"},
                    {"start": "14:00", "end": "16:30", "quality": "trung bình"},
                    {"start": "19:30", "end": "22:00", "quality": "tốt"},
                ],
                "total_free_study_hours": 8.0,
            },
            "chu_nhat": {
                "school_sessions": [],  # Completely free
                "free_slots": [
                    {"start": "09:00", "end": "11:00", "quality": "trung bình"},
                    {"start": "14:00", "end": "16:00", "quality": "trung bình"},
                    {"start": "19:30", "end": "21:30", "quality": "tốt"},
                ],
                "total_free_study_hours": 6.0,
            },
        },
        "total_weekly_study_hours": 31.0,

        # --- Current Study Habits ---
        "current_habits": {
            "study_days_per_week": 6,
            "average_daily_study_hours": 2.5,
            "does_homework_regularly": True,
            "reviews_before_class": False,
            "reviews_after_class": True,
            "uses_study_plan": False,
            "has_tutor": True,
            "tutor_subjects": ["Toán"],
            "tutor_schedule": "Thứ 7, 8:00-10:00",
            "self_study_subjects_priority": ["Toán", "Tiếng Anh", "Vật Lý"],
        },

        # --- Extracurricular & Constraints ---
        "constraints": {
            "dinner_time": "19:00-19:30",
            "bedtime": "22:30",
            "wake_up_time": "06:00",
            "extracurricular_activities": [
                {
                    "activity": "CLB Tin học",
                    "day": "thu_7",
                    "time": "14:00-16:00",
                },
            ],
            "family_obligations": "Phụ giúp gia đình Chủ Nhật sáng",
        },
    }


# Convenience constant
MOCK_STUDY_HABITS = create_mock_study_habits()
