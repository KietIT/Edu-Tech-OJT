"""
Timetable Analyzer - Single analyzer replacing the 3-agent architecture.

Analyzes 3 input data fields:
  1. School Timetable (thời khóa biểu)
  2. Report Card (bảng điểm)
  3. Study Habits (thói quen học tập)

Outputs a weekly supplementary study schedule to improve weak subjects,
ensuring no conflicts with the school schedule.
"""
import time
import uuid
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from .base import AgentContext
from ..schemas.paths import WeeklyStudySchedule, ScheduleEntry
from ..schemas.student import get_subject_display_name
from ..schemas.output import AnalysisResult, WeakSubjectInfo
from ..config import settings

logger = logging.getLogger(__name__)


class TimetableAnalyzer:
    """
    Single analyzer that replaces the 3-agent pipeline.

    Process:
    1. Identify weak subjects from report_card + academic_data (deterministic)
    2. Extract free time slots from study_habits (already excludes school hours)
    3. Build a weekly supplementary study schedule (deterministic)

    All core logic is deterministic.
    """

    def __init__(self):
        self.name = "TimetableAnalyzer"
        self.logs: List[str] = []

    def log(self, message: str) -> None:
        """Add a log entry"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{self.name}] {message}"
        self.logs.append(log_entry)
        logger.info(log_entry)

    def analyze(self, context: AgentContext) -> Dict[str, Any]:
        """
        Main entry point: analyze the 3 input fields and produce a weekly schedule.

        Args:
            context: AgentContext containing student_profile, academic_data,
                     psychology_data, timetable, report_card, study_habits

        Returns:
            Dict (serialized AnalysisResult) containing:
            - weekly_study_schedule: the supplementary study timetable
            - weak_subjects_analysis: list of identified weak subjects
            - ai_summary: always None in deterministic mode
            - processing metadata
        """
        self.logs = []
        start_time = time.time()
        self.log(f"Starting analysis for student: {context.student_profile.student_id}")

        # Step 1: Identify weak subjects
        weak_subjects = self._identify_weak_subjects(
            context.academic_data,
            context.report_card,
        )
        self.log(f"Found {len(weak_subjects)} weak subject(s)")

        # Step 2: Build the weekly study schedule
        weekly_schedule = None
        if weak_subjects and context.study_habits:
            weekly_schedule = self._build_weekly_schedule(
                weak_subjects, context
            )
        elif not context.study_habits:
            self.log("No study habits data provided — cannot build schedule")
        elif not weak_subjects:
            self.log("No weak subjects found — no supplementary schedule needed")

        # Step 3: AI summary placeholder (deterministic mode)
        ai_summary = None

        # Build result
        processing_time = time.time() - start_time
        self.log(f"Analysis completed in {processing_time:.2f}s")

        weak_subjects_info = [
            WeakSubjectInfo(
                subject=ws["subject"],
                average_score=ws["average_score"],
                gap=ws["gap"],
                weak_topics=[t.get("topic_name", "") for t in ws.get("weak_topics", [])],
                source=ws.get("source", "academic_data"),
                classification=ws.get("classification"),
            )
            for ws in weak_subjects
        ]

        result = AnalysisResult(
            student_id=context.student_profile.student_id,
            student_name=context.student_profile.name,
            generated_at=datetime.utcnow(),
            weekly_study_schedule=weekly_schedule,
            weak_subjects_analysis=weak_subjects_info,
            ai_summary=ai_summary,
            processing_time_seconds=processing_time,
        )

        return result.model_dump()

    # ──────────────────────────────────────────────
    # Step 1: Identify weak subjects
    # ──────────────────────────────────────────────

    def _identify_weak_subjects(
        self,
        academic_data,
        report_card: Optional[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Identify subjects below the WEAK_TOPIC_THRESHOLD.

        Sources:
        - academic_data.subject_scores (from test results)
        - report_card (current semester grades from school)

        Returns a list sorted by gap (largest gap first).
        """
        threshold = settings.WEAK_TOPIC_THRESHOLD
        weak_subjects: List[Dict[str, Any]] = []
        seen_subjects: set = set()

        # --- From academic_data (test results / topic scores) ---
        for subject_score in academic_data.subject_scores:
            if subject_score.average_score < threshold:
                subject_val = subject_score.subject.value
                display_name = get_subject_display_name(subject_val)

                weak_topics = [
                    {
                        "topic_id": ts.topic_id,
                        "topic_name": ts.topic_name,
                        "score": ts.score,
                        "is_core": ts.is_core_topic,
                        "exam_frequency": ts.exam_frequency,
                    }
                    for ts in subject_score.topic_scores
                    if ts.score < threshold
                ]

                weak_subjects.append({
                    "subject": display_name,
                    "subject_key": subject_val,
                    "average_score": subject_score.average_score,
                    "weak_topics": weak_topics,
                    "gap": threshold - subject_score.average_score,
                    "source": "academic_data",
                })
                seen_subjects.add(display_name)

        # --- Enrich / add from report_card ---
        if report_card:
            name_mapping = {
                "Toán": "Toán", "Vật Lý": "Lý", "Ngữ Văn": "Văn",
                "Tiếng Anh": "Anh", "Hóa học": "Hóa", "Sinh học": "Sinh",
                "Lịch Sử": "Sử", "Tin học": "Tin", "Công nghệ": "Công nghệ",
            }
            reverse_mapping = {v: k for k, v in name_mapping.items()}

            rc_by_name = {s["subject_name"]: s for s in report_card.get("subjects", [])}

            # Enrich existing weak subjects with report card data
            for ws in weak_subjects:
                rc_name = reverse_mapping.get(ws["subject"], ws["subject"])
                rc_data = rc_by_name.get(rc_name)
                if rc_data:
                    ws["report_card_average"] = rc_data.get("average_score")
                    ws["classification"] = rc_data.get("classification")

            # Discover additional weak subjects from report card
            for rc_subj in report_card.get("subjects", []):
                avg = rc_subj.get("average_score")
                if avg is None:
                    continue
                display_name = name_mapping.get(rc_subj["subject_name"], rc_subj["subject_name"])
                if display_name not in seen_subjects and avg < threshold:
                    weak_subjects.append({
                        "subject": display_name,
                        "subject_key": rc_subj.get("subject_code", "").lower(),
                        "average_score": avg,
                        "weak_topics": [],
                        "gap": threshold - avg,
                        "source": "report_card",
                        "report_card_average": avg,
                        "classification": rc_subj.get("classification"),
                    })
                    seen_subjects.add(display_name)

        # Sort by gap (largest gap = highest priority)
        weak_subjects.sort(key=lambda x: x["gap"], reverse=True)
        return weak_subjects

    # ──────────────────────────────────────────────
    # Step 2: Build the weekly supplementary schedule
    # ──────────────────────────────────────────────

    def _build_weekly_schedule(
        self,
        weak_subjects: List[Dict],
        context: AgentContext,
    ) -> Optional[WeeklyStudySchedule]:
        """
        Build a concrete weekly supplementary study schedule.

        Rules:
        - Uses free time slots from study_habits (already avoids school hours)
        - Distributes weak subjects weighted by gap (larger gap → more slots)
        - Prioritizes high-quality concentration times ("tốt" quality)
        - Skips slots shorter than 30 minutes
        """
        study_habits = context.study_habits
        if not study_habits:
            return None

        weekly_slots = study_habits.get("weekly_available_slots", {})
        if not weekly_slots:
            self.log("No available time slots found in study_habits")
            return None

        # Day display names
        day_labels = {
            "thu_2": "Thứ 2", "thu_3": "Thứ 3", "thu_4": "Thứ 4",
            "thu_5": "Thứ 5", "thu_6": "Thứ 6", "thu_7": "Thứ 7",
            "chu_nhat": "Chủ Nhật",
        }
        day_order = list(day_labels.keys())

        # Sort weak subjects by gap (largest first)
        sorted_weak = sorted(weak_subjects, key=lambda x: x["gap"], reverse=True)

        # Collect and sort all available slots
        all_slots = []
        for day_key, day_data in weekly_slots.items():
            for slot in day_data.get("free_slots", []):
                all_slots.append({
                    "day_key": day_key,
                    "day_label": day_labels.get(day_key, day_key),
                    "start": slot["start"],
                    "end": slot["end"],
                    "quality": slot.get("quality", "trung bình"),
                })

        # Sort: best quality first, then by day order
        all_slots.sort(key=lambda s: (
            0 if s["quality"] == "tốt" else 1,
            day_order.index(s["day_key"]) if s["day_key"] in day_order else 99,
        ))

        # Calculate slot duration in minutes
        def slot_minutes(slot):
            h1, m1 = map(int, slot["start"].split(":"))
            h2, m2 = map(int, slot["end"].split(":"))
            return (h2 * 60 + m2) - (h1 * 60 + m1)

        # Calculate weight for each subject based on gap
        total_gap = sum(ws["gap"] for ws in sorted_weak) or 1
        subject_weights = {
            ws["subject"]: ws["gap"] / total_gap for ws in sorted_weak
        }

        # Distribute slots across subjects (weighted round-robin)
        entries = []
        subject_slot_count: Dict[str, int] = {}
        total_minutes = 0

        for slot in all_slots:
            minutes = slot_minutes(slot)
            if minutes < 30:
                continue  # Skip slots too short for meaningful study

            # Pick the subject that is most "under-allocated" relative to its weight
            best_subject = None
            best_deficit = -float("inf")
            for ws in sorted_weak:
                subj = ws["subject"]
                allocated = subject_slot_count.get(subj, 0)
                target_slots = subject_weights[subj] * len(all_slots)
                deficit = target_slots - allocated
                if deficit > best_deficit:
                    best_deficit = deficit
                    best_subject = ws

            if not best_subject:
                continue

            subj_name = best_subject["subject"]
            weak_topic_names = [
                t.get("topic_name", "") for t in best_subject.get("weak_topics", [])
            ]

            # Activity based on slot quality
            if slot["quality"] == "tốt":
                activity = "Học lý thuyết + Làm bài tập"
            else:
                activity = "Ôn tập + Làm bài tập nhẹ"

            entries.append(ScheduleEntry(
                day=slot["day_label"],
                day_key=slot["day_key"],
                start=slot["start"],
                end=slot["end"],
                subject=subj_name,
                topics=weak_topic_names[:3],
                activity=activity,
                duration_minutes=minutes,
                slot_quality=slot["quality"],
            ))

            subject_slot_count[subj_name] = subject_slot_count.get(subj_name, 0) + 1
            total_minutes += minutes

        if not entries:
            return None

        # Sort entries by day order, then by time
        entries.sort(key=lambda e: (
            day_order.index(e.day_key) if e.day_key in day_order else 99,
            e.start,
        ))

        # Build notes
        notes = []
        constraints = study_habits.get("constraints", {})
        if constraints.get("dinner_time"):
            notes.append(f"Giờ ăn tối: {constraints['dinner_time']}")
        concentration = study_habits.get("concentration", {})
        if concentration.get("best_focus_time"):
            notes.append(f"Tập trung tốt nhất: {concentration['best_focus_time']}")
        notes.append("Lịch học bổ sung này đã tránh toàn bộ giờ học trên lớp")

        self.log(f"Built schedule: {len(entries)} sessions, {total_minutes / 60:.1f}h total")

        return WeeklyStudySchedule(
            schedule_id=f"schedule_{context.student_profile.student_id}_{uuid.uuid4().hex[:8]}",
            student_name=context.student_profile.name,
            entries=entries,
            total_supplementary_hours=round(total_minutes / 60, 1),
            weak_subjects_covered=[ws["subject"] for ws in sorted_weak],
            notes=notes,
        )
