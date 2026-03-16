# ĐẶC TẢ KỸ THUẬT AGENTIC AI CHO HỆ THỐNG LỘ TRÌNH HỌC TẬP CÁ NHÂN HÓA (Edu-Tech)

## 1. MỤC TIÊU HỆ THỐNG

### 1.1 Mục tiêu chức năng
Hệ thống AI cần thực hiện được chuỗi xử lý:

1. **Phân tích bảng điểm** (dữ liệu từ backend):
   - Nhận dữ liệu điểm số, lịch sử bài kiểm tra, môn học, khối thi.
   - Phát hiện điểm mạnh – điểm yếu theo từng môn và từng chủ đề (topic).

2. **Đối chiếu tâm lý – hành vi học tập:**
   - Nhận kết quả bộ câu hỏi tâm sinh lý (MSLQ, Big Five, EQ, VARK).
   - Suy luận phong cách học, động cơ, mức độ tự chủ, lo âu thi cử, mức độ cần hỗ trợ.

3. **Truy xuất lộ trình học tập:**
   - Tạo 3 lộ trình song song:
     - (1) Lộ trình khắc phục điểm yếu theo môn - Đối tượng: cá nhân.
     - (2) Lộ trình tổng thể THPT (tập trung 4 môn tự chọn theo khối thi, bắt buộc văn và toán) - Đối tượng: học sinh lớp 9 đến lớp 12.
     - (3) Lộ trình cá nhân theo ngành học (đặc biệt từ đại học trở lên – ví dụ: AI) - Đối tượng: sinh viên đại học trở lên.

4. **Tổng hợp kết quả:**
   - Hợp nhất 3 lộ trình thành một cấu trúc thống nhất.
   - Xử lý trùng lặp, xung đột, ưu tiên.
   - Chuẩn bị output ở dạng JSON có cấu trúc rõ ràng cho frontend / backend sử dụng.

### 1.2 Mục tiêu phi chức năng
- Thời gian phản hồi: **< 15s** cho 1 lần sinh lộ trình đầy đủ.
- Khả năng mở rộng: dễ bổ sung thêm agent mới (ví dụ: Soft-skill Agent).
- Khả năng giám sát, debug: có log theo agent, theo request, theo học sinh.
- Bảo mật: không lộ thông tin cá nhân trực tiếp cho LLM (ẩn danh hóa / rút gọn).

---

## 2. KIẾN TRÚC AGENTIC AI TỔNG THỂ

### 2.1 Mô hình tổng quan

- 01 **Orchestrator Agent** (điều phối).
- 03 **Functional Agents** chạy song song:
  1. **Remedial Path Agent** – Lộ trình khắc phục môn yếu.
  2. **Strategic THPT Path Agent** – Lộ trình tổng thể lớp 9–12 dựa trên tổ hợp 6 môn.
  3. **Career Path Agent** – Lộ trình theo ngành học (đặc biệt cho bậc đại học).

### 2.2 Luồng xử lý tổng quát

1. Frontend/Backend gửi `student_id` (và các tham số cần thiết) → Orchestrator.
2. Orchestrator:
   - Gọi backend để lấy:
     - Bảng điểm, lịch sử bài kiểm tra.
     - Thông tin học sinh (khối thi, mục tiêu nghề nghiệp…).
     - Kết quả bộ câu hỏi tâm sinh lý.
   - Chuẩn hóa dữ liệu đầu vào → context chung cho 3 agents.
3. Orchestrator khởi chạy **3 agents song song** (3 function call độc lập).
4. Mỗi agent:
   - Thực hiện logic chuyên biệt (remedial / strategic / career).
   - Truy xuất thêm từ knowledge base (lộ trình mẫu, tài nguyên học tập).
   - Sinh ra 1 lộ trình riêng (định dạng JSON).
5. Orchestrator:
   - Nhận 3 kết quả.
   - Thực hiện hợp nhất + xử lý xung đột.
   - Đính kèm insight tâm lý học tập từ bộ câu hỏi.
   - Gửi kết quả cuối cùng cho backend để lưu và cho phép review (GV/phụ huynh).

---

## 3. MÔ TẢ CHI TIẾT 3 AGENTS

### 3.1 Remedial Path Agent (Lộ trình khắc phục môn yếu)

**Mục tiêu:**
- Xác định các môn / chủ đề mà học sinh còn yếu (score thấp hoặc dao động).
- Đề xuất lộ trình ngắn hạn (ví dụ: 4–8 tuần) để "vá lỗ hổng" kiến thức.

**Yêu cầu dữ liệu đầu vào:**
- Điểm số theo từng bài kiểm tra, từng môn.
- Thông tin chi tiết bài kiểm tra: chủ đề (topic), dạng bài, độ khó.
- Chuẩn đầu ra môn học theo lớp (curriculum standard).
- Kết quả tâm sinh lý liên quan đến:
  - **Tự điều chỉnh nhận thức, nỗ lực**, **test anxiety**, **tính cẩn thận (conscientiousness)**.

**Yêu cầu xử lý:**
1. Nhóm dữ liệu điểm theo môn → theo chủ đề → tính:
   - Điểm trung bình.
   - Độ lệch so với chuẩn (ví dụ: chuẩn 80%, học sinh 55%).
2. Xác định danh sách `weak_topics`:
   - Chủ đề < ngưỡng (ví dụ: 80%).
   - Ưu tiên:
     - Chủ đề cốt lõi, nền tảng.
     - Chủ đề có tần suất xuất hiện cao trong bài thi.
3. Dựa trên hồ sơ tâm lý:
   - Học sinh có test anxiety cao → chia nhỏ mục tiêu, tăng kiểm tra ngắn, phản hồi tích cực.
   - Học sinh có conscientiousness cao → có thể giao workload cao hơn, kế hoạch chi tiết hơn.
   - Learning style (VARK) → gợi ý dạng tài liệu phù hợp (video, sơ đồ, bài tập thực hành).

**Yêu cầu output (Remedial Path):**
- Thời lượng: 4–8 tuần.
- Cho mỗi môn yếu:
  - `current_score`, `target_score`.
  - Các `weak_topics`.
  - Kế hoạch theo tuần:
    - Mục tiêu (learning goal).
    - Tài nguyên (resource list): video, bài tập, đề luyện.
    - Checkpoint (bài test nhỏ / bài quiz).
- Ước tính mức cải thiện nếu hoàn thành (ví dụ: +20–30 điểm sau 4 tuần).

---

### 3.2 Strategic THPT Path Agent (Lộ trình tổng thể THPT – 4 môn)

**Mục tiêu:**
- Tập trung xây lộ trình dài hạn cho khối thi (tổ hợp 4 môn).
- Đảm bảo:
  - 4 môn khối thi hướng tới **100% mục tiêu**.
  - Môn còn lại tối thiểu **80%** (để không “hổng” quá nhiều).

**Yêu cầu dữ liệu đầu vào:**
- Thông tin học sinh:
  - Lớp hiện tại (9–12).
  - Khối thi hoặc tổ hợp môn (A00, D01, v.v.).
  - Ngành/nhóm ngành dự định (để đối chiếu điểm chuẩn).
- Điểm trung bình hiện tại từng môn.
- Điểm chuẩn/benchmark của các trường/khối ngành liên quan (nếu có).
- Thông tin từ khảo sát:
  - Động cơ nội tại vs ngoại tại (MSLQ).
  - Năng lực tự học, quản lý thời gian, môi trường học.

**Yêu cầu xử lý:**
1. Xác định danh sách 4 môn thuộc tổ hợp thi và các môn còn lại.
2. Phân loại:
   - Môn ưu tiên (ưu tiên cao nếu điểm thấp nhưng trọng số lớn).
   - Môn không thuộc khối thi nhưng thấp hơn 80% → cần nâng nhẹ.
3. Thiết kế lộ trình 12–24 tháng:
   - Chia theo giai đoạn (quý / học kỳ).
   - Ứng với mỗi giai đoạn:
     - Mục tiêu điểm số từng môn.
     - Phân bổ thời gian học (tỉ lệ thời lượng/môn).
4. Tích hợp insights tâm lý:
   - Học sinh có self-efficacy thấp → tăng hỗ trợ, đặt mục tiêu vừa sức, nhiều feedback.
   - Học sinh có test anxiety cao → xen kẽ các mock test theo dạng “thi thử an toàn”.
   - Học sinh có time management kém → thêm block “train kỹ năng quản lý thời gian”.

**Yêu cầu output (Strategic Path):**
- Mức ưu tiên môn: `critical`, `high`, `medium`.
- Kế hoạch 12–24 tháng:
  - Mỗi giai đoạn (3 tháng / 1 kỳ):
    - Mục tiêu điểm số từng môn.
    - Gợi ý số giờ học/tuần cho từng môn.
    - Milestones (ví dụ: hoàn thành x% chương trình, làm x đề thi).
- Phân tích gap:
  - Điểm hiện tại vs điểm mục tiêu vào trường/khối ngành.

---

### 3.3 Career Path Agent (Lộ trình theo ngành – Đại học trở đi)

**Mục tiêu:**
- Xây lộ trình học tập theo ngành nghề (ví dụ: AI, Y khoa, Kinh tế…).
- Nhấn mạnh:
  - Nền tảng kiến thức cần có trước đại học.
  - Kỹ năng & kiến thức cần tích lũy trong 1–2 năm đầu đại học.

**Yêu cầu dữ liệu đầu vào:**
- Ngành học mục tiêu (ví dụ: “AI”, “Data Science”, “Y khoa”).
- Khả năng hiện tại:
  - Toán, logic, tư duy phân tích.
  - Ngoại ngữ (đặc biệt là tiếng Anh).
  - Kỹ năng liên quan (lập trình, thuyết trình, nghiên cứu…).
- Hồ sơ tâm lý:
  - Openness, Conscientiousness, Extraversion…
  - Động cơ nội tại với lĩnh vực (mức độ hứng thú, tò mò).

**Yêu cầu xử lý:**
1. Lấy “roadmap chuẩn” theo ngành (internal knowledge base):
   - Các mô-đun chính (prerequisite → core → advanced).
   - Thời gian khuyến nghị (theo năm).
2. Đối chiếu với tình trạng hiện tại:
   - Kỹ năng nào đã đạt?
   - Kỹ năng nào còn thiếu / yếu?
3. Thiết kế lộ trình nhiều pha:
   - Pha THPT: xây nền tảng kiến thức, kỹ năng (ví dụ: toán, tiếng Anh, tư duy logic).
   - Pha “pre-university”: khóa học online, dự án nhỏ, trải nghiệm thực tế.
   - Pha năm 1–2 đại học: môn trọng tâm, project nên làm, chứng chỉ nên thi.

**Yêu cầu output (Career Path):**
- Danh sách prerequisite + trạng thái (đạt/chưa đạt).
- Roadmap theo pha (THPT → tiền đại học → đại học năm 1–2).
- Gợi ý:
  - Khóa học cụ thể (tùy theo mức độ chi tiết của knowledge base).
  - Loại project nên làm (mini project, nghiên cứu nhỏ…).
  - Mốc đánh giá: kỹ năng / kiến thức cần check ở mỗi pha.

---

## 4. ORCHESTRATOR AGENT & CHẠY SONG SONG 3 FUNCTION CALL

### 4.1 Nhiệm vụ Orchestrator

- Chuẩn hóa input: từ `student_id` → gom toàn bộ dữ liệu cần thiết:
  - Bảng điểm, kết quả test.
  - Hồ sơ tâm lý (từ bộ câu hỏi).
  - Mục tiêu khối thi, ngành học.
- Gọi **đồng thời** 3 function/agent:
  1. `generate_remedial_path(student_profile, academic_data, psychology_data)`
  2. `generate_strategic_path(student_profile, academic_data, psychology_data)`
  3. `generate_career_path(student_profile, academic_data, psychology_data)`
- Giám sát:
  - Thời gian thực thi mỗi agent (timeout).
  - Xử lý trường hợp 1 agent fail (fallback: trả 2 lộ trình còn lại + cờ “partial result”).
- Hợp nhất kết quả:
  - Các lộ trình đều được đưa về 1 JSON chung.
  - Xử lý trùng lặp đề xuất (ví dụ: cùng đề xuất tăng học Toán):
    - Gộp, tránh trùng nội dung.
    - Đánh priority theo logic (remedial > strategic > career).
- Tích hợp Human-in-the-Loop:
  - Lưu kết quả trạng thái `pending_approval`.
  - Cho phép giáo viên/phụ huynh chỉnh sửa nhẹ hoặc approve trước khi hiển thị cho học sinh.

### 4.2 Yêu cầu về Function Call

- 3 function cần:
  - Input có schema rõ ràng (student_profile, academic_data, psychology_data).
  - Output tuân thủ 1 JSON schema thống nhất (xem mục 5).
- Nên định nghĩa **schema chung** để:
  - Validate output.
  - Giảm lỗi do LLM sinh sai cấu trúc.

---

## 5. ĐỊNH NGHĨA OUTPUT JSON CHUẨN

### 5.1 Cấu trúc JSON tổng

```jsonc
{
  "student_id": "string",
  "generated_at": "ISO8601 datetime",
  "paths": {
    "remedial": { /* chi tiết lộ trình khắc phục */ },
    "strategic": { /* chi tiết lộ trình THPT */ },
    "career": { /* chi tiết lộ trình ngành học */ }
  },
  "psychology_insights": {
    "learning_style": "string",
    "motivation": {
      "intrinsic": "float (1-7)",
      "extrinsic": "float (1-7)",
      "note": "string"
    },
    "self_efficacy": "float (1-7)",
    "test_anxiety": "float (1-7)",
    "big_five": {
      "openness": "float",
      "conscientiousness": "float",
      "extraversion": "float",
      "agreeableness": "float",
      "neuroticism": "float"
    }
  },
  "status": {
    "human_review": "pending_approval | approved | rejected",
    "reviewer": "string | null",
    "notes": "string | null"
  }
}

---

## 6.  TẠO DỮ LIỆU MÔ PHỎNG CỦA 1 USER ĐỂ TEST HỆ THỐNG 

- Tạo dữ liệu mô phỏng cho một học sinh, yêu cầu đúng format JSON và schema chung.
