# ĐẶC TẢ KỸ THUẬT – HỆ THỐNG PHÂN TÍCH THỜI KHÓA BIỂU (Edu-Tech OJT)

## Mục lục

1. [Mục tiêu hệ thống](#1-mục-tiêu-hệ-thống)
2. [Kiến trúc tổng thể](#2-kiến-trúc-tổng-thể)
3. [Cấu trúc thư mục](#3-cấu-trúc-thư-mục)
4. [Công nghệ sử dụng](#4-công-nghệ-sử-dụng)
5. [Cài đặt & Khởi chạy](#5-cài-đặt--khởi-chạy)
6. [Đặc tả Input / Output](#6-đặc-tả-input--output)
7. [Logic xử lý cốt lõi](#7-logic-xử-lý-cốt-lõi)
8. [Cấu hình & Thang điểm](#8-cấu-hình--thang-điểm)
9. [Hướng dẫn tích hợp](#9-hướng-dẫn-tích-hợp)
10. [Tài liệu liên quan](#10-tài-liệu-liên-quan)

---

## 1. MỤC TIÊU HỆ THỐNG

### 1.1 Mục tiêu chức năng

Hệ thống phân tích thời khóa biểu và tạo **lịch học bổ sung cá nhân hóa** cho học sinh THPT Việt Nam.  
Dựa trên 3 điều kiện đầu vào cốt lõi, hệ thống:

1. **Phân tích bảng điểm** – Xác định các môn và chủ đề học sinh còn yếu (dưới ngưỡng `8.0/10`).
2. **Đối chiếu thời khóa biểu** – Tránh xung đột giữa lịch học bổ sung và giờ học trên lớp.
3. **Tổng hợp kết quả** – Tạo lịch học bổ sung hàng tuần ở dạng JSON có cấu trúc cho frontend / backend sử dụng.

### 1.2 Mục tiêu phi chức năng

- **Hiệu năng**: Thời gian xử lý thường < 1ms (core engine deterministic, không gọi API).
- **Khả năng mở rộng**: Dễ bổ sung môn học mới, thay đổi ngưỡng điểm, enable AI summary.
- **Tích hợp**: Thiết kế dưới dạng thư viện Python – dễ wrap vào FastAPI hoặc bất kỳ backend nào.
- **Bảo mật**: Core engine không gửi dữ liệu học sinh ra ngoài (không gọi LLM API ở v2).

---

## 2. KIẾN TRÚC TỔNG THỂ

### 2.1 Sơ đồ luồng xử lý

```
Frontend (React/Next.js)          Backend (FastAPI)           Analyzer Engine
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│  Form nhập liệu  │  POST   │  /api/analyze    │  call   │ TimetableAnalyzer│
│  Hiển thị lịch   │ ──────> │  Validate input  │ ──────> │ Deterministic    │
│  học bổ sung     │ <────── │  Return JSON     │ <────── │ (no API call)    │
└──────────────────┘  JSON   └──────────────────┘  dict   └──────────────────┘
```

**Quan trọng**: Core engine hiện tại hoạt động **hoàn toàn deterministic** (không gọi LLM API).  
Trường `ai_summary` trong output được reserved cho tính năng tương lai.

### 2.2 Mô hình xử lý nội bộ

```
Input (6 trường)
       │
       ▼
AgentContext  ←── Pydantic validation
       │
       ▼
TimetableAnalyzer
  ├── _identify_weak_subjects()   ←── academic_data + report_card
  └── _build_weekly_schedule()   ←── study_habits (free slots)
       │
       ▼
AnalysisResult (JSON)
  ├── weekly_study_schedule
  └── weak_subjects_analysis
```

---

## 3. CẤU TRÚC THƯ MỤC

```
Edu-Tech-OJT/
├── README.md
├── TKB.xlsx                     # Ví dụ thời khóa biểu mẫu
├── agentic_ai/
│   ├── __init__.py              # Package exports: generate_learning_path, generate_learning_path_from_dict
│   ├── main.py                  # Entry point chính – 2 hàm API
│   ├── config.py                # Cấu hình: thresholds, scoring settings
│   ├── llm_client.py            # Claude API client (singleton, chưa dùng trong v2)
│   ├── show_result.py           # Hiển thị kết quả trên terminal
│   ├── run_test.py              # Script test với mock data
│   ├── requirements.txt         # Python dependencies
│   ├── agents/
│   │   ├── __init__.py          # Exports: TimetableAnalyzer, AgentContext, BaseAgent
│   │   ├── base.py              # AgentContext (input container) + BaseAgent (abstract)
│   │   └── timetable_analyzer.py # Core logic: xác định môn yếu + tạo lịch
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── student.py           # StudentProfile, AcademicData, SubjectScore, ExamBlock
│   │   ├── psychology.py        # PsychologyData, MSLQ, Big Five, VARK, MentalHealth
│   │   ├── paths.py             # WeeklyStudySchedule, ScheduleEntry + legacy schemas
│   │   └── output.py            # AnalysisResult, WeakSubjectInfo (final output schema)
│   └── test_data/
│       ├── __init__.py
│       ├── mock_student.py      # Mock student profiles (3 profiles)
│       ├── mock_timetable.py    # Mock school timetable (TKB)
│       ├── mock_report_card.py  # Mock semester grades (bảng điểm)
│       └── mock_study_habits.py # Mock study habits & time slots
└── doc/
    ├── agentic-ai.md            # Đặc tả kỹ thuật hệ thống agentic AI
    ├── new-requirement.md       # Yêu cầu mới: tính năng lịch học hàng tuần
    ├── hanh-vi-hoc-tap.md       # Bộ câu hỏi hành vi học tập (MSLQ rút gọn)
    ├── tam-sinh-li.md           # Bộ câu hỏi đánh giá tâm sinh lý
    └── tutorial.md              # Hướng dẫn cài đặt & tích hợp chi tiết
```

---

## 4. CÔNG NGHỆ SỬ DỤNG

| Thành phần | Công nghệ | Ghi chú |
|------------|-----------|---------|
| Ngôn ngữ | **Python** 3.11+ | |
| Validation | **Pydantic** v2 | Data schemas & input validation |
| LLM (tương lai) | **Anthropic SDK** | Claude API – reserved cho `ai_summary` |
| API layer | **FastAPI** | Không bao gồm – do team Backend implement |
| Frontend | **React / Next.js** | Không bao gồm – do team Frontend implement |

---

## 5. CÀI ĐẶT & KHỞI CHẠY

### 5.1 Yêu cầu hệ thống

- Python 3.11 trở lên
- pip hoặc uv

### 5.2 Cài đặt

```bash
# Clone repo
git clone <repo-url>
cd Edu-Tech-OJT

# Tạo virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows

# Cài dependencies
pip install -r agentic_ai/requirements.txt
```

### 5.3 Cấu hình môi trường

Tạo file `agentic_ai/.env` (tùy chọn – chỉ cần khi enable AI summary):

```env
# Chưa cần thiết cho v2 (core engine không gọi API)
# Chỉ cần khi enable tính năng ai_summary trong tương lai
ANTHROPIC_API_KEY=sk-ant-...
LLM_PROVIDER=anthropic
LLM_MODEL=claude-sonnet-4-20250514
```

### 5.4 Chạy thử

```bash
# Chạy test nhanh với mock data
python -m agentic_ai.run_test
```

Kết quả sẽ in ra terminal và lưu vào `output_test_results.json`.

---

## 6. ĐẶC TẢ INPUT / OUTPUT

### 6.1 Input: 6 trường dữ liệu

| # | Trường | Kiểu dữ liệu | Bắt buộc | Mô tả |
|---|--------|--------------|----------|-------|
| 1 | `student_profile` | `StudentProfile` | ✅ | Thông tin học sinh: tên, lớp, khối thi, mục tiêu |
| 2 | `academic_data` | `AcademicData` | ✅ | Kết quả học tập: điểm từng môn, topic scores |
| 3 | `psychology_data` | `PsychologyData` | ✅ | Đánh giá tâm lý: MSLQ, Big Five, VARK, sức khỏe tâm thần |
| 4 | `timetable` | `Dict` | ❌ | Thời khóa biểu trường (hiện chưa dùng trực tiếp) |
| 5 | `report_card` | `Dict` | ❌ | Bảng điểm học kỳ từ trường |
| 6 | `study_habits` | `Dict` | ❌ | Thói quen học tập & khung giờ rảnh |

### 6.2 Chi tiết từng trường input

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

- `grade_level`: `"9"`, `"10"`, `"11"`, `"12"`
- `exam_block`: `"A00"` (Toán, Lý, Hóa) · `"A01"` (Toán, Lý, Anh) · `"B00"` (Toán, Hóa, Sinh) · `"C00"` (Văn, Sử, Địa) · `"D01"` (Toán, Văn, Anh) · `"D07"` (Toán, Hóa, Anh)
- `target_score`: Tổng điểm 3 môn, thang 0–30

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

- `subject` enum: `toan` · `van` · `anh` · `ly` · `hoa` · `sinh` · `su` · `dia` · `gdcd` · `tin` · `cong_nghe`
- Tất cả `score` và `average_score`: thang **0–10**

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

- Day keys: `thu_2` · `thu_3` · `thu_4` · `thu_5` · `thu_6` · `thu_7` · `chu_nhat`
- `quality`: `"tốt"` hoặc `"trung bình"`
- `school_sessions`: `"S"` = sáng, `"C"` = chiều

### 6.3 Output: `AnalysisResult`

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

Các trường trong `weekly_study_schedule.entries`:

| Trường | Mô tả | Ví dụ |
|--------|-------|-------|
| `day` | Tên thứ (tiếng Việt) | `"Thứ 2"` |
| `start`, `end` | Giờ bắt đầu / kết thúc | `"19:30"`, `"22:00"` |
| `subject` | Tên môn cần học | `"Lý"` |
| `topics` | Chủ đề cụ thể | `["Cơ học", "Điện học"]` |
| `activity` | Loại hoạt động | `"Học lý thuyết + Làm bài tập"` |
| `slot_quality` | Chất lượng tập trung | `"tốt"` / `"trung bình"` |

---

## 7. LOGIC XỬ LÝ CỐT LÕI

### 7.1 Xác định môn yếu (`_identify_weak_subjects`)

- **Nguồn dữ liệu**: `academic_data.subject_scores` + `report_card.subjects`
- **Ngưỡng**: `8.0/10` (cấu hình trong `config.py`)
- **Đầu ra**: Danh sách môn yếu, sắp xếp theo gap lớn nhất

### 7.2 Tạo lịch học bổ sung (`_build_weekly_schedule`)

- Lấy các khung giờ rảnh từ `study_habits.weekly_available_slots`
- Phân phối môn yếu theo **trọng số gap** (gap lớn hơn → được xếp nhiều slot hơn)
- Ưu tiên slot chất lượng `"tốt"` cho học lý thuyết + làm bài tập
- Slot chất lượng `"trung bình"` dùng cho ôn tập + bài tập nhẹ
- Bỏ qua các slot có thời lượng < 30 phút

### 7.3 AI Summary (tính năng tương lai)

Trường `ai_summary` hiện tại luôn trả về `null`.  
Code cho tính năng này đã được viết sẵn nhưng bị comment out trong `timetable_analyzer.py`.  
Khi enable, cần thiết lập `ANTHROPIC_API_KEY` trong file `.env`.

---

## 8. CẤU HÌNH & THANG ĐIỂM

| Tham số | Giá trị | Mô tả |
|---------|---------|-------|
| `WEAK_TOPIC_THRESHOLD` | `8.0` | Dưới 8.0/10 được xem là môn yếu |
| `MINIMUM_SUBJECT_SCORE` | `8.0` | Điểm tối thiểu cho môn không thuộc khối thi |
| Thang điểm | `0–10` | Thang điểm chuẩn Việt Nam |
| `target_score` (career goal) | `0–30` | Tổng điểm 3 môn thi |

Để thay đổi cấu hình, chỉnh sửa file `agentic_ai/config.py`.

---

## 9. HƯỚNG DẪN TÍCH HỢP

### 9.1 Gọi từ Python code

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

# Option B: Truyền dict / JSON (cho API integration)
result = generate_learning_path_from_dict(data)
```

### 9.2 Cho team Backend

**Tích hợp FastAPI:**

```python
from fastapi import FastAPI
from agentic_ai.main import generate_learning_path_from_dict

app = FastAPI()

@app.post("/api/analyze")
async def analyze(data: dict):
    result = generate_learning_path_from_dict(data)
    return result
```

Lưu ý khi tích hợp:
1. Wrap `generate_learning_path_from_dict()` trong FastAPI endpoint.
2. Input: JSON body chứa 6 fields như mô tả ở mục 6.
3. Output: JSON `AnalysisResult`.
4. **Không cần API key** – core engine hoàn toàn deterministic.
5. **Thời gian xử lý**: thường < 1ms (không có network call).
6. Validation lỗi: Pydantic sẽ raise `ValidationError` với message chi tiết nếu data sai format.

**Mở rộng hệ thống:**
- Thêm môn học mới: chỉnh sửa `Subject` enum trong `schemas/student.py`
- Thay đổi ngưỡng điểm: chỉnh sửa `config.py`
- Enable AI summary: uncomment code trong `timetable_analyzer.py`, thiết lập `ANTHROPIC_API_KEY`

### 9.3 Cho team Frontend

**Dữ liệu cần thu thập từ UI:**

1. **Thông tin học sinh** – tên, lớp, khối thi, mục tiêu nghề nghiệp
2. **Điểm học tập** – điểm từng môn, từng chủ đề (thang 10)
3. **Bảng điểm học kỳ** – điểm trung bình các môn từ trường
4. **Đánh giá tâm lý** – MSLQ (1–7), Big Five (0–1), VARK (0–100)
5. **Thời khóa biểu** – giờ học trên lớp từng ngày
6. **Thói quen học tập** – khung giờ rảnh, thời gian tập trung tốt nhất

**Hiển thị kết quả:**
- Output chính: `weekly_study_schedule.entries` – mảng các buổi học bổ sung theo tuần.
- Output phụ: `weak_subjects_analysis` – danh sách môn yếu kèm điểm số và gap.

### 9.4 Mock Data để test

3 hồ sơ học sinh mẫu có sẵn:

```python
from agentic_ai.test_data.mock_student import (
    create_mock_student_data,           # Mặc định: Trịnh Vỹ Kiệt (12A2, A01)
    create_mock_student_high_achiever,  # Trần Thị B (12, A00, điểm cao)
    create_mock_student_struggling,     # Lê Văn C (10, D01, điểm thấp)
)
```

---

## 10. TÀI LIỆU LIÊN QUAN

| Tài liệu | Đường dẫn | Mô tả |
|----------|-----------|-------|
| Đặc tả Agentic AI | [`doc/agentic-ai.md`](doc/agentic-ai.md) | Kiến trúc hệ thống 3-agent đầy đủ (định hướng tương lai) |
| Hướng dẫn chi tiết | [`doc/tutorial.md`](doc/tutorial.md) | Hướng dẫn cài đặt, tích hợp, data flow toàn hệ thống |
| Yêu cầu mới | [`doc/new-requirement.md`](doc/new-requirement.md) | Yêu cầu tính năng lịch học bổ sung hàng tuần |
| Bộ câu hỏi hành vi học tập | [`doc/hanh-vi-hoc-tap.md`](doc/hanh-vi-hoc-tap.md) | MSLQ rút gọn – 30 câu đánh giá động cơ & chiến lược học |
| Bộ câu hỏi tâm sinh lý | [`doc/tam-sinh-li.md`](doc/tam-sinh-li.md) | 10 câu đánh giá nguy cơ rối loạn tâm lý – tâm thần |
