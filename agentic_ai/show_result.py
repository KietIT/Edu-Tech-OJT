"""
Result Viewer for Agentic AI System
Displays output_test_results.json in a clear, visual format.
"""
import json
from pathlib import Path


# ANSI color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def colored(text: str, color: str) -> str:
    """Apply color to text"""
    return f"{color}{text}{Colors.END}"


def print_header(title: str, char: str = "=", width: int = 80):
    """Print a header with decoration"""
    print("\n" + colored(char * width, Colors.CYAN))
    print(colored(f" {title} ".center(width, char), Colors.BOLD + Colors.CYAN))
    print(colored(char * width, Colors.CYAN))


def print_subheader(title: str, char: str = "-", width: int = 60):
    """Print a subheader"""
    print("\n" + colored(f" {title} ".center(width, char), Colors.YELLOW))


def print_field(label: str, value, indent: int = 2):
    """Print a labeled field"""
    spaces = " " * indent
    if value is None:
        value = "N/A"
    print(f"{spaces}{colored(label + ':', Colors.BOLD)} {value}")


def print_list(items: list, indent: int = 4):
    """Print a list of items"""
    spaces = " " * indent
    for item in items:
        print(f"{spaces}{colored('•', Colors.GREEN)} {item}")


def format_score(score: float, threshold: float = 8.0) -> str:
    """Định dạng điểm với màu dựa trên ngưỡng (thang điểm 10)"""
    if score >= threshold:
        return colored(f"{score:.2f}/10", Colors.GREEN)
    elif score >= threshold - 2:
        return colored(f"{score:.2f}/10", Colors.YELLOW)
    else:
        return colored(f"{score:.2f}/10", Colors.RED)


def display_overview(data: dict):
    """Display overview section"""
    print_header("TỔNG QUAN KẾT QUẢ - OVERVIEW", "=")

    print_field("Mã học sinh", data.get("student_id"))
    print_field("Thời gian tạo", data.get("generated_at"))
    print_field("Thời gian xử lý", f"{data.get('processing_time_seconds', 0):.2f} giây")
    print_field("Kết quả không đầy đủ", colored("Có", Colors.RED) if data.get("is_partial_result") else colored("Không", Colors.GREEN))
    print_field("Phiên bản", data.get("version", "1.0"))

    # Status
    status = data.get("status", {})
    status_text = status.get("status", "unknown")
    if status_text == "pending_approval":
        print_field("Trạng thái", colored("CHỜ PHÊ DUYỆT", Colors.YELLOW))
    elif status_text == "approved":
        print_field("Trạng thái", colored("ĐÃ PHÊ DUYỆT", Colors.GREEN))
    else:
        print_field("Trạng thái", status_text)


def display_agent_results(data: dict):
    """Display agent execution results"""
    print_subheader("KẾT QUẢ THỰC THI AGENT - Agent Results")

    agent_results = data.get("agent_results", [])
    for agent in agent_results:
        name = agent.get("agent_name", "Unknown")
        success = agent.get("success", False)
        time = agent.get("execution_time_seconds", 0)
        error = agent.get("error")

        status = colored("THÀNH CÔNG", Colors.GREEN) if success else colored("THẤT BẠI", Colors.RED)
        print(f"    {colored(name, Colors.BOLD)}: {status} ({time:.2f}s)")
        if error:
            print(f"      Lỗi: {colored(error, Colors.RED)}")


def display_psychology_insights(data: dict):
    """Display psychology insights"""
    print_header("PHÂN TÍCH TÂM LÝ - Psychology Insights", "=")

    insights = data.get("psychology_insights", {})

    # Learning style
    style = insights.get("learning_style", "N/A")
    style_map = {
        "visual": "Thị giác (Visual)",
        "auditory": "Thính giác (Auditory)",
        "reading_writing": "Đọc/Viết (Reading/Writing)",
        "kinesthetic": "Vận động (Kinesthetic)",
        "multimodal": "Đa phương thức (Multimodal)"
    }
    print_field("Phong cách học", style_map.get(style, style))

    # Motivation
    motivation = insights.get("motivation", {})
    print_field("Động lực nội tại", f"{motivation.get('intrinsic', 0):.1f}/7")
    print_field("Động lực ngoại tại", f"{motivation.get('extrinsic', 0):.1f}/7")
    if motivation.get("note"):
        print_field("Ghi chú", motivation.get("note"))

    # Self-efficacy & Test anxiety
    se = insights.get("self_efficacy", 0)
    ta = insights.get("test_anxiety", 0)

    se_color = Colors.GREEN if se >= 5 else (Colors.YELLOW if se >= 3 else Colors.RED)
    ta_color = Colors.GREEN if ta <= 3 else (Colors.YELLOW if ta <= 5 else Colors.RED)

    print_field("Sự tự tin", colored(f"{se:.1f}/7", se_color))
    print_field("Lo âu thi cử", colored(f"{ta:.1f}/7", ta_color))

    # Workload
    workload = insights.get("workload_recommendation", "medium")
    workload_map = {"light": "Nhẹ", "medium": "Trung bình", "heavy": "Nặng"}
    print_field("Khối lượng học đề xuất", workload_map.get(workload, workload))

    # Big Five
    big_five = insights.get("big_five", {})
    if big_five:
        print_subheader("Tính cách Big Five")
        trait_map = {
            "openness": "Cởi mở",
            "conscientiousness": "Tận tâm",
            "extraversion": "Hướng ngoại",
            "agreeableness": "Hòa đồng",
            "neuroticism": "Nhạy cảm"
        }
        for trait, value in big_five.items():
            bar_len = int(value * 20)
            bar = colored("█" * bar_len, Colors.BLUE) + "░" * (20 - bar_len)
            label = trait_map.get(trait, trait.capitalize())
            print(f"    {label:20} {bar} {value:.2f}")

    # Support recommendations
    recommendations = insights.get("support_recommendations", [])
    if recommendations:
        print_subheader("Khuyến nghị hỗ trợ - Support Recommendations")
        print_list(recommendations)


def display_remedial_path(data: dict):
    """Display remedial path details"""
    print_header("LỘ TRÌNH KHẮC PHỤC - Remedial Path (4-8 tuần)", "=")

    paths = data.get("paths", {})
    remedial = paths.get("remedial", {})

    if not remedial or remedial.get("duration_weeks", 0) == 0:
        print(colored("    Không cần khắc phục - Học sinh đã đạt tiêu chuẩn!", Colors.GREEN))
        return

    print_field("Mã lộ trình", remedial.get("path_id"))
    print_field("Thời gian", f"{remedial.get('duration_weeks', 0)} tuần")
    print_field("Ngày bắt đầu", remedial.get("start_date"))
    print_field("Ngày kết thúc", remedial.get("end_date"))

    # Overall goals
    goals = remedial.get("overall_goals", [])
    if goals:
        print_subheader("Mục tiêu tổng thể - Overall Goals")
        print_list(goals)

    # Subject plans
    subject_plans = remedial.get("subject_plans", [])
    if subject_plans:
        print_subheader("Kế hoạch theo môn - Subject Plans")
        for sp in subject_plans:
            subject = sp.get("subject", "Unknown")
            current = sp.get("current_score", 0)
            target = sp.get("target_score", 0)
            improvement = sp.get("estimated_improvement", "")

            print(f"\n    {colored('MÔN: ' + subject.upper(), Colors.BOLD + Colors.BLUE)}")
            print(f"      Điểm hiện tại: {format_score(current)} → Mục tiêu: {format_score(target, 9.0)}")
            print(f"      Khoảng cách: {colored(f'{target - current:.1f} điểm', Colors.YELLOW)}")
            print(f"      Dự kiến cải thiện: {colored(improvement, Colors.GREEN)}")

            weak_topics = sp.get("weak_topics", [])
            if weak_topics:
                print(f"      Chủ đề yếu: {', '.join(weak_topics[:5])}")

            # Weekly plans - show ALL weeks
            weekly_plans = sp.get("weekly_plans", [])
            if weekly_plans:
                print(f"\n      {colored('Kế hoạch hàng tuần:', Colors.BOLD)} ({len(weekly_plans)} tuần)")
                print(f"      {'-' * 50}")
                for wp in weekly_plans:  # Show ALL weeks
                    week_num = wp.get("week_number", 0)
                    goals = wp.get("learning_goals", [])
                    hours = wp.get("estimated_hours", 0)
                    topics = wp.get("topics_to_cover", [])

                    print(f"\n        {colored(f'Tuần {week_num}:', Colors.CYAN)} ({hours}h)")
                    if topics:
                        print(f"          Chủ đề: {', '.join(topics[:3])}")
                    if goals:
                        print(f"          Mục tiêu:")
                        for goal in goals[:3]:
                            print(f"            • {goal}")

                    # Show checkpoints if any
                    checkpoints = wp.get("checkpoints", [])
                    if checkpoints:
                        for cp in checkpoints:
                            cp_name = cp.get("name", "Kiểm tra")
                            print(f"          {colored('📝 Checkpoint:', Colors.YELLOW)} {cp_name}")

    # Psychology considerations (AI content)
    psych = remedial.get("psychology_considerations", {})
    if psych:
        print_subheader("Phân tích từ AI - AI-Generated Insights")

        if psych.get("ai_strategy"):
            print(f"\n    {colored('Chiến lược học tập từ AI:', Colors.BOLD)}")
            strategy = psych.get("ai_strategy", "")
            # Word wrap for long text
            words = strategy.split()
            line = "      "
            for word in words:
                if len(line) + len(word) > 75:
                    print(line)
                    line = "      " + word + " "
                else:
                    line += word + " "
            print(line)

        if psych.get("ai_study_tips"):
            print(f"\n    {colored('Mẹo học tập từ AI:', Colors.BOLD)}")
            tips = psych.get("ai_study_tips", "").split("; ")
            print_list(tips, indent=6)

        # Show other psychology considerations
        for key, value in psych.items():
            if key not in ["ai_strategy", "ai_study_tips"] and value:
                key_map = {
                    "workload": "Khối lượng học",
                    "feedback": "Phản hồi",
                    "resources": "Tài nguyên",
                    "support": "Hỗ trợ"
                }
                label = key_map.get(key, key.capitalize()) or key.capitalize()
                print(f"\n    {colored(label + ':', Colors.BOLD)} {value}")

    # Success metrics   
    metrics = remedial.get("success_metrics", [])
    if metrics:
        print_subheader("Tiêu chí thành công - Success Metrics")
        print_list(metrics)


def display_strategic_path(data: dict):
    """Display strategic THPT path details"""
    print_header("LỘ TRÌNH CHIẾN LƯỢC THPT - Strategic Path (12-24 tháng)", "=")

    paths = data.get("paths", {})
    strategic = paths.get("strategic", {})

    if not strategic or strategic.get("duration_months", 0) == 0:
        print(colored("    Không áp dụng", Colors.YELLOW))
        return

    print_field("Mã lộ trình", strategic.get("path_id"))
    print_field("Thời gian", f"{strategic.get('duration_months', 0)} tháng")
    print_field("Khối thi", strategic.get("exam_block"))

    # Gap Analysis
    gap = strategic.get("gap_analysis", {})
    if gap:
        print_subheader("Phân tích khoảng cách - Gap Analysis")
        current = gap.get("current_total_score", 0)
        target = gap.get("target_total_score", 0)
        gap_val = gap.get("gap", 0)
        comp = gap.get("competitiveness", "")

        comp_map = {"achievable": "Khả thi", "challenging": "Thách thức", "stretch": "Rất khó"}
        comp_color = Colors.GREEN if comp == "achievable" else (Colors.YELLOW if comp == "challenging" else Colors.RED)

        avg_current = current / 3
        avg_target = target / 3

        print_field("Điểm hiện tại", f"{current:.1f}/30 (TB: {avg_current:.1f}/10 mỗi môn)", indent=4)
        print_field("Điểm mục tiêu", f"{target:.1f}/30 (TB: {avg_target:.1f}/10 mỗi môn)", indent=4)
        print_field("Khoảng cách", colored(f"{gap_val:.1f} điểm", Colors.YELLOW if gap_val > 0 else Colors.GREEN), indent=4)
        print_field("Mức độ cạnh tranh", colored(comp_map.get(comp, comp).upper(), comp_color), indent=4)
        if gap.get("target_university"):
            print_field("Trường mục tiêu", gap.get("target_university"), indent=4)

    # Subject priorities
    priorities = strategic.get("subject_priorities", [])
    if priorities:
        print_subheader("Ưu tiên môn học - Subject Priorities")
        print(f"\n    {'Môn':<10} {'Ưu tiên':<12} {'Hiện tại':<10} {'Mục tiêu':<10} {'Chênh lệch':<10} {'Giờ/Tuần'}")
        print("    " + "-" * 65)
        for sp in priorities:
            subj = sp.get("subject", "")[:10]
            pri = sp.get("priority", "")
            cur = sp.get("current_score", 0)
            tar = sp.get("target_score", 0)
            g = sp.get("gap", 0)
            hrs = sp.get("weekly_hours_recommended", 0)

            pri_color = Colors.RED if pri == "critical" else (Colors.YELLOW if pri == "high" else Colors.GREEN)
            exam_mark = "*" if sp.get("is_exam_subject") else " "

            print(f"    {subj:<10} {colored(f'{pri:<12}', pri_color)} {cur:<10.1f} {tar:<10.1f} {g:<10.1f} {hrs:.1f}h {exam_mark}")
        print("    (* = Môn thi khối | Điểm trên thang 10)")

    # Phases summary
    phases = strategic.get("phases", [])
    if phases:
        print_subheader("Các giai đoạn - Phases")
        for phase in phases[:4]:  # Show first 4 phases
            num = phase.get("phase_number", 0)
            name = phase.get("phase_name", "")
            focus = phase.get("focus_areas", [])
            print(f"\n    {colored(f'Giai đoạn {num}:', Colors.BOLD)} {name}")
            if focus:
                print(f"      Trọng tâm: {', '.join(focus[:2])}")

    # AI Strategic Summary
    psych = strategic.get("psychology_considerations", {})
    if psych.get("ai_strategic_summary"):
        print_subheader("Tóm tắt chiến lược từ AI")
        summary = psych.get("ai_strategic_summary", "")
        words = summary.split()
        line = "    "
        for word in words:
            if len(line) + len(word) > 75:
                print(line)
                line = "    " + word + " "
            else:
                line += word + " "
        print(line)

    # Critical success factors
    factors = strategic.get("critical_success_factors", [])
    if factors:
        print_subheader("Yếu tố thành công - Critical Success Factors")
        print_list(factors)


def display_career_path(data: dict):
    """Display career path details"""
    print_header("LỘ TRÌNH NGHỀ NGHIỆP - Career Path", "=")

    paths = data.get("paths", {})
    career = paths.get("career", {})

    if not career or career.get("target_field") == "general":
        print(colored("    Chưa xác định mục tiêu nghề nghiệp", Colors.YELLOW))
        return

    print_field("Mã lộ trình", career.get("path_id"))
    print_field("Nghề nghiệp mục tiêu", colored(career.get("target_career", ""), Colors.BOLD + Colors.BLUE))
    print_field("Lĩnh vực", career.get("target_field"))

    # Universities
    unis = career.get("recommended_universities", [])
    if unis:
        print_field("Trường đại học đề xuất", ", ".join(unis))

    # Prerequisites
    prereqs = career.get("prerequisites", [])
    if prereqs:
        print_subheader("Điều kiện tiên quyết - Prerequisites")
        achieved = sum(1 for p in prereqs if p.get("status") == "achieved")
        in_progress = sum(1 for p in prereqs if p.get("status") == "in_progress")
        not_started = sum(1 for p in prereqs if p.get("status") == "not_started")

        print(f"    Tiến độ: {colored(str(achieved), Colors.GREEN)} đã đạt / {colored(str(in_progress), Colors.YELLOW)} đang học / {colored(str(not_started), Colors.RED)} chưa bắt đầu")
        print()

        for p in prereqs:
            name = p.get("name", "")
            status = p.get("status", "")
            target = p.get("target_level", "")

            if status == "achieved":
                icon = colored("✓", Colors.GREEN)
                status_vn = "Đã đạt"
            elif status == "in_progress":
                icon = colored("◐", Colors.YELLOW)
                status_vn = "Đang học"
            else:
                icon = colored("○", Colors.RED)
                status_vn = "Chưa bắt đầu"

            print(f"    {icon} {name:<25} Mục tiêu: {target}")

    # Career phases
    phases = career.get("phase_plans", [])
    if phases:
        print_subheader("Các giai đoạn nghề nghiệp - Career Phases")
        for phase in phases:
            phase_name = phase.get("phase_name", "")
            duration = phase.get("duration_months", 0)
            objectives = phase.get("objectives", [])
            courses = phase.get("key_courses", [])

            print(f"\n    {colored(phase_name, Colors.BOLD)} ({duration} tháng)")
            if objectives:
                print(f"      Mục tiêu: {objectives[0]}")
            if courses:
                print(f"      Khóa học chính: {', '.join(courses[:3])}")

    # Psychology fit & AI advice
    psych_fit = career.get("psychology_fit", {})
    if psych_fit:
        print_subheader("Phù hợp tâm lý & Lời khuyên AI")

        for key, value in psych_fit.items():
            if key.startswith("ai_"):
                label_map = {
                    "ai_career_advice": "Lời khuyên nghề nghiệp từ AI",
                    "ai_roadmap_advice": "Lời khuyên lộ trình từ AI"
                }
                label = label_map.get(key, key.replace('ai_', '').replace('_', ' ').title()) or key.replace('ai_', '').replace('_', ' ').title()
                print(f"\n    {colored(label + ':', Colors.BOLD)}")
                words = value.split()
                line = "      "
                for word in words:
                    if len(line) + len(word) > 75:
                        print(line)
                        line = "      " + word + " "
                    else:
                        line += word + " "
                print(line)
            else:
                trait_map = {
                    "openness": "Cởi mở",
                    "conscientiousness": "Tận tâm",
                    "extraversion": "Hướng ngoại",
                    "agreeableness": "Hòa đồng",
                    "neuroticism": "Nhạy cảm",
                    "general": "Tổng quát"
                }
                label = trait_map.get(key, key.capitalize()) or key.capitalize()
                print(f"    {colored(label + ':', Colors.BOLD)} {value}")

    # Industry insights
    insights = career.get("industry_insights", [])
    if insights:
        print_subheader("Thông tin ngành - Industry Insights")
        print_list(insights)


def display_full_json(data: dict):
    """Display full JSON for reference"""
    print_header("DU LIEU JSON DAY DU - Full JSON Data", "=")
    print("\nSee output_test_results.json for complete data.")
    print(f"Total keys: {len(data)}")
    print(f"Paths included: {list(data.get('paths', {}).keys())}")


def main():
    """Main function to display results"""
    # Find the JSON file
    script_dir = Path(__file__).parent
    json_path = script_dir.parent / "output_test_results.json"

    if not json_path.exists():
        json_path = Path("output_test_results.json")

    if not json_path.exists():
        print(colored("ERROR: output_test_results.json not found!", Colors.RED))
        print("Please run 'python -m agentic_ai.run_test' first.")
        return

    # Load JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Display all sections
    print("\n" + "=" * 80)
    print(colored("  AGENTIC AI SYSTEM - KẾT QUẢ PHÂN TÍCH LỘ TRÌNH HỌC TẬP  ", Colors.BOLD + Colors.HEADER).center(90))
    print(colored("  Personalized Learning Path Analysis Results  ", Colors.HEADER).center(90))
    print("=" * 80)

    display_overview(data)
    display_agent_results(data)
    display_psychology_insights(data)
    display_remedial_path(data)
    display_strategic_path(data)
    display_career_path(data)

    # Footer
    print("\n" + "=" * 80)
    print(colored("  KẾT THÚC BÁO CÁO - END OF REPORT  ", Colors.BOLD + Colors.CYAN).center(90))
    print("=" * 80)
    print(f"\nDữ liệu đầy đủ được lưu tại: {json_path.absolute()}")
    print("Để xem chi tiết, mở file JSON trực tiếp.\n")


if __name__ == "__main__":
    main()
