"""
Mock student data for testing the Agentic AI system.
Based on the specifications in agentic-ai.md section 6.
"""
from datetime import date
from typing import Dict, Any

from ..schemas.student import (
    StudentProfile,
    AcademicData,
    SubjectScore,
    TopicScore,
    TestResult,
    CareerGoal,
    GradeLevel,
    ExamBlock,
    Subject,
)
from ..schemas.psychology import (
    PsychologyData,
    MSLQResults,
    BigFiveResults,
    VARKResults,
    LearningBehaviorResults,
    MentalHealthResults,
    LearningStyle,
    RiskLevel,
)
from .mock_timetable import create_mock_timetable
from .mock_report_card import create_mock_report_card
from .mock_study_habits import create_mock_study_habits


def create_mock_student_data() -> Dict[str, Any]:
    """
    Create complete mock data for a test student.

    Student profile:
    - Name: Trịnh Vỹ Kiệt
    - Grade: 12
    - Exam block: A01 (Toán, Lý, Anh)
    - Career goal: AI/Data Science
    - Weak subjects: Physics (Lý), Chemistry (Hóa)
    - Strong subjects: Math (Toán)
    - Psychology: Moderate test anxiety, high intrinsic motivation
    """

    # Create student profile
    student_profile = StudentProfile(
        student_id="STU_2024_001",
        name="Trịnh Vỹ Kiệt",
        date_of_birth=date(2005, 3, 9),
        grade_level=GradeLevel.GRADE_12,
        exam_block=ExamBlock.A01,
        career_goal=CareerGoal(
            field="AI",
            target_university="Đại học FPT",
            target_score=27.0  # 9/10 average for 3 subjects
        ),
        current_skills=["Python cơ bản", "Tiếng Anh B1", "Excel"],
        available_study_hours_per_week=25.0
    )

    # Create academic data
    academic_data = create_mock_academic_data()

    # Create psychology data
    psychology_data = create_mock_psychology_data()

    # Create the 3 input data fields
    timetable = create_mock_timetable()
    report_card = create_mock_report_card()
    study_habits = create_mock_study_habits()

    return {
        "student_profile": student_profile,
        "academic_data": academic_data,
        "psychology_data": psychology_data,
        "timetable": timetable,
        "report_card": report_card,
        "study_habits": study_habits,
    }


def create_mock_academic_data() -> AcademicData:
    """Create mock academic data with realistic scores"""

    # Math - Strong subject
    math_topics = [
        TopicScore(topic_id="toan_01", topic_name="Hàm số và đồ thị", score=9.2, is_core_topic=True, exam_frequency=0.9),
        TopicScore(topic_id="toan_02", topic_name="Phương trình và bất phương trình", score=8.8, is_core_topic=True, exam_frequency=0.85),
        TopicScore(topic_id="toan_03", topic_name="Lượng giác", score=8.5, is_core_topic=True, exam_frequency=0.8),
        TopicScore(topic_id="toan_04", topic_name="Hình học phẳng", score=7.8, is_core_topic=True, exam_frequency=0.7),
        TopicScore(topic_id="toan_05", topic_name="Xác suất thống kê", score=9.0, is_core_topic=False, exam_frequency=0.6),
        TopicScore(topic_id="toan_06", topic_name="Dãy số, cấp số cộng, cấp số nhân", score=9.5, is_core_topic=True, exam_frequency=0.75),
    ]

    # Physics - Weak subject
    physics_topics = [
        TopicScore(topic_id="ly_01", topic_name="Cơ học", score=6.5, is_core_topic=True, exam_frequency=0.85),
        TopicScore(topic_id="ly_02", topic_name="Nhiệt học", score=7.0, is_core_topic=True, exam_frequency=0.7),
        TopicScore(topic_id="ly_03", topic_name="Điện học", score=5.5, is_core_topic=True, exam_frequency=0.9),
        TopicScore(topic_id="ly_04", topic_name="Quang học", score=7.2, is_core_topic=True, exam_frequency=0.65),
        TopicScore(topic_id="ly_05", topic_name="Sóng cơ và sóng điện tử", score=6.0, is_core_topic=True, exam_frequency=0.8),
    ]

    # Chemistry - Weak subject
    chemistry_topics = [
        TopicScore(topic_id="hoa_01", topic_name="Cấu tạo nguyên tử", score=7.5, is_core_topic=True, exam_frequency=0.7),
        TopicScore(topic_id="hoa_02", topic_name="Liên kết hóa học", score=6.8, is_core_topic=True, exam_frequency=0.75),
        TopicScore(topic_id="hoa_03", topic_name="Phản ứng hóa học", score=6.2, is_core_topic=True, exam_frequency=0.9),
        TopicScore(topic_id="hoa_04", topic_name="Hóa học hữu cơ", score=5.8, is_core_topic=True, exam_frequency=0.85),
        TopicScore(topic_id="hoa_05", topic_name="Điện phân", score=7.0, is_core_topic=True, exam_frequency=0.6),
    ]

    # Literature - Non-exam subject
    literature_topics = [
        TopicScore(topic_id="van_01", topic_name="Nghị luận xã hội", score=7.5, is_core_topic=True, exam_frequency=0.8),
        TopicScore(topic_id="van_02", topic_name="Nghị luận văn học", score=7.2, is_core_topic=True, exam_frequency=0.9),
        TopicScore(topic_id="van_03", topic_name="Đọc hiểu", score=8.0, is_core_topic=True, exam_frequency=0.7),
    ]

    # English
    english_topics = [
        TopicScore(topic_id="anh_01", topic_name="Grammar", score=7.8, is_core_topic=True, exam_frequency=0.8),
        TopicScore(topic_id="anh_02", topic_name="Vocabulary", score=8.2, is_core_topic=True, exam_frequency=0.85),
        TopicScore(topic_id="anh_03", topic_name="Reading", score=7.5, is_core_topic=True, exam_frequency=0.9),
        TopicScore(topic_id="anh_04", topic_name="Listening", score=7.0, is_core_topic=False, exam_frequency=0.5),
    ]

    subject_scores = [
        SubjectScore(
            subject=Subject.TOAN,
            average_score=8.8,
            topic_scores=math_topics,
            test_count=12
        ),
        SubjectScore(
            subject=Subject.LY,
            average_score=6.44,
            topic_scores=physics_topics,
            test_count=10
        ),
        SubjectScore(
            subject=Subject.HOA,
            average_score=6.66,
            topic_scores=chemistry_topics,
            test_count=10
        ),
        SubjectScore(
            subject=Subject.VAN,
            average_score=7.57,
            topic_scores=literature_topics,
            test_count=8
        ),
        SubjectScore(
            subject=Subject.ANH,
            average_score=7.63,
            topic_scores=english_topics,
            test_count=10
        ),
    ]

    # Sample test results
    test_results = [
        TestResult(
            test_id="test_001",
            subject=Subject.TOAN,
            topic_id="toan_01",
            topic_name="Hàm số và đồ thị",
            score=9.2,
            max_score=10,
            difficulty="medium",
            test_date=date(2024, 9, 15),
            test_type="quiz"
        ),
        TestResult(
            test_id="test_002",
            subject=Subject.LY,
            topic_id="ly_03",
            topic_name="Điện học",
            score=5.5,
            max_score=10,
            difficulty="medium",
            test_date=date(2024, 9, 20),
            test_type="quiz"
        ),
        TestResult(
            test_id="test_003",
            subject=Subject.HOA,
            topic_id="hoa_04",
            topic_name="Hóa học hữu cơ",
            score=5.8,
            max_score=10,
            difficulty="hard",
            test_date=date(2024, 9, 25),
            test_type="midterm"
        ),
        TestResult(
            test_id="test_004",
            subject=Subject.TOAN,
            topic_name="Tổng hợp",
            score=8.5,
            max_score=10,
            difficulty="hard",
            test_date=date(2024, 10, 1),
            test_type="midterm"
        ),
    ]

    return AcademicData(
        test_results=test_results,
        subject_scores=subject_scores,
        gpa=7.8,
        class_rank=8,
        total_students_in_class=45
    )


def create_mock_psychology_data() -> PsychologyData:
    """Create mock psychology assessment data"""

    # MSLQ Results (based on hanh-vi-hoc-tap.md questionnaire structure)
    mslq = MSLQResults(
        # Motivation scales
        intrinsic_goal_orientation=5.8,  # High - likes challenging tasks
        extrinsic_goal_orientation=4.5,  # Moderate - cares about grades
        task_value=5.5,                  # High - sees value in learning
        control_of_learning_beliefs=5.0,  # Moderate
        self_efficacy=4.2,               # Below average - needs confidence boost
        test_anxiety=5.5,                # Elevated - gets anxious about tests

        # Learning strategy scales
        rehearsal=4.0,                   # Moderate use of repetition
        elaboration=5.2,                 # Good at connecting concepts
        organization=4.8,                # Moderate organization
        critical_thinking=5.0,           # Good analytical skills
        metacognitive_self_regulation=4.5,  # Moderate self-regulation

        # Resource management
        time_and_study_environment=3.8,  # Needs improvement
        effort_regulation=4.5,           # Moderate persistence
        peer_learning=4.0,               # Some collaborative learning
        help_seeking=3.5                 # Reluctant to ask for help
    )

    # Big Five Personality
    big_five = BigFiveResults(
        openness=0.75,           # High - curious and creative
        conscientiousness=0.55,  # Moderate - somewhat organized
        extraversion=0.40,       # Lower - more introverted
        agreeableness=0.70,      # Good - cooperative
        neuroticism=0.55         # Moderate - some emotional variability
    )

    # VARK Learning Style
    vark = VARKResults(
        visual=75,
        auditory=45,
        reading_writing=60,
        kinesthetic=55,
        dominant_style=LearningStyle.VISUAL
    )

    # Learning Behavior Results (from hanh-vi-hoc-tap.md)
    learning_behavior = LearningBehaviorResults(
        # Section 1: Learning Motivation
        learning_motivation_score=5.2,
        intrinsic_motivation=5.8,
        extrinsic_motivation=4.5,
        task_value=5.5,
        self_efficacy=4.2,

        # Section 2: Learning Strategies
        learning_strategies_score=4.7,
        rehearsal_strategies=4.0,
        elaboration_strategies=5.2,
        critical_thinking=5.0,
        metacognitive_regulation=4.5,

        # Section 3: Study Habits
        study_habits_score=4.0,
        daily_study_routine=3.8,
        time_management=3.5,
        study_environment=4.8
    )

    # Mental Health Assessment (from tam-sinh-li.md)
    # Simulating a student with mild stress but no serious concerns
    mental_health = MentalHealthResults(
        total_score=180,  # Mid-range
        normalized_score=108,  # Scaled to 0-240
        risk_level=RiskLevel.MEDIUM,
        self_perception=30,    # Q1: Somewhat anxious in social situations
        social_initiative=25,  # Q2: Sometimes initiates
        wishes=35,             # Q3: Wants to be happier
        emotional_control=30,  # Q4: Mostly in control
        morning_mood=20,       # Q5: Variable morning mood
        leisure_activities=25, # Q6: Typical activities
        family_gatherings=30,  # Q7: Some discomfort
        self_harm_thoughts=5,  # Q8: No significant concerns (important!)
        favorite_quote=25,     # Q9: Neutral quote preference
        self_assessment=25,    # Q10: Mild awareness of anxiety
        needs_professional_support=False
    )

    return PsychologyData(
        mslq=mslq,
        big_five=big_five,
        vark=vark,
        learning_behavior=learning_behavior,
        mental_health=mental_health,
        learning_style=LearningStyle.VISUAL,
        support_level_needed="normal",
        recommended_workload="medium"
    )


# Complete mock data as a constant for easy import
MOCK_STUDENT_DATA = create_mock_student_data()


# JSON-serializable version for API testing
def get_mock_student_json() -> Dict[str, Any]:
    """Get mock student data as JSON-serializable dict"""
    data = create_mock_student_data()
    return {
        "student_profile": data["student_profile"].model_dump(),
        "academic_data": data["academic_data"].model_dump(),
        "psychology_data": data["psychology_data"].model_dump()
    }


# Additional mock students for variety testing
def create_mock_student_high_achiever() -> Dict[str, Any]:
    """Create a high-achieving student profile"""
    profile = StudentProfile(
        student_id="STU_2024_002",
        name="Tran Thi B",
        date_of_birth=date(2007, 3, 20),
        grade_level=GradeLevel.GRADE_12,
        exam_block=ExamBlock.A00,
        career_goal=CareerGoal(
            field="Data Science",
            target_university="DHQG Ha Noi",
            target_score=28.5
        ),
        current_skills=["Python trung binh", "Tieng Anh B2", "SQL co ban", "Data Analysis"],
        available_study_hours_per_week=30.0
    )

    # Điểm cao tất cả các môn (thang điểm 10)
    subject_scores = [
        SubjectScore(subject=Subject.TOAN, average_score=9.5, topic_scores=[], test_count=15),
        SubjectScore(subject=Subject.LY, average_score=9.2, topic_scores=[], test_count=12),
        SubjectScore(subject=Subject.HOA, average_score=9.0, topic_scores=[], test_count=12),
        SubjectScore(subject=Subject.VAN, average_score=8.5, topic_scores=[], test_count=10),
        SubjectScore(subject=Subject.ANH, average_score=8.8, topic_scores=[], test_count=12),
    ]

    academic_data = AcademicData(
        test_results=[],
        subject_scores=subject_scores,
        gpa=9.2,
        class_rank=1,
        total_students_in_class=45
    )

    psychology_data = PsychologyData(
        mslq=MSLQResults(
            intrinsic_goal_orientation=6.5,
            extrinsic_goal_orientation=5.0,
            task_value=6.0,
            control_of_learning_beliefs=6.0,
            self_efficacy=6.2,
            test_anxiety=3.0,  # Low anxiety
            rehearsal=5.5,
            elaboration=6.0,
            organization=6.0,
            critical_thinking=6.2,
            metacognitive_self_regulation=5.8,
            time_and_study_environment=5.5,
            effort_regulation=6.0,
            peer_learning=4.5,
            help_seeking=4.0
        ),
        big_five=BigFiveResults(
            openness=0.80,
            conscientiousness=0.85,
            extraversion=0.50,
            agreeableness=0.65,
            neuroticism=0.30
        ),
        vark=VARKResults(
            visual=65,
            auditory=55,
            reading_writing=80,
            kinesthetic=50,
            dominant_style=LearningStyle.READING_WRITING
        ),
        learning_style=LearningStyle.READING_WRITING,
        support_level_needed="low",
        recommended_workload="heavy"
    )

    return {
        "student_profile": profile,
        "academic_data": academic_data,
        "psychology_data": psychology_data
    }


def create_mock_student_struggling() -> Dict[str, Any]:
    """Create a struggling student profile"""
    profile = StudentProfile(
        student_id="STU_2024_003",
        name="Le Van C",
        date_of_birth=date(2008, 11, 8),
        grade_level=GradeLevel.GRADE_10,
        exam_block=ExamBlock.D01,  # Toan, Van, Anh
        career_goal=CareerGoal(
            field="Kinh te",
            target_university="Dai hoc Kinh te Quoc dan",
            target_score=24.0
        ),
        current_skills=["Tieng Anh A2"],
        available_study_hours_per_week=15.0
    )

    # Điểm thấp, nhiều môn yếu (thang điểm 10)
    subject_scores = [
        SubjectScore(subject=Subject.TOAN, average_score=5.5, topic_scores=[], test_count=8),
        SubjectScore(subject=Subject.VAN, average_score=6.0, topic_scores=[], test_count=8),
        SubjectScore(subject=Subject.ANH, average_score=5.0, topic_scores=[], test_count=8),
        SubjectScore(subject=Subject.LY, average_score=5.2, topic_scores=[], test_count=6),
        SubjectScore(subject=Subject.HOA, average_score=4.8, topic_scores=[], test_count=6),
    ]

    academic_data = AcademicData(
        test_results=[],
        subject_scores=subject_scores,
        gpa=5.5,
        class_rank=38,
        total_students_in_class=45
    )

    psychology_data = PsychologyData(
        mslq=MSLQResults(
            intrinsic_goal_orientation=3.5,
            extrinsic_goal_orientation=5.5,  # High external motivation
            task_value=3.8,
            control_of_learning_beliefs=3.0,
            self_efficacy=2.8,  # Very low confidence
            test_anxiety=6.2,  # High anxiety
            rehearsal=3.5,
            elaboration=3.0,
            organization=3.2,
            critical_thinking=3.5,
            metacognitive_self_regulation=2.8,
            time_and_study_environment=2.5,  # Poor time management
            effort_regulation=3.5,
            peer_learning=4.0,
            help_seeking=2.5  # Doesn't ask for help
        ),
        big_five=BigFiveResults(
            openness=0.45,
            conscientiousness=0.35,
            extraversion=0.60,
            agreeableness=0.70,
            neuroticism=0.70  # High emotional instability
        ),
        vark=VARKResults(
            visual=70,
            auditory=60,
            reading_writing=40,
            kinesthetic=80,
            dominant_style=LearningStyle.KINESTHETIC
        ),
        learning_style=LearningStyle.KINESTHETIC,
        support_level_needed="high",
        recommended_workload="light"
    )

    return {
        "student_profile": profile,
        "academic_data": academic_data,
        "psychology_data": psychology_data
    }
