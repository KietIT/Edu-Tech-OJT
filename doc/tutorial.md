# Agentic AI System - Complete Tutorial

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Data Flow](#3-data-flow)
4. [Input Schemas](#4-input-schemas)
5. [Agent Details](#5-agent-details)
6. [Output Schema Analysis](#6-output-schema-analysis)
7. [How to Run](#7-how-to-run)
8. [Integration Guide](#8-integration-guide)
9. [Future AI Integration](#9-future-ai-integration)

---

## 1. Project Overview

### What is this system?

The **Agentic AI System** is a personalized learning path generator for Vietnamese high school students (THPT). It analyzes student data and generates customized learning recommendations through three specialized AI agents.

### Key Features

- **Multi-Agent Architecture**: 3 agents run in parallel for different aspects of learning
- **Psychology-Aware**: Considers learning styles, motivation, anxiety levels
- **Vietnamese Education System**: Designed for THPT (grades 9-12) and exam blocks (A00, B00, D01, etc.)
- **Human-in-the-Loop**: Results require teacher/advisor approval before being shown to students

### Project Structure

```
agentic_ai/
├── __init__.py              # Package exports
├── main.py                  # Main entry point & API
├── config.py                # Configuration settings
├── llm_client.py            # LLM client for Claude API integration
├── run_test.py              # Test runner script
├── show_result.py           # Result visualization utility
├── requirements.txt         # Dependencies
│
├── agents/                  # AI Agents
│   ├── __init__.py
│   ├── base.py              # BaseAgent class + AgentContext
│   ├── orchestrator.py      # OrchestratorAgent (coordinator)
│   ├── remedial_agent.py    # Short-term remediation (4-8 weeks)
│   ├── strategic_agent.py   # Long-term THPT prep (12-24 months)
│   └── career_agent.py      # Career-oriented paths
│
├── schemas/                 # Pydantic data models
│   ├── __init__.py
│   ├── student.py           # StudentProfile, AcademicData
│   ├── psychology.py        # MSLQ, Big Five, VARK, etc.
│   ├── paths.py             # RemedialPath, StrategicPath, CareerPath
│   └── output.py            # FinalPathOutput
│
└── test_data/               # Mock data for testing
    ├── __init__.py
    ├── mock_student.py      # Mock student generators
    └── mock_student_data.json
```

---

## 2. Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INPUT DATA                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │ StudentProfile  │  │  AcademicData   │  │      PsychologyData         │  │
│  │ - student_id    │  │ - test_results  │  │ - MSLQ (motivation)         │  │
│  │ - grade_level   │  │ - subject_scores│  │ - Big Five (personality)    │  │
│  │ - exam_block    │  │ - gpa           │  │ - VARK (learning style)     │  │
│  │ - career_goal   │  │ - class_rank    │  │ - Mental Health             │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR AGENT                                   │
│                                                                              │
│   Coordinates 3 agents in parallel, merges results, resolves conflicts      │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                     PARALLEL EXECUTION                               │   │
│   │                                                                      │   │
│   │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────┐   │   │
│   │  │ RemedialAgent   │ │ StrategicAgent  │ │   CareerAgent       │   │   │
│   │  │                 │ │                 │ │                     │   │   │
│   │  │ Duration:       │ │ Duration:       │ │ Duration:           │   │   │
│   │  │ 4-8 weeks       │ │ 12-24 months    │ │ Long-term           │   │   │
│   │  │                 │ │                 │ │                     │   │   │
│   │  │ Focus:          │ │ Focus:          │ │ Focus:              │   │   │
│   │  │ Fix weak topics │ │ THPT exam prep  │ │ Career preparation  │   │   │
│   │  └─────────────────┘ └─────────────────┘ └─────────────────────┘   │   │
│   │          │                   │                     │                │   │
│   └──────────┼───────────────────┼─────────────────────┼────────────────┘   │
│              │                   │                     │                     │
│              └───────────────────┼─────────────────────┘                     │
│                                  ▼                                           │
│                        ┌─────────────────┐                                   │
│                        │  Result Merger  │                                   │
│                        │  & Conflict     │                                   │
│                        │  Resolution     │                                   │
│                        └─────────────────┘                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FINAL OUTPUT                                       │
│                                                                              │
│  FinalPathOutput {                                                           │
│    student_id, generated_at,                                                 │
│    paths: { remedial, strategic, career },                                   │
│    psychology_insights,                                                      │
│    status: "pending_approval",  ← Human review required                      │
│    agent_results, processing_time                                            │
│  }                                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Agent Responsibilities

| Agent | Timeframe | Purpose | Key Output |
|-------|-----------|---------|------------|
| **RemedialPathAgent** | 4-8 weeks | Fix weak subjects/topics immediately | Weekly plans, resources, checkpoints |
| **StrategicTHPTPathAgent** | 12-24 months | Long-term exam preparation | Phase plans, subject priorities, gap analysis |
| **CareerPathAgent** | Long-term | Career/university preparation | Prerequisites, career phases, university recommendations |

---

## 3. Data Flow

### Complete Data Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Backend    │     │  Agentic AI  │     │   Frontend   │
│   (FastAPI)  │     │    System    │     │   (React)    │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       │  1. Collect Data   │                    │
       │◄───────────────────┼────────────────────┤
       │   (forms, tests,   │                    │
       │    assessments)    │                    │
       │                    │                    │
       │  2. Send Input     │                    │
       ├───────────────────►│                    │
       │   StudentProfile   │                    │
       │   AcademicData     │                    │
       │   PsychologyData   │                    │
       │                    │                    │
       │                    │  3. Process        │
       │                    │  (3 agents run     │
       │                    │   in parallel)     │
       │                    │                    │
       │  4. Return Result  │                    │
       │◄───────────────────┤                    │
       │   FinalPathOutput  │                    │
       │                    │                    │
       │  5. Store Result   │                    │
       │  (database)        │                    │
       │                    │                    │
       │  6. Teacher Review │                    │
       │◄───────────────────┼────────────────────┤
       │                    │                    │
       │  7. Approved Path  │                    │
       ├────────────────────┼───────────────────►│
       │                    │                    │  8. Display
       │                    │                    │  to Student
```

---

## 4. Input Schemas

### 4.1 StudentProfile

```python
class StudentProfile(BaseModel):
    student_id: str                    # Required: Unique ID
    name: str                          # Required: Student name
    date_of_birth: Optional[date]      # Optional: DOB
    grade_level: GradeLevel            # Required: "9", "10", "11", "12"
    exam_block: Optional[ExamBlock]    # Optional: "A00", "B00", "D01", etc.
    career_goal: Optional[CareerGoal]  # Optional: Career target
    current_skills: List[str]          # Optional: ["Python", "Tieng Anh B1"]
    available_study_hours_per_week: float = 20  # Default: 20 hours
```

**ExamBlock options:**
| Block | Subjects |
|-------|----------|
| A00 | Toan, Ly, Hoa |
| A01 | Toan, Ly, Anh |
| B00 | Toan, Hoa, Sinh |
| C00 | Van, Su, Dia |
| D01 | Toan, Van, Anh |
| D07 | Toan, Hoa, Anh |

### 4.2 AcademicData

```python
class AcademicData(BaseModel):
    test_results: List[TestResult]       # Individual test scores
    subject_scores: List[SubjectScore]   # Aggregated by subject
    gpa: Optional[float]                 # 0-10 scale
    class_rank: Optional[int]            # Rank in class
    total_students_in_class: Optional[int]

class SubjectScore(BaseModel):
    subject: Subject           # "toan", "ly", "hoa", "van", "anh", etc.
    average_score: float       # 0-100
    topic_scores: List[TopicScore]  # Detailed topic breakdown
    test_count: int

class TopicScore(BaseModel):
    topic_id: str
    topic_name: str            # e.g., "Ham so va do thi"
    score: float               # 0-100
    is_core_topic: bool        # Is this foundational?
    exam_frequency: float      # 0-1, how often in exams
```

### 4.3 PsychologyData

```python
class PsychologyData(BaseModel):
    mslq: Optional[MSLQResults]              # Motivation & learning strategies
    big_five: Optional[BigFiveResults]       # Personality traits
    vark: Optional[VARKResults]              # Learning style
    learning_behavior: Optional[LearningBehaviorResults]  # Study habits
    mental_health: Optional[MentalHealthResults]          # Risk assessment
```

#### MSLQ (Motivated Strategies for Learning Questionnaire)
Scale: 1-7 (1 = strongly disagree, 7 = strongly agree)

```python
class MSLQResults(BaseModel):
    # Motivation Scales
    intrinsic_goal_orientation: float   # Internal motivation
    extrinsic_goal_orientation: float   # External motivation (grades)
    task_value: float                   # Perceived importance
    control_of_learning_beliefs: float  # Belief in ability to control
    self_efficacy: float                # Confidence (IMPORTANT!)
    test_anxiety: float                 # Anxiety level (IMPORTANT!)

    # Learning Strategies
    rehearsal: float                    # Use of repetition
    elaboration: float                  # Connecting concepts
    organization: float                 # Structuring knowledge
    critical_thinking: float            # Analytical skills
    metacognitive_self_regulation: float  # Self-monitoring

    # Resource Management
    time_and_study_environment: float   # Time management (IMPORTANT!)
    effort_regulation: float            # Persistence
    peer_learning: float                # Group learning
    help_seeking: float                 # Willingness to ask help
```

#### Big Five Personality (scale 0-1)
```python
class BigFiveResults(BaseModel):
    openness: float           # Creativity, curiosity
    conscientiousness: float  # Organization, discipline (affects workload)
    extraversion: float       # Social energy
    agreeableness: float      # Cooperation
    neuroticism: float        # Emotional instability
```

#### VARK Learning Style
```python
class VARKResults(BaseModel):
    visual: float              # 0-100
    auditory: float            # 0-100
    reading_writing: float     # 0-100
    kinesthetic: float         # 0-100
    dominant_style: LearningStyle  # "visual", "auditory", "reading_writing", "kinesthetic", "multimodal"
```

---

## 5. Agent Details

### 5.1 RemedialPathAgent

**Purpose:** Generate short-term (4-8 weeks) plans to fix weak subjects.

**Input Analysis:**
- Identifies subjects with average_score < 80% (configurable threshold)
- Sorts weak topics by: `is_core_topic` and `exam_frequency`
- Considers psychology for adaptations

**Output Structure:**
```python
class RemedialPath(BaseModel):
    path_id: str
    duration_weeks: int          # 4-8 weeks
    start_date: date
    end_date: date
    subject_plans: List[SubjectRemedialPlan]  # Per-subject plans
    overall_goals: List[str]
    psychology_considerations: Dict[str, str]
    success_metrics: List[str]

class SubjectRemedialPlan(BaseModel):
    subject: str
    current_score: float
    target_score: float
    weak_topics: List[str]
    weekly_plans: List[WeeklyPlan]   # Week-by-week breakdown
    estimated_improvement: str       # e.g., "+15-20 diem sau 4 tuan"
```

### 5.2 StrategicTHPTPathAgent

**Purpose:** Generate long-term (12-24 months) exam preparation strategy.

**Key Logic:**
- Duration based on grade: Grade 12 = 12 months, Grade 10 = 24 months
- Prioritizes exam block subjects (e.g., A00 = Toan, Ly, Hoa)
- Creates phase plans (quarters) with progressive targets

**Output Structure:**
```python
class StrategicPath(BaseModel):
    path_id: str
    duration_months: int           # 12-24
    exam_block: str                # "A00", "D01", etc.
    subject_priorities: List[SubjectPriority]
    phases: List[PhasePlan]        # Quarterly plans
    gap_analysis: GapAnalysis      # Current vs target score
    critical_success_factors: List[str]

class SubjectPriority(BaseModel):
    subject: str
    priority: Priority             # "critical", "high", "medium", "low"
    is_exam_subject: bool
    current_score: float
    target_score: float
    gap: float
    weekly_hours_recommended: float

class GapAnalysis(BaseModel):
    current_total_score: float     # Sum of 3 exam subjects (30-point scale)
    target_total_score: float
    gap: float
    target_university: str
    competitiveness: str           # "achievable", "challenging", "stretch"
```

### 5.3 CareerPathAgent

**Purpose:** Generate career-oriented learning paths for university and beyond.

**Knowledge Base:** Contains predefined roadmaps for:
- AI / Tri tue nhan tao
- Y khoa / Medicine
- Kinh te / Economics
- Data Science

**Output Structure:**
```python
class CareerPath(BaseModel):
    path_id: str
    target_career: str
    target_field: str              # "AI", "Y khoa", etc.
    prerequisites: List[Prerequisite]
    phase_plans: List[CareerPhasePlan]  # THPT -> Pre-Uni -> Uni Year 1-4
    recommended_universities: List[str]
    industry_insights: List[str]
    psychology_fit: Dict[str, str]  # How personality fits career

class Prerequisite(BaseModel):
    name: str                      # "Lap trinh Python"
    category: str                  # "knowledge", "skill", "certification"
    status: str                    # "achieved", "in_progress", "not_started"
    current_level: str
    target_level: str
    resources: List[LearningResource]
```

---

## 6. Output Schema Analysis

### Complete FinalPathOutput

```python
class FinalPathOutput(BaseModel):
    # Identification
    student_id: str
    generated_at: datetime

    # The 3 Learning Paths
    paths: PathsOutput  # Contains: remedial, strategic, career

    # Psychology Summary
    psychology_insights: PsychologyInsights

    # Human Review Status
    status: HumanReviewStatus  # "pending_approval" by default

    # Metadata
    agent_results: List[AgentResult]  # Per-agent success/failure
    is_partial_result: bool           # True if any agent failed
    processing_time_seconds: float
    version: str
```

### PsychologyInsights (Summary for UI)

```python
class PsychologyInsights(BaseModel):
    learning_style: LearningStyle      # "visual", "auditory", etc.
    motivation: MotivationInsight      # intrinsic vs extrinsic
    self_efficacy: float               # 1-7, confidence level
    test_anxiety: float                # 1-7, anxiety level
    big_five: Dict[str, float]         # Personality summary
    support_recommendations: List[str] # Action items
    workload_recommendation: str       # "light", "medium", "heavy"
```

### Sample Output (Abbreviated)

```json
{
  "student_id": "STU_2024_001",
  "generated_at": "2024-11-15T10:30:00Z",
  "paths": {
    "remedial": {
      "path_id": "remedial_STU_2024_001_abc123",
      "duration_weeks": 6,
      "subject_plans": [
        {
          "subject": "ly",
          "current_score": 64.4,
          "target_score": 90.0,
          "weak_topics": ["Dien hoc", "Song co va song dien tu"],
          "weekly_plans": [...]
        }
      ]
    },
    "strategic": {
      "path_id": "strategic_STU_2024_001_def456",
      "duration_months": 18,
      "exam_block": "A00",
      "subject_priorities": [...],
      "gap_analysis": {
        "current_total_score": 21.9,
        "target_total_score": 27.0,
        "gap": 5.1,
        "competitiveness": "challenging"
      }
    },
    "career": {
      "path_id": "career_STU_2024_001_ghi789",
      "target_career": "Tri tue nhan tao (AI)",
      "target_field": "AI",
      "prerequisites": [...],
      "recommended_universities": ["Bach khoa Ha Noi", "DHQG Ha Noi"]
    }
  },
  "psychology_insights": {
    "learning_style": "visual",
    "self_efficacy": 4.2,
    "test_anxiety": 5.5,
    "workload_recommendation": "medium",
    "support_recommendations": [
      "Tang cuong phan hoi tich cuc va khich le",
      "Luyen tap ky thuat giam stress truoc ky thi"
    ]
  },
  "status": {
    "status": "pending_approval",
    "reviewer": null
  },
  "is_partial_result": false,
  "processing_time_seconds": 0.45
}
```

---

## 7. How to Run

### Prerequisites

```bash
# Install dependencies
pip install -r agentic_ai/requirements.txt

# Required packages:
# - pydantic>=2.0
# - pydantic-settings
# - anthropic (for AI integration)
# - python-dotenv (for environment variables)
```

### Running Tests

```powershell
# From the Edu-Tech directory (parent of agentic_ai)
cd D:\Project\Edu-Tech

# Run the test script
python -m agentic_ai.run_test
```

### Expected Output

```
============================================================
AGENTIC AI SYSTEM TEST
Personalized Learning Path Generator
============================================================

============================================================
Testing: Default Student (Nguyen Van A - Moderate)
============================================================

Student ID: STU_2024_001
Processing Time: 0.15s
Partial Result: False

Agent Results:
  - RemedialPathAgent: SUCCESS (0.03s)
  - StrategicTHPTPathAgent: SUCCESS (0.02s)
  - CareerPathAgent: SUCCESS (0.04s)

Remedial Path:
  Duration: 6 weeks
  Subjects to improve: 2
    - ly: 64% -> 90%
    - hoa: 67% -> 90%

Strategic Path:
  Duration: 18 months
  Exam Block: A00
  Subject priorities:
    - ly: critical (gap: 35.6)
    - hoa: critical (gap: 33.4)
    - toan: medium (gap: 12.0)

Career Path:
  Target Field: AI
  Target Career: Tri tue nhan tao (AI)
  Prerequisites: 3/5 achieved

Psychology Insights:
  Learning Style: visual
  Self-Efficacy: 4.2/7
  Test Anxiety: 5.5/7
  Workload: medium
  Recommendations: 2
```

### Viewing Results (show_result.py)

After running tests, you can view the detailed results with color formatting:

```powershell
# View results in terminal with colors
python -m agentic_ai.show_result
```

This displays:
- Overview (student ID, processing time, status)
- Agent execution results
- Psychology insights with visual indicators
- Remedial path details with weekly plans
- Strategic path with gap analysis
- Career path with prerequisites checklist

### Using as a Library

```python
from agentic_ai import generate_learning_path
from agentic_ai.test_data.mock_student import create_mock_student_data

# Get mock data
data = create_mock_student_data()

# Generate learning path
result = generate_learning_path(
    student_profile=data["student_profile"],
    academic_data=data["academic_data"],
    psychology_data=data["psychology_data"]
)

# Access results
print(result["paths"]["remedial"]["duration_weeks"])
print(result["psychology_insights"]["learning_style"])
```

---

## 8. Integration Guide

### 8.1 What Backend Must Provide to AI

The backend (FastAPI) must collect and provide these data to the AI system:

#### Required Data

| Data | Source | Format |
|------|--------|--------|
| `student_id` | User registration | String |
| `name` | User profile | String |
| `grade_level` | User profile | Enum: "9", "10", "11", "12" |
| `exam_block` | User selection | Enum: "A00", "B00", "D01", etc. |
| `career_goal` | Career survey | `{field, target_university, target_score}` |
| `available_study_hours_per_week` | User input | Float |
| `test_results` | Test/Quiz module | List of `TestResult` |
| `subject_scores` | Calculated from tests | List of `SubjectScore` |
| `mslq` | MSLQ questionnaire | 15 float values (1-7 scale) |
| `big_five` | Big Five questionnaire | 5 float values (0-1 scale) |
| `vark` | VARK questionnaire | 4 float values + dominant_style |

#### API Endpoint (Example)

```python
# Backend FastAPI endpoint
@app.post("/api/generate-learning-path")
async def generate_path(request: LearningPathRequest):
    """
    Request body:
    {
        "student_profile": {...},
        "academic_data": {...},
        "psychology_data": {...}
    }
    """
    from agentic_ai import generate_learning_path_from_dict

    result = generate_learning_path_from_dict(request.dict())

    # Store in database
    await db.learning_paths.insert_one(result)

    return result
```

### 8.2 What AI Returns to Backend

The AI system returns `FinalPathOutput` which backend should:

1. **Store in Database**
   ```python
   # MongoDB example
   learning_paths_collection.insert_one({
       **result,
       "created_at": datetime.utcnow(),
       "status": "pending_approval"
   })
   ```

2. **Notify Teacher/Advisor** for review

3. **After Approval**, update status and notify student

### 8.3 What Frontend Needs

Frontend should display:

#### From `paths.remedial`:
- Duration (weeks)
- List of subjects to improve with current/target scores
- Weekly plans with:
  - Learning goals
  - Resources (videos, exercises)
  - Checkpoints (quizzes)
  - Estimated hours

#### From `paths.strategic`:
- Duration (months)
- Subject priorities table
- Gap analysis visualization
- Phase timeline (quarters)

#### From `paths.career`:
- Career target and field
- Prerequisites checklist (achieved/in_progress/not_started)
- Recommended universities
- Career phase timeline

#### From `psychology_insights`:
- Learning style badge
- Self-efficacy meter
- Test anxiety indicator
- Workload recommendation
- Support recommendations list

### 8.4 Frontend Requirements for AI

Frontend must provide forms to collect:

1. **Student Profile Form**
   - Basic info (name, DOB)
   - Grade level selector
   - Exam block selector
   - Career goal form
   - Study hours input

2. **MSLQ Questionnaire** (15 questions, 1-7 scale)
   - 6 motivation questions
   - 5 learning strategy questions
   - 4 resource management questions

3. **Big Five Assessment** (simplified version)
   - 10-25 questions about personality

4. **VARK Assessment**
   - Learning preference questions

5. **Test Results** (automatic from quiz module)

---

## 9. AI Integration

### Current State

The system now uses a **hybrid approach** combining rule-based logic with Claude AI:
- **Rule-based**: Weak subjects identified by threshold (< 80%), priorities calculated by formulas
- **AI-powered**: Personalized study tips, strategic summaries, career advice, and content generation

### LLM Client (llm_client.py)

The system includes a unified LLM client for Claude API integration:

```python
from agentic_ai.llm_client import get_llm_client

llm = get_llm_client()

# Check if AI is available
if llm.is_available:
    # Generate text
    response = llm.generate(
        prompt="Generate study tips for Physics",
        system_prompt="You are an educational advisor",
        max_tokens=500,
        temperature=0.7
    )

    # Generate structured content (lower temperature)
    structured = llm.generate_structured(
        prompt="List 3 key topics for Chemistry",
        system_prompt="You are a curriculum expert"
    )
```

**Key Features:**
- Singleton pattern for efficient resource usage
- Graceful degradation when API unavailable (returns `None`)
- Configurable model and temperature
- Automatic environment variable loading from `.env`

### AI Integration

The `config.py` contains LLM configuration:

```python
class Settings(BaseSettings):
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "anthropic"
    LLM_MODEL: str = "claude-sonnet-4-20250514"
```

### AI Features by Agent

The following AI-powered features are **already implemented**:

1. **RemedialPathAgent** - AI generates:
   - Personalized study tips for weak topics
   - Weekly learning goals based on student profile
   - Overall learning strategy considering psychology

2. **StrategicTHPTPathAgent** - AI generates:
   - Strategic summary for long-term exam preparation
   - Critical success factors based on student situation
   - Phase-specific advice for each quarter

3. **CareerPathAgent** - AI generates:
   - Personalized career advice based on goals and personality
   - Industry insights for target career field
   - Roadmap advice for career phases

### Implementation Example (Already in Codebase)

```python
# In agents/remedial_agent.py
from agentic_ai.llm_client import get_llm_client

class RemedialPathAgent(BaseAgent):
    def __init__(self):
        super().__init__("RemedialPathAgent")
        self.llm = get_llm_client()

    def _generate_ai_study_tips(self, weak_topic: str, learning_style: str) -> Optional[str]:
        """Use AI to generate personalized study tips"""
        if not self.llm.is_available:
            return None

        prompt = f"""
        Generate 3 practical study tips in Vietnamese for a student who:
        - Struggles with: {weak_topic}
        - Learning style: {learning_style}

        Keep tips actionable and specific.
        """
        return self.llm.generate(prompt, max_tokens=500)
```

### Environment Setup for AI

```bash
# Create .env file in agentic_ai/
ANTHROPIC_API_KEY=sk-ant-api03-...

# Or set environment variable
export ANTHROPIC_API_KEY=sk-ant-api03-...
```

---

## Appendix: Quick Reference

### Key Thresholds (config.py)

| Setting | Value | Meaning |
|---------|-------|---------|
| `WEAK_TOPIC_THRESHOLD` | 80.0 | Below this = weak |
| `MINIMUM_SUBJECT_SCORE` | 80.0 | Non-exam subjects target |
| `LOW_THRESHOLD` | 3.0 | Psychology: needs support |
| `HIGH_THRESHOLD` | 5.0 | Psychology: strong/concerning |
| `AGENT_TIMEOUT_SECONDS` | 300 | Max agent execution time (5 min for LLM calls) |

### Priority Logic

| Condition | Priority |
|-----------|----------|
| Exam subject + gap > 30 | CRITICAL |
| Exam subject + gap > 15 | HIGH |
| Exam subject + gap <= 15 | MEDIUM |
| Non-exam + gap > 20 | MEDIUM |
| Non-exam + gap <= 20 | LOW |

### Duration Calculation

| Grade | Strategic Duration | Remedial Duration |
|-------|-------------------|-------------------|
| 9 | 24 months | 4-8 weeks |
| 10 | 24 months | 4-8 weeks |
| 11 | 18 months | 4-8 weeks |
| 12 | 12 months | 4-8 weeks |

---

## Contact & Support

For issues or questions about this system:
- Check the source code in `/agents/` for logic details
- Review `/schemas/` for data structure definitions
- Modify `config.py` for threshold adjustments
