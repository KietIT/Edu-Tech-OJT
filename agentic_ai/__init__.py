# Timetable Analyzer System for Personalized Learning Schedules
# Edu-Tech Project

from .main import generate_learning_path, generate_learning_path_from_dict
from .agents import TimetableAnalyzer, AgentContext

__version__ = "2.0.0"

__all__ = [
    "generate_learning_path",
    "generate_learning_path_from_dict",
    "TimetableAnalyzer",
    "AgentContext",
]
