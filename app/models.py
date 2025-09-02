from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


# Enums for better type safety
class GradeLevel(str, Enum):
    GRADE_4 = "grade_4"
    GRADE_5 = "grade_5"
    GRADE_6 = "grade_6"


class UserRole(str, Enum):
    TEACHER = "teacher"
    STUDENT = "student"
    ADMIN = "admin"


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ContentType(str, Enum):
    PRESENTATION = "presentation"
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"


class HistoricalPeriod(str, Enum):
    PREHISTORIC = "prehistoric"
    HINDU_BUDDHIST = "hindu_buddhist"
    ISLAMIC_KINGDOMS = "islamic_kingdoms"
    COLONIAL_DUTCH = "colonial_dutch"
    COLONIAL_JAPANESE = "colonial_japanese"
    INDEPENDENCE = "independence"
    POST_INDEPENDENCE = "post_independence"


class RewardType(str, Enum):
    POINTS = "points"
    BADGE = "badge"
    POWER_UP = "power_up"
    ACHIEVEMENT = "achievement"


# User Management
class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=100, unique=True)
    email: str = Field(max_length=255, unique=True)
    full_name: str = Field(max_length=200)
    role: UserRole = Field(default=UserRole.STUDENT)
    grade_level: Optional[GradeLevel] = Field(default=None)
    school_name: Optional[str] = Field(default=None, max_length=200)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    learning_modules: List["LearningModule"] = Relationship(back_populates="teacher")
    quiz_sessions: List["QuizSession"] = Relationship(back_populates="student")
    rewards: List["StudentReward"] = Relationship(back_populates="student")
    progress_records: List["StudentProgress"] = Relationship(back_populates="student")


# 1. Learning Module System
class LearningModule(SQLModel, table=True):
    __tablename__ = "learning_modules"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: str = Field(max_length=1000)
    grade_level: GradeLevel
    historical_period: HistoricalPeriod
    curriculum_alignment: str = Field(max_length=500)
    learning_objectives: List[str] = Field(default=[], sa_column=Column(JSON))
    teacher_id: int = Field(foreign_key="users.id")
    is_published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    teacher: User = Relationship(back_populates="learning_modules")
    lesson_plans: List["LessonPlan"] = Relationship(back_populates="module")
    teaching_materials: List["TeachingMaterial"] = Relationship(back_populates="module")
    student_activities: List["StudentActivity"] = Relationship(back_populates="module")


class LessonPlan(SQLModel, table=True):
    __tablename__ = "lesson_plans"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    module_id: int = Field(foreign_key="learning_modules.id")
    title: str = Field(max_length=200)
    duration_minutes: int = Field(gt=0)
    objectives: List[str] = Field(default=[], sa_column=Column(JSON))
    activities: List[Dict[str, Any]] = Field(default=[], sa_column=Column(JSON))
    assessment_criteria: List[str] = Field(default=[], sa_column=Column(JSON))
    gamification_elements: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    module: LearningModule = Relationship(back_populates="lesson_plans")


class TeachingMaterial(SQLModel, table=True):
    __tablename__ = "teaching_materials"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    module_id: int = Field(foreign_key="learning_modules.id")
    title: str = Field(max_length=200)
    content_type: ContentType
    file_url: str = Field(max_length=500)
    description: Optional[str] = Field(default=None, max_length=500)
    file_metadata: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    is_validated: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    module: LearningModule = Relationship(back_populates="teaching_materials")


class StudentActivity(SQLModel, table=True):
    __tablename__ = "student_activities"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    module_id: int = Field(foreign_key="learning_modules.id")
    title: str = Field(max_length=200)
    description: str = Field(max_length=1000)
    activity_type: str = Field(max_length=100)  # collaborative, explorative, individual
    instructions: List[str] = Field(default=[], sa_column=Column(JSON))
    resources_needed: List[str] = Field(default=[], sa_column=Column(JSON))
    estimated_duration: int = Field(gt=0)  # in minutes
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    module: LearningModule = Relationship(back_populates="student_activities")


# 2. Quiz Adventure System
class QuizLevel(SQLModel, table=True):
    __tablename__ = "quiz_levels"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    level_number: int = Field(ge=1)
    title: str = Field(max_length=200)
    historical_period: HistoricalPeriod
    description: str = Field(max_length=500)
    unlock_requirements: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    reward_points: int = Field(default=100, ge=0)
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.EASY)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    questions: List["QuizQuestion"] = Relationship(back_populates="level")
    sessions: List["QuizSession"] = Relationship(back_populates="level")


class QuizQuestion(SQLModel, table=True):
    __tablename__ = "quiz_questions"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    level_id: int = Field(foreign_key="quiz_levels.id")
    question_text: str = Field(max_length=1000)
    question_type: str = Field(max_length=50)  # multiple_choice, true_false, fill_blank
    options: List[str] = Field(default=[], sa_column=Column(JSON))
    correct_answer: str = Field(max_length=500)
    explanation: str = Field(max_length=1000)
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM)
    points: int = Field(default=10, ge=1)
    media_url: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    level: QuizLevel = Relationship(back_populates="questions")


class QuizSession(SQLModel, table=True):
    __tablename__ = "quiz_sessions"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="users.id")
    level_id: int = Field(foreign_key="quiz_levels.id")
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = Field(default=None)
    score: int = Field(default=0, ge=0)
    total_questions: int = Field(ge=1)
    correct_answers: int = Field(default=0, ge=0)
    is_completed: bool = Field(default=False)
    answers: List[Dict[str, Any]] = Field(default=[], sa_column=Column(JSON))

    # Relationships
    student: User = Relationship(back_populates="quiz_sessions")
    level: QuizLevel = Relationship(back_populates="sessions")


class StudentReward(SQLModel, table=True):
    __tablename__ = "student_rewards"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="users.id")
    reward_type: RewardType
    title: str = Field(max_length=200)
    description: str = Field(max_length=500)
    points_value: int = Field(default=0, ge=0)
    icon_url: Optional[str] = Field(default=None, max_length=500)
    earned_at: datetime = Field(default_factory=datetime.utcnow)
    source_activity: str = Field(max_length=200)  # quiz, vocabulary, diary, etc.

    # Relationships
    student: User = Relationship(back_populates="rewards")


# 3. Vocab Explorer System
class VocabularyTerm(SQLModel, table=True):
    __tablename__ = "vocabulary_terms"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    term: str = Field(max_length=200, unique=True)
    definition: str = Field(max_length=1000)
    historical_period: HistoricalPeriod
    etymology: Optional[str] = Field(default=None, max_length=500)
    pronunciation: Optional[str] = Field(default=None, max_length=200)
    audio_url: Optional[str] = Field(default=None, max_length=500)
    image_url: Optional[str] = Field(default=None, max_length=500)
    example_usage: Optional[str] = Field(default=None, max_length=500)
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM)
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class VocabularyConnection(SQLModel, table=True):
    __tablename__ = "vocabulary_connections"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    source_term_id: int = Field(foreign_key="vocabulary_terms.id")
    target_term_id: int = Field(foreign_key="vocabulary_terms.id")
    connection_type: str = Field(max_length=100)  # synonym, antonym, related, cause_effect, etc.
    description: Optional[str] = Field(default=None, max_length=500)
    strength: int = Field(default=1, ge=1, le=5)  # connection strength 1-5
    created_at: datetime = Field(default_factory=datetime.utcnow)


# 4. Hero's Diary System
class HistoricalFigure(SQLModel, table=True):
    __tablename__ = "historical_figures"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    birth_date: Optional[str] = Field(default=None, max_length=50)  # flexible date format
    death_date: Optional[str] = Field(default=None, max_length=50)
    birth_place: Optional[str] = Field(default=None, max_length=200)
    historical_period: HistoricalPeriod
    role_title: str = Field(max_length=200)  # Sultan, Pahlawan, Tokoh Pendidikan, etc.
    biography: str = Field(max_length=5000)
    major_achievements: List[str] = Field(default=[], sa_column=Column(JSON))
    historical_context: str = Field(max_length=2000)
    portrait_url: Optional[str] = Field(default=None, max_length=500)
    is_featured: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    diary_entries: List["DiaryEntry"] = Relationship(back_populates="figure")
    timeline_events: List["TimelineEvent"] = Relationship(back_populates="figure")
    multimedia_content: List["MultimediaContent"] = Relationship(back_populates="figure")


class DiaryEntry(SQLModel, table=True):
    __tablename__ = "diary_entries"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    figure_id: int = Field(foreign_key="historical_figures.id")
    title: str = Field(max_length=200)
    entry_date: str = Field(max_length=50)  # historical date in flexible format
    content: str = Field(max_length=5000)
    emotional_tone: str = Field(max_length=100)  # hopeful, worried, determined, etc.
    historical_context: str = Field(max_length=1000)
    is_fictional: bool = Field(default=True)  # most diary entries are interpretive
    order_sequence: int = Field(default=1, ge=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    figure: HistoricalFigure = Relationship(back_populates="diary_entries")


class TimelineEvent(SQLModel, table=True):
    __tablename__ = "timeline_events"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    figure_id: int = Field(foreign_key="historical_figures.id")
    event_title: str = Field(max_length=200)
    event_date: str = Field(max_length=50)
    description: str = Field(max_length=1000)
    significance: str = Field(max_length=500)
    location: Optional[str] = Field(default=None, max_length=200)
    related_figures: List[str] = Field(default=[], sa_column=Column(JSON))
    order_sequence: int = Field(default=1, ge=1)
    is_major_event: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    figure: HistoricalFigure = Relationship(back_populates="timeline_events")


class MultimediaContent(SQLModel, table=True):
    __tablename__ = "multimedia_content"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    figure_id: int = Field(foreign_key="historical_figures.id")
    title: str = Field(max_length=200)
    content_type: ContentType
    file_url: str = Field(max_length=500)
    description: str = Field(max_length=500)
    source_attribution: Optional[str] = Field(default=None, max_length=300)
    is_primary_source: bool = Field(default=False)
    file_metadata: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    figure: HistoricalFigure = Relationship(back_populates="multimedia_content")


# 5. Augmented Reality System
class ARTrigger(SQLModel, table=True):
    __tablename__ = "ar_triggers"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    trigger_type: str = Field(max_length=100)  # banknote, stamp, textbook_image, qr_code
    reference_image_url: str = Field(max_length=500)
    description: str = Field(max_length=500)
    recognition_data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))  # image processing metadata
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    ar_experiences: List["ARExperience"] = Relationship(back_populates="trigger")


class ARExperience(SQLModel, table=True):
    __tablename__ = "ar_experiences"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    trigger_id: int = Field(foreign_key="ar_triggers.id")
    figure_id: Optional[int] = Field(default=None, foreign_key="historical_figures.id")
    title: str = Field(max_length=200)
    description: str = Field(max_length=500)
    model_3d_url: str = Field(max_length=500)
    animation_data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    interaction_scripts: List[Dict[str, Any]] = Field(default=[], sa_column=Column(JSON))
    audio_narration_url: Optional[str] = Field(default=None, max_length=500)
    duration_seconds: int = Field(default=60, ge=1)
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM)
    educational_objectives: List[str] = Field(default=[], sa_column=Column(JSON))
    is_published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    trigger: ARTrigger = Relationship(back_populates="ar_experiences")


class ARInteraction(SQLModel, table=True):
    __tablename__ = "ar_interactions"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    experience_id: int = Field(foreign_key="ar_experiences.id")
    interaction_type: str = Field(max_length=100)  # tap, gesture, voice, proximity
    trigger_condition: str = Field(max_length=200)
    response_action: str = Field(max_length=200)
    dialogue_text: Optional[str] = Field(default=None, max_length=1000)
    audio_response_url: Optional[str] = Field(default=None, max_length=500)
    animation_trigger: Optional[str] = Field(default=None, max_length=200)
    educational_content: Optional[str] = Field(default=None, max_length=1000)
    order_sequence: int = Field(default=1, ge=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Progress Tracking
class StudentProgress(SQLModel, table=True):
    __tablename__ = "student_progress"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="users.id")
    activity_type: str = Field(max_length=100)  # quiz, vocabulary, diary, ar_experience
    activity_id: int  # generic reference to any activity
    progress_percentage: int = Field(default=0, ge=0, le=100)
    completion_time: Optional[datetime] = Field(default=None)
    score: Optional[int] = Field(default=None, ge=0)
    attempts_count: int = Field(default=1, ge=1)
    last_accessed: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = Field(default=None, max_length=500)

    # Relationships
    student: User = Relationship(back_populates="progress_records")


# Application Usage Analytics
class UsageAnalytics(SQLModel, table=True):
    __tablename__ = "usage_analytics"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    feature_used: str = Field(max_length=100)  # learning_module, quiz, vocabulary, diary, ar
    session_duration: int = Field(default=0, ge=0)  # in seconds
    actions_performed: List[str] = Field(default=[], sa_column=Column(JSON))
    device_info: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Non-persistent schemas for validation and API
class UserCreate(SQLModel, table=False):
    username: str = Field(max_length=100)
    email: str = Field(max_length=255)
    full_name: str = Field(max_length=200)
    role: UserRole = Field(default=UserRole.STUDENT)
    grade_level: Optional[GradeLevel] = Field(default=None)
    school_name: Optional[str] = Field(default=None, max_length=200)


class UserUpdate(SQLModel, table=False):
    full_name: Optional[str] = Field(default=None, max_length=200)
    grade_level: Optional[GradeLevel] = Field(default=None)
    school_name: Optional[str] = Field(default=None, max_length=200)
    is_active: Optional[bool] = Field(default=None)


class QuizSessionCreate(SQLModel, table=False):
    student_id: int
    level_id: int
    total_questions: int = Field(ge=1)


class QuizAnswerSubmit(SQLModel, table=False):
    session_id: int
    question_id: int
    answer: str = Field(max_length=500)
    time_taken: int = Field(ge=0)  # in seconds


class VocabularyTermCreate(SQLModel, table=False):
    term: str = Field(max_length=200)
    definition: str = Field(max_length=1000)
    historical_period: HistoricalPeriod
    pronunciation: Optional[str] = Field(default=None, max_length=200)
    example_usage: Optional[str] = Field(default=None, max_length=500)
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM)
    tags: List[str] = Field(default=[])


class LearningModuleCreate(SQLModel, table=False):
    title: str = Field(max_length=200)
    description: str = Field(max_length=1000)
    grade_level: GradeLevel
    historical_period: HistoricalPeriod
    curriculum_alignment: str = Field(max_length=500)
    learning_objectives: List[str] = Field(default=[])
    teacher_id: int


class ARExperienceCreate(SQLModel, table=False):
    trigger_id: int
    figure_id: Optional[int] = Field(default=None)
    title: str = Field(max_length=200)
    description: str = Field(max_length=500)
    model_3d_url: str = Field(max_length=500)
    audio_narration_url: Optional[str] = Field(default=None, max_length=500)
    duration_seconds: int = Field(default=60, ge=1)
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM)
    educational_objectives: List[str] = Field(default=[])
