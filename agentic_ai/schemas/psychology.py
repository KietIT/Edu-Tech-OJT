"""
Psychology and learning behavior assessment schemas.
Based on MSLQ, Big Five, VARK, and custom questionnaires.
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class LearningStyle(str, Enum):
    """VARK Learning Styles"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    READING_WRITING = "reading_writing"
    KINESTHETIC = "kinesthetic"
    MULTIMODAL = "multimodal"


class MSLQResults(BaseModel):
    """
    Motivated Strategies for Learning Questionnaire (MSLQ) results.
    Scale: 1-7 (1 = strongly disagree, 7 = strongly agree)
    """
    # Motivation Scales
    intrinsic_goal_orientation: float = Field(ge=1, le=7, description="Internal motivation to learn")
    extrinsic_goal_orientation: float = Field(ge=1, le=7, description="External motivation (grades, rewards)")
    task_value: float = Field(ge=1, le=7, description="Perceived importance of learning content")
    control_of_learning_beliefs: float = Field(ge=1, le=7, description="Belief in ability to control learning outcomes")
    self_efficacy: float = Field(ge=1, le=7, description="Confidence in ability to succeed")
    test_anxiety: float = Field(ge=1, le=7, description="Anxiety about tests/exams")

    # Learning Strategy Scales
    rehearsal: float = Field(ge=1, le=7, description="Use of repetition strategies")
    elaboration: float = Field(ge=1, le=7, description="Connecting new to existing knowledge")
    organization: float = Field(ge=1, le=7, description="Structuring and summarizing")
    critical_thinking: float = Field(ge=1, le=7, description="Analytical thinking")
    metacognitive_self_regulation: float = Field(ge=1, le=7, description="Planning, monitoring, regulating")

    # Resource Management
    time_and_study_environment: float = Field(ge=1, le=7, description="Time management and study environment")
    effort_regulation: float = Field(ge=1, le=7, description="Persistence and effort control")
    peer_learning: float = Field(ge=1, le=7, description="Learning with peers")
    help_seeking: float = Field(ge=1, le=7, description="Willingness to seek help")


class BigFiveResults(BaseModel):
    """
    Big Five Personality Traits results.
    Scale: typically 1-5 or 1-7, normalized to 0-1 for this system.
    """
    openness: float = Field(ge=0, le=1, description="Openness to experience")
    conscientiousness: float = Field(ge=0, le=1, description="Organization, discipline")
    extraversion: float = Field(ge=0, le=1, description="Social energy")
    agreeableness: float = Field(ge=0, le=1, description="Cooperation, trust")
    neuroticism: float = Field(ge=0, le=1, description="Emotional instability, anxiety")


class VARKResults(BaseModel):
    """
    VARK Learning Preferences results.
    Scores indicate preference strength for each modality.
    """
    visual: float = Field(ge=0, le=100)
    auditory: float = Field(ge=0, le=100)
    reading_writing: float = Field(ge=0, le=100)
    kinesthetic: float = Field(ge=0, le=100)
    dominant_style: LearningStyle


class LearningBehaviorResults(BaseModel):
    """
    Results from the Learning Behavior Questionnaire (hanh-vi-hoc-tap.md).
    Based on 30 questions across 3 sections.
    Scale: 1-7
    """
    # Section 1: Learning Motivation (10 questions)
    learning_motivation_score: float = Field(ge=1, le=7)
    intrinsic_motivation: float = Field(ge=1, le=7, description="Questions 1-3: Internal drive")
    extrinsic_motivation: float = Field(ge=1, le=7, description="Questions 4-5: External rewards")
    task_value: float = Field(ge=1, le=7, description="Questions 6-7: Content value")
    self_efficacy: float = Field(ge=1, le=7, description="Questions 8-10: Confidence")

    # Section 2: Learning Strategies (10 questions)
    learning_strategies_score: float = Field(ge=1, le=7)
    rehearsal_strategies: float = Field(ge=1, le=7, description="Questions 11-12")
    elaboration_strategies: float = Field(ge=1, le=7, description="Questions 13-16")
    critical_thinking: float = Field(ge=1, le=7, description="Questions 17-18")
    metacognitive_regulation: float = Field(ge=1, le=7, description="Questions 19-20")

    # Section 3: Study Habits & Environment (10 questions)
    study_habits_score: float = Field(ge=1, le=7)
    daily_study_routine: float = Field(ge=1, le=7, description="Questions 21-24")
    time_management: float = Field(ge=1, le=7, description="Questions 25-28")
    study_environment: float = Field(ge=1, le=7, description="Questions 29-30")


class RiskLevel(str, Enum):
    """Mental health risk levels"""
    LOW = "low"  # 0-70 points
    MEDIUM = "medium"  # 80-150 points
    HIGH = "high"  # 160-240 points


class MentalHealthResults(BaseModel):
    """
    Results from the Mental Health Risk Assessment (tam-sinh-li.md).
    Based on 10 questions, scale 0-400.
    """
    total_score: float = Field(ge=0, le=400)
    normalized_score: float = Field(ge=0, le=240, description="Scaled score for interpretation")
    risk_level: RiskLevel
    self_perception: float = Field(ge=0, le=40, description="Q1: How others perceive you")
    social_initiative: float = Field(ge=0, le=40, description="Q2: Social behavior")
    wishes: float = Field(ge=0, le=40, description="Q3: Desires and aspirations")
    emotional_control: float = Field(ge=0, le=40, description="Q4: Control over emotions")
    morning_mood: float = Field(ge=0, le=40, description="Q5: Morning mood state")
    leisure_activities: float = Field(ge=0, le=40, description="Q6: Free time activities")
    family_gatherings: float = Field(ge=0, le=40, description="Q7: Family interaction")
    self_harm_thoughts: float = Field(ge=0, le=40, description="Q8: Self-harm ideation")
    favorite_quote: float = Field(ge=0, le=40, description="Q9: Quote preference")
    self_assessment: float = Field(ge=0, le=40, description="Q10: Self-diagnosis")
    needs_professional_support: bool = Field(default=False, description="Flag for urgent support needs")


class PsychologyData(BaseModel):
    """Complete psychology assessment data"""
    mslq: Optional[MSLQResults] = None
    big_five: Optional[BigFiveResults] = None
    vark: Optional[VARKResults] = None
    learning_behavior: Optional[LearningBehaviorResults] = None
    mental_health: Optional[MentalHealthResults] = None

    # Derived insights
    learning_style: Optional[LearningStyle] = None
    support_level_needed: str = Field(default="normal", description="low, normal, high, intensive")
    recommended_workload: str = Field(default="medium", description="light, medium, heavy")
