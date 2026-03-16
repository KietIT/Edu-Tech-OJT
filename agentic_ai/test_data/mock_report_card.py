"""
Mock report card (bảng điểm) for student Trịnh Vỹ Kiệt.

This simulates the current grade sheet data that will be received
from the backend in production. Scores are on 0-10 scale (Vietnamese standard).

INPUT FIELD #2: Current Report Card (Bảng điểm hiện tại)
- Purpose: Assess student abilities and identify knowledge gaps
- Source: Backend API (from school database)
- Contains: Subject scores for the current semester/year
"""
from typing import Dict, Any, List


def create_mock_report_card() -> Dict[str, Any]:
    """
    Create mock report card data for Trịnh Vỹ Kiệt (12A2).

    Vietnamese grading types:
    - Điểm miệng (oral): weight 1
    - Điểm 15 phút (15-min test): weight 1
    - Điểm 1 tiết (45-min test): weight 2
    - Điểm giữa kỳ (midterm): weight 2
    - Điểm cuối kỳ (final): weight 3
    """
    return {
        "student_id": "STU_2024_001",
        "student_name": "Trịnh Vỹ Kiệt",
        "class": "12A2",
        "school_year": "2025-2026",
        "semester": 1,
        "subjects": [
            {
                "subject_code": "TO",
                "subject_name": "Toán",
                "scores": {
                    "diem_mieng": [8.0, 9.0],
                    "diem_15_phut": [8.5, 9.0, 7.5],
                    "diem_1_tiet": [8.0, 9.0],
                    "diem_giua_ky": 8.5,
                    "diem_cuoi_ky": 9.0,
                },
                "average_score": 8.6,
                "classification": "Giỏi",
            },
            {
                "subject_code": "VL",
                "subject_name": "Vật Lý",
                "scores": {
                    "diem_mieng": [6.0, 7.0],
                    "diem_15_phut": [5.5, 6.5, 7.0],
                    "diem_1_tiet": [6.0, 5.5],
                    "diem_giua_ky": 6.0,
                    "diem_cuoi_ky": 6.5,
                },
                "average_score": 6.2,
                "classification": "Trung bình",
            },
            {
                "subject_code": "NV",
                "subject_name": "Ngữ Văn",
                "scores": {
                    "diem_mieng": [7.0, 7.5],
                    "diem_15_phut": [7.0, 7.5, 8.0],
                    "diem_1_tiet": [7.5, 7.0],
                    "diem_giua_ky": 7.5,
                    "diem_cuoi_ky": 7.0,
                },
                "average_score": 7.3,
                "classification": "Khá",
            },
            {
                "subject_code": "TA",
                "subject_name": "Tiếng Anh",
                "scores": {
                    "diem_mieng": [7.5, 8.0],
                    "diem_15_phut": [7.0, 8.0, 7.5],
                    "diem_1_tiet": [7.5, 8.0],
                    "diem_giua_ky": 7.5,
                    "diem_cuoi_ky": 8.0,
                },
                "average_score": 7.7,
                "classification": "Khá",
            },
            {
                "subject_code": "KTPL",
                "subject_name": "Kinh tế và Pháp luật",
                "scores": {
                    "diem_mieng": [7.0, 7.5],
                    "diem_15_phut": [7.0, 6.5],
                    "diem_1_tiet": [7.0],
                    "diem_giua_ky": 7.0,
                    "diem_cuoi_ky": 7.5,
                },
                "average_score": 7.1,
                "classification": "Khá",
            },
            {
                "subject_code": "SU",
                "subject_name": "Lịch Sử",
                "scores": {
                    "diem_mieng": [6.5],
                    "diem_15_phut": [6.0, 7.0],
                    "diem_1_tiet": [6.5],
                    "diem_giua_ky": 6.5,
                    "diem_cuoi_ky": 7.0,
                },
                "average_score": 6.6,
                "classification": "Trung bình",
            },
            {
                "subject_code": "TI",
                "subject_name": "Tin học",
                "scores": {
                    "diem_mieng": [8.0],
                    "diem_15_phut": [8.5, 9.0],
                    "diem_1_tiet": [8.5],
                    "diem_giua_ky": 8.0,
                    "diem_cuoi_ky": 8.5,
                },
                "average_score": 8.4,
                "classification": "Giỏi",
            },
            {
                "subject_code": "TD",
                "subject_name": "Thể dục",
                "scores": {
                    "diem_mieng": [],
                    "diem_15_phut": [],
                    "diem_1_tiet": [],
                    "diem_giua_ky": None,
                    "diem_cuoi_ky": None,
                },
                "average_score": None,
                "classification": "Đạt",
            },
            {
                "subject_code": "CNNN",
                "subject_name": "Công nghệ",
                "scores": {
                    "diem_mieng": [7.5],
                    "diem_15_phut": [7.0, 7.5],
                    "diem_1_tiet": [7.0],
                    "diem_giua_ky": 7.5,
                    "diem_cuoi_ky": 7.0,
                },
                "average_score": 7.2,
                "classification": "Khá",
            },
            {
                "subject_code": "QP",
                "subject_name": "Giáo dục Quốc phòng",
                "scores": {
                    "diem_mieng": [7.0],
                    "diem_15_phut": [7.5],
                    "diem_1_tiet": [7.0],
                    "diem_giua_ky": 7.0,
                    "diem_cuoi_ky": 7.5,
                },
                "average_score": 7.2,
                "classification": "Khá",
            },
            {
                "subject_code": "GDDP",
                "subject_name": "Giáo dục địa phương",
                "scores": {
                    "diem_mieng": [7.0],
                    "diem_15_phut": [7.5],
                    "diem_1_tiet": [7.0],
                    "diem_giua_ky": None,
                    "diem_cuoi_ky": 7.5,
                },
                "average_score": 7.3,
                "classification": "Khá",
            },
        ],
        "gpa": 7.5,
        "overall_classification": "Khá",
        "class_rank": 12,
        "total_students_in_class": 42,
        "teacher_comment": "Học sinh có năng lực tốt ở môn Toán và Tin học. Cần cải thiện Vật Lý và Lịch Sử.",
    }


# Convenience constant
MOCK_REPORT_CARD = create_mock_report_card()
