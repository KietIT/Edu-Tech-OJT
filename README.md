# Edu-Tech: Timetable Analyzer

Hệ thống phân tích thời khóa biểu và tạo lịch học bổ sung cho học sinh THPT Việt Nam. Hệ thống nhận 6 trường dữ liệu đầu vào, xác định các môn yếu, và tạo lịch học bổ sung hàng tuần tránh xung đột với giờ học trên lớp.

## Tổng quan kiến trúc

```
Frontend (React/Next.js)          Backend (FastAPI)           Analyzer Engine
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│  Form nhập liệu  │  POST   │  /api/analyze    │  call   │ TimetableAnalyzer│
│  Hiển thị lịch   │ ──────> │  Validate input  │ ──────> │ Deterministic    │
│  học bổ sung     │ <────── │  Return JSON     │ <────── │ (no API call)    │
└──────────────────┘  JSON   └──────────────────┘  dict   └──────────────────┘
```

**Quan trọng**: Core engine hiện tại hoạt động **hoàn toàn deterministic** (không gọi LLM API).

## Cấu trúc thư mục

```
agentic_ai/
├── __init__.py              # Package exports: generate_learning_path, generate_learning_path_from_dict
├── main.py                  # Entry point chính - 2 hàm API
├── config.py                # Cấu hình: thresholds, scoring settings
├── show_result.py           # Hiển thị kết quả trên terminal
├── run_test.py              # Script test với mock data
├── requirements.txt         # Python dependencies
├── agents/
│   ├── __init__.py          # Exports: TimetableAnalyzer, AgentContext, BaseAgent
│   ├── base.py              # AgentContext (input container) + BaseAgent (abstract)
│   └── timetable_analyzer.py # Core logic: xác định môn yếu + tạo lịch
├── schemas/
│   ├── __init__.py
│   ├── student.py           # StudentProfile, AcademicData, SubjectScore, ExamBlock
│   ├── psychology.py        # PsychologyData, MSLQ, Big Five, VARK, MentalHealth
│   ├── paths.py             # WeeklyStudySchedule, ScheduleEntry + legacy schemas
│   └── output.py            # AnalysisResult, WeakSubjectInfo (final output schema)
├── test_data/
│   ├── __init__.py
│   ├── mock_student.py      # Mock student profiles (3 profiles)
│   ├── mock_timetable.py    # Mock school timetable (TKB)
│   ├── mock_report_card.py  # Mock semester grades (bảng điểm)
│   └── mock_study_habits.py # Mock study habits & time slots
└── doc/
    ├── agentic-ai.md        # System design document
    ├── new-requirement.md   # Requirements for weekly schedule feature
    ├── hanh-vi-hoc-tap.md   # Learning behavior questionnaire spec
    ├── tam-sinh-li.md       # Mental health assessment spec
    └── tutorial.md          # Setup tutorial
```

## Cài đặt

```bash
# Clone repo
git clone <repo-url>
cd Edu-Tech

# Tạo virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Cài dependencies
pip install -r agentic_ai/requirements.txt
```

### Environment Variables (Optional)

Có thể tạo file `agentic_ai/.env` để override ngưỡng:

```env
WEAK_TOPIC_THRESHOLD=8.0
MINIMUM_SUBJECT_SCORE=8.0
LOW_THRESHOLD=3.0
HIGH_THRESHOLD=5.0
```

## Cách sử dụng

### 1. Chạy test nhanh

```bash
cd Edu-Tech
python -m agentic_ai.run_test
```

Kết quả sẽ in ra terminal và lưu vào `output_test_results.json`.

### 2. Gọi từ Python code

```python
from agentic_ai.main import generate_learning_path, generate_learning_path_from_dict

# Option A: Truyền Pydantic objects
result = generate_learning_path(
    student_profile=student_profile,   # StudentProfile
    academic_data=academic_data,       # AcademicData
    psychology_data=psychology_data,   # PsychologyData
    timetable=timetable,               # Dict (optional)
    report_card=report_card,           # Dict (optional)
    study_habits=study_habits,         # Dict (optional)
)

# Option B: Truyền dict/JSON (cho API integration)
result = generate_learning_path_from_dict(data)
```

### 3. Tích hợp với Backend (FastAPI)

```python
from fastapi import FastAPI
from agentic_ai.main import generate_learning_path_from_dict

app = FastAPI()

@app.post("/api/analyze")
async def analyze(data: dict):
    result = generate_learning_path_from_dict(data)
    return result
```

## Input / Output Specification

### Input: 6 trường dữ liệu

| # | Field | Type | Required | Mô tả |
|---|-------|------|----------|-------|
| 1 | `student_profile` | `StudentProfile` | Yes | Thông tin học sinh: tên, lớp, khối thi, mục tiêu |
| 2 | `academic_data` | `AcademicData` | Yes | Kết quả học tập: điểm từng môn, topic scores |
| 3 | `psychology_data` | `PsychologyData` | Yes | Đánh giá tâm lý: MSLQ, Big Five, VARK, sức khỏe tâm thần |
| 4 | `timetable` | `Dict` | No | Thời khóa biểu trường (hiện chưa dùng trực tiếp) |
| 5 | `report_card` | `Dict` | No | Bảng điểm học kỳ từ trường |
| 6 | `study_habits` | `Dict` | No | Thói quen học tập & khung giờ rảnh |


### Output: `AnalysisResult`

```json
{
  "student_id": "STU_2024_001",
  "student_name": "Trịnh Vỹ Kiệt",
  "generated_at": "2026-03-05T14:39:50.255872",

  "weekly_study_schedule": {
    "schedule_id": "schedule_STU_2024_001_a412e14d",
    "student_name": "Trịnh Vỹ Kiệt",
    "entries": [
      {
        "day": "Thứ 2",
        "day_key": "thu_2",
        "start": "19:30",
        "end": "22:00",
        "subject": "Lý",
        "topics": ["Cơ học", "Nhiệt học", "Điện học"],
        "activity": "Học lý thuyết + Làm bài tập",
        "duration_minutes": 150,
        "slot_quality": "tốt",
        "notes": ""
      }
    ],
    "total_supplementary_hours": 36.0,
    "weak_subjects_covered": ["Lý", "Hóa", "Văn", "Anh"],
    "notes": [
      "Giờ ăn tối: 19:00-19:30",
      "Tập trung tốt nhất: 20:00-22:00",
      "Lịch học bổ sung này đã tránh toàn bộ giờ học trên lớp"
    ]
  },

  "weak_subjects_analysis": [
    {
      "subject": "Lý",
      "average_score": 6.44,
      "gap": 1.56,
      "weak_topics": ["Cơ học", "Nhiệt học", "Điện học", "Quang học"],
      "source": "academic_data",
      "classification": "Trung bình"
    }
  ],

  "ai_summary": null,
  "processing_time_seconds": 0.0003,
  "version": "2.0.0"
}
```

### Chi tiết format input data

#### `student_profile`
```json
{
  "student_id": "STU_2024_001",
  "name": "Trịnh Vỹ Kiệt",
  "date_of_birth": "2005-03-09",
  "grade_level": "12",
  "exam_block": "A01",
  "career_goal": {
    "field": "AI",
    "target_university": "Đại học FPT",
    "target_score": 27.0
  },
  "current_skills": ["Python cơ bản", "Tiếng Anh B1"],
  "available_study_hours_per_week": 25.0
}
```

- `grade_level`: "9", "10", "11", "12"
- `exam_block`: "A00" (Toán,Lý,Hóa), "A01" (Toán,Lý,Anh), "B00" (Toán,Hóa,Sinh), "C00" (Văn,Sử,Địa), "D01" (Toán,Văn,Anh), "D07" (Toán,Hóa,Anh)
- `target_score`: Tổng điểm 3 môn, max 30

#### `academic_data`
```json
{
  "subject_scores": [
    {
      "subject": "ly",
      "average_score": 6.44,
      "topic_scores": [
        {
          "topic_id": "ly_01",
          "topic_name": "Cơ học",
          "score": 6.5,
          "max_score": 10,
          "is_core_topic": true,
          "exam_frequency": 0.85
        }
      ],
      "test_count": 10
    }
  ],
  "test_results": [
    {
      "test_id": "test_001",
      "subject": "ly",
      "topic_id": "ly_03",
      "topic_name": "Điện học",
      "score": 5.5,
      "max_score": 10,
      "difficulty": "medium",
      "test_date": "2024-09-20",
      "test_type": "quiz"
    }
  ],
  "gpa": 7.8,
  "class_rank": 8,
  "total_students_in_class": 45
}
```

- `subject` enum values: `toan`, `van`, `anh`, `ly`, `hoa`, `sinh`, `su`, `dia`, `gdcd`, `tin`, `cong_nghe`
- Tất cả `score` và `average_score`: **0-10**

#### `report_card`
```json
{
  "semester": "HK1",
  "school_year": "2024-2025",
  "subjects": [
    {
      "subject_name": "Vật Lý",
      "subject_code": "LY",
      "average_score": 6.5,
      "classification": "Trung bình"
    }
  ],
  "overall_gpa": 7.3,
  "overall_classification": "Khá",
  "conduct": "Tốt"
}
```

#### `study_habits`
```json
{
  "student_id": "STU_2024_001",
  "concentration": {
    "best_focus_time": "20:00-22:00",
    "average_focus_duration_minutes": 40
  },
  "weekly_available_slots": {
    "thu_2": {
      "school_sessions": ["S", "C"],
      "free_slots": [
        {"start": "17:30", "end": "19:00", "quality": "trung bình"},
        {"start": "19:30", "end": "22:00", "quality": "tốt"}
      ],
      "total_free_study_hours": 3.0
    }
  },
  "constraints": {
    "dinner_time": "19:00-19:30",
    "bedtime": "22:30"
  }
}
```

- Day keys: `thu_2`, `thu_3`, `thu_4`, `thu_5`, `thu_6`, `thu_7`, `chu_nhat`
- `quality`: `"tốt"` hoặc `"trung bình"`
- `school_sessions`: `"S"` = sáng, `"C"` = chiều

## Core Logic

### 1. Xác định môn yếu (`_identify_weak_subjects`)

- Threshold: `8.0/10` (configurable trong `config.py`)
- Sources: `academic_data.subject_scores` + `report_card.subjects`
- Output: Danh sách môn yếu, sort theo gap lớn nhất

### 2. Tạo lịch học bổ sung (`_build_weekly_schedule`)

- Lấy free time slots từ `study_habits.weekly_available_slots`
- Phân phối môn yếu theo trọng số gap (gap lớn = nhiều slot hơn)
- Ưu tiên slot chất lượng "tốt" cho học lý thuyết + bài tập
- Slot "trung bình" dùng cho ôn tập + bài tập nhẹ
- Bỏ qua slot < 30 phút

### 3. AI Summary

Trường `ai_summary` trong output hiện được giữ ở `null` để tương thích schema.

## Thang điểm & Config

| Setting | Value | Mô tả |
|---------|-------|-------|
| `WEAK_TOPIC_THRESHOLD` | 8.0 | Dưới 8.0/10 = môn yếu |
| `MINIMUM_SUBJECT_SCORE` | 8.0 | Điểm tối thiểu môn không thi |
| Scoring scale | 0-10 | Thang điểm Việt Nam |
| `target_score` (career goal) | 0-30 | Tổng 3 môn x 10 |

## Cho team Backend

### Tích hợp API

1. Wrap `generate_learning_path_from_dict()` trong FastAPI endpoint
2. Input: JSON body chứa 6 fields như trên
3. Output: JSON `AnalysisResult`
4. Không cần API key (core engine deterministic)
5. Processing time: < 1ms (no network calls)

### Validation

Tất cả input đã được validate bởi Pydantic schemas. Nếu data sai format sẽ raise `ValidationError` với message chi tiết.

### Mở rộng

- Thêm subjects mới: edit `Subject` enum trong `schemas/student.py`
- Thay đổi threshold: edit `config.py`
- Tinh chỉnh logic phân bổ slot: edit `_build_weekly_schedule()` trong `agents/timetable_analyzer.py`

## Cho team Frontend

### Dữ liệu cần thu thập từ UI

1. **Thông tin học sinh**: tên, lớp, khối thi, mục tiêu nghề nghiệp
2. **Điểm học tập**: điểm từng môn, từng chủ đề (thang 10)
3. **Bảng điểm học kỳ**: điểm trung bình các môn từ trường
4. **Đánh giá tâm lý**: MSLQ (1-7), Big Five (0-1), VARK (0-100)
5. **Thời khóa biểu**: giờ học trên lớp từng ngày
6. **Thói quen học tập**: khung giờ rảnh, thời gian tập trung tốt nhất

### Hiển thị kết quả

Primary output là `weekly_study_schedule.entries` - mảng các buổi học:

| Field | Mô tả | Ví dụ |
|-------|-------|-------|
| `day` | Tên thứ (tiếng Việt) | "Thứ 2" |
| `start`, `end` | Giờ bắt đầu/kết thúc | "19:30", "22:00" |
| `subject` | Tên môn cần học | "Lý" |
| `topics` | Chủ đề cụ thể | ["Cơ học", "Điện học"] |
| `activity` | Loại hoạt động | "Học lý thuyết + Làm bài tập" |
| `slot_quality` | Chất lượng tập trung | "tốt" / "trung bình" |

Secondary: `weak_subjects_analysis` - danh sách môn yếu với điểm và gap.

## Mock Data

3 mock student profiles có sẵn để test:

```python
from agentic_ai.test_data.mock_student import (
    create_mock_student_data,           # Default: Trịnh Vỹ Kiệt (12A2, A01)
    create_mock_student_high_achiever,  # Tran Thi B (12, A00, high scores)
    create_mock_student_struggling,     # Le Van C (10, D01, low scores)
)
```

## Tech Stack

- **Python** 3.11+
- **Pydantic** v2 - Data validation & schemas
- **FastAPI** - Recommended for API layer (not included, BE team implements)
