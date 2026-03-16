"""
Base agent class and shared utilities.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import time
import logging
from datetime import datetime

from ..schemas.student import StudentProfile, AcademicData, get_subject_display_name
from ..schemas.psychology import PsychologyData
from ..schemas.output import AgentOutput
from ..config import settings


logger = logging.getLogger(__name__)


class AgentContext(BaseModel):
    """Context passed to all agents"""
    student_profile: StudentProfile
    academic_data: AcademicData
    psychology_data: PsychologyData
    timetable: Optional[Dict[str, Any]] = None
    report_card: Optional[Dict[str, Any]] = None
    study_habits: Optional[Dict[str, Any]] = None
    request_id: str
    timestamp: datetime = datetime.utcnow()

    class Config:
        arbitrary_types_allowed = True


class BaseAgent(ABC):
    """Base class for all agents in the system"""

    def __init__(self, name: str):
        self.name = name
        self.logs: List[str] = []
        self.start_time: Optional[float] = None

    def log(self, message: str) -> None:
        """Add a log entry"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{self.name}] {message}"
        self.logs.append(log_entry)
        logger.info(log_entry)

    def execute(self, context: AgentContext) -> AgentOutput:
        """Execute the agent with timing and error handling"""
        self.logs = []
        self.start_time = time.time()

        try:
            self.log(f"Starting agent execution for student: {context.student_profile.student_id}")

            # Run the agent-specific logic
            result = self.run(context)

            execution_time = time.time() - self.start_time
            self.log(f"Agent completed successfully in {execution_time:.2f}s")

            return AgentOutput(
                agent_name=self.name,
                success=True,
                data=result,
                execution_time_seconds=execution_time,
                logs=self.logs
            )

        except Exception as e:
            execution_time = time.time() - self.start_time if self.start_time else 0
            error_msg = str(e)
            self.log(f"Agent failed with error: {error_msg}")
            logger.exception(f"Agent {self.name} failed")

            return AgentOutput(
                agent_name=self.name,
                success=False,
                error=error_msg,
                execution_time_seconds=execution_time,
                logs=self.logs
            )

    @abstractmethod
    def run(self, context: AgentContext) -> Dict[str, Any]:
        """
        Run the agent-specific logic.
        Must be implemented by each agent.

        Returns:
            Dict containing the agent's output data
        """
        pass

    def _analyze_weak_subjects(
        self,
        academic_data: AcademicData,
        threshold: float = 0
    ) -> List[Dict[str, Any]]:
        """Identify subjects where the student is below threshold"""
        threshold = threshold or settings.WEAK_TOPIC_THRESHOLD
        weak_subjects = []

        for subject_score in academic_data.subject_scores:
            if subject_score.average_score < threshold:
                weak_topics = [
                    {
                        "topic_id": ts.topic_id,
                        "topic_name": ts.topic_name,
                        "score": ts.score,
                        "is_core": ts.is_core_topic,
                        "exam_frequency": ts.exam_frequency
                    }
                    for ts in subject_score.topic_scores
                    if ts.score < threshold
                ]

                subject_val = subject_score.subject.value
                weak_subjects.append({
                    "subject": get_subject_display_name(subject_val),
                    "subject_key": subject_val,
                    "average_score": subject_score.average_score,
                    "weak_topics": weak_topics,
                    "gap": threshold - subject_score.average_score
                })

        # Sort by gap (largest gap first)
        weak_subjects.sort(key=lambda x: x["gap"], reverse=True)
        return weak_subjects

    def _get_psychology_adaptations(
        self,
        psychology_data: PsychologyData
    ) -> Dict[str, List[str]]:
        """Generate psychology-based adaptations for learning path"""
        adaptations = {
            "workload": [],
            "feedback": [],
            "resources": [],
            "support": []
        }

        if psychology_data.learning_behavior:
            lb = psychology_data.learning_behavior

            # High test anxiety
            if lb.self_efficacy < settings.LOW_THRESHOLD:
                adaptations["workload"].append("Chia nhỏ mục tiêu, tăng kiểm tra ngắn")
                adaptations["feedback"].append("Phản hồi tích cực, khích lệ thường xuyên")
                adaptations["support"].append("Cần hỗ trợ thường xuyên hơn")

            # Low time management
            if lb.time_management < settings.LOW_THRESHOLD:
                adaptations["workload"].append("Thêm khối ' rèn kỹ năng quản lý thời gian'")
                adaptations["support"].append("Lập kế hoạch chi tiết hơn")

        if psychology_data.mslq:
            mslq = psychology_data.mslq

            # High test anxiety
            if mslq.test_anxiety > settings.HIGH_THRESHOLD:
                adaptations["feedback"].append("Xen kẽ mock test đang 'thi thử an toàn'")
                adaptations["workload"].append("Giảm áp lực kiểm tra")

            # Low self-efficacy
            if mslq.self_efficacy < settings.LOW_THRESHOLD:
                adaptations["support"].append("Tăng hỗ trợ, đặt mục tiêu vừa sức")
                adaptations["feedback"].append("Nhiều feedback và khích lệ")

        if psychology_data.big_five:
            bf = psychology_data.big_five

            # High conscientiousness - can handle heavier workload
            if bf.conscientiousness > 0.7:
                adaptations["workload"].append("Có thể giao thêm workload cao hơn")
                adaptations["resources"].append("Kế hoạch chi tiết, có cấu trúc")

        if psychology_data.vark:
            style = psychology_data.vark.dominant_style.value
            resource_suggestions = {
                "visual": ["Sơ đồ tư duy", "Infographics", "Video minh họa"],
                "auditory": ["Podcast", "Audio lectures", "Thảo luận nhóm"],
                "reading_writing": ["Tài liệu văn bản", "Ghi chép", "Bài tập viết"],
                "kinesthetic": ["Bài tập thực hành", "Dự án thực tế", "Thí nghiệm"]
            }
            adaptations["resources"].extend(
                resource_suggestions.get(style, [])
            )

        return adaptations

    def _calculate_study_hours(
        self,
        subjects: List[str],
        priorities: Dict[str, str],
        available_hours: float
    ) -> Dict[str, float]:
        """Calculate recommended study hours per subject"""
        # Weight by priority
        weights = {"critical": 4, "high": 3, "medium": 2, "low": 1}

        total_weight = sum(
            weights.get(priorities.get(s, "medium"), 2)
            for s in subjects
        )

        hours_distribution = {}
        for subject in subjects:
            priority = priorities.get(subject, "medium")
            weight = weights.get(priority, 2)
            hours_distribution[subject] = round(
                (weight / total_weight) * available_hours, 1
            )

        return hours_distribution
