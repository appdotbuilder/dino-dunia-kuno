from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


# Enums for type safety
class GradeLevel(str, Enum):
    GRADE_4 = "grade_4"
    GRADE_5 = "grade_5"
    GRADE_6 = "grade_6"


class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class MaterialType(str, Enum):
    LESSON_PLAN = "lesson_plan"
    PRESENTATION = "presentation"
    TEXT = "text"
    IMAGE = "image"
    ACTIVITY_SHEET = "activity_sheet"
    GUIDE = "guide"


class QuizQuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_IN_THE_BLANK = "fill_in_the_blank"


class BadgeType(str, Enum):
    LEVEL_COMPLETION = "level_completion"
    STREAK = "streak"
    PERFECT_SCORE = "perfect_score"
    EXPLORER = "explorer"
    HISTORIAN = "historian"


# Base User Model
class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True)
    email: str = Field(max_length=255, unique=True)
    full_name: str = Field(max_length=100)
    role: UserRole = Field(default=UserRole.STUDENT)
    grade_level: Optional[GradeLevel] = Field(default=None)
    school_name: Optional[str] = Field(default=None, max_length=200)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    quiz_attempts: List["QuizAttempt"] = Relationship(back_populates="user")
    user_progress: List["UserProgress"] = Relationship(back_populates="user")
    user_badges: List["UserBadge"] = Relationship(back_populates="user")


# Historical Periods
class HistoricalPeriod(SQLModel, table=True):
    __tablename__ = "historical_periods"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    description: str = Field(max_length=1000)
    start_year: Optional[int] = Field(default=None)
    end_year: Optional[int] = Field(default=None)
    image_url: Optional[str] = Field(default=None, max_length=500)
    display_order: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    learning_modules: List["LearningModule"] = Relationship(back_populates="historical_period")
    quiz_levels: List["QuizLevel"] = Relationship(back_populates="historical_period")
    historical_figures: List["HistoricalFigure"] = Relationship(back_populates="historical_period")


# Learning Modules Feature
class LearningModule(SQLModel, table=True):
    __tablename__ = "learning_modules"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: str = Field(max_length=1000)
    historical_period_id: int = Field(foreign_key="historical_periods.id")
    grade_level: GradeLevel
    curriculum_alignment: str = Field(max_length=500)
    learning_objectives: List[str] = Field(default=[], sa_column=Column(JSON))
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    historical_period: HistoricalPeriod = Relationship(back_populates="learning_modules")
    teaching_materials: List["TeachingMaterial"] = Relationship(back_populates="learning_module")


class TeachingMaterial(SQLModel, table=True):
    __tablename__ = "teaching_materials"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: str = Field(max_length=1000)
    learning_module_id: int = Field(foreign_key="learning_modules.id")
    material_type: MaterialType
    file_url: Optional[str] = Field(default=None, max_length=500)
    content: Optional[str] = Field(default=None)
    material_metadata: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    is_validated: bool = Field(default=False)
    display_order: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    learning_module: LearningModule = Relationship(back_populates="teaching_materials")


# Quiz Adventure Feature
class QuizLevel(SQLModel, table=True):
    __tablename__ = "quiz_levels"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    description: str = Field(max_length=1000)
    historical_period_id: int = Field(foreign_key="historical_periods.id")
    level_number: int
    unlock_requirements: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    rewards: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.EASY)
    points_reward: int = Field(default=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    historical_period: HistoricalPeriod = Relationship(back_populates="quiz_levels")
    quiz_questions: List["QuizQuestion"] = Relationship(back_populates="quiz_level")
    quiz_attempts: List["QuizAttempt"] = Relationship(back_populates="quiz_level")


class QuizQuestion(SQLModel, table=True):
    __tablename__ = "quiz_questions"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    quiz_level_id: int = Field(foreign_key="quiz_levels.id")
    question_text: str = Field(max_length=1000)
    question_type: QuizQuestionType
    options: List[str] = Field(default=[], sa_column=Column(JSON))
    correct_answer: str = Field(max_length=500)
    explanation: str = Field(max_length=1000)
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.EASY)
    points_value: int = Field(default=10)
    image_url: Optional[str] = Field(default=None, max_length=500)
    display_order: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    quiz_level: QuizLevel = Relationship(back_populates="quiz_questions")


class QuizAttempt(SQLModel, table=True):
    __tablename__ = "quiz_attempts"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    quiz_level_id: int = Field(foreign_key="quiz_levels.id")
    score: int = Field(default=0)
    max_score: int
    completion_time: Optional[int] = Field(default=None)  # in seconds
    answers: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    is_completed: bool = Field(default=False)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)

    # Relationships
    user: User = Relationship(back_populates="quiz_attempts")
    quiz_level: QuizLevel = Relationship(back_populates="quiz_attempts")


# Vocab Explorer Feature
class VocabularyTerm(SQLModel, table=True):
    __tablename__ = "vocabulary_terms"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    term: str = Field(max_length=200, unique=True)
    definition: str = Field(max_length=2000)
    pronunciation: Optional[str] = Field(default=None, max_length=500)
    audio_url: Optional[str] = Field(default=None, max_length=500)
    image_urls: List[str] = Field(default=[], sa_column=Column(JSON))
    historical_context: Optional[str] = Field(default=None, max_length=2000)
    related_periods: List[int] = Field(default=[], sa_column=Column(JSON))
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.EASY)
    usage_count: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    term_connections: List["TermConnection"] = Relationship(
        back_populates="source_term", sa_relationship_kwargs={"foreign_keys": "TermConnection.source_term_id"}
    )
    connected_terms: List["TermConnection"] = Relationship(
        back_populates="target_term", sa_relationship_kwargs={"foreign_keys": "TermConnection.target_term_id"}
    )


class TermConnection(SQLModel, table=True):
    __tablename__ = "term_connections"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    source_term_id: int = Field(foreign_key="vocabulary_terms.id")
    target_term_id: int = Field(foreign_key="vocabulary_terms.id")
    connection_type: str = Field(max_length=100)  # e.g., "related_to", "part_of", "caused_by"
    description: Optional[str] = Field(default=None, max_length=500)
    strength: int = Field(default=1)  # 1-5 scale
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    source_term: VocabularyTerm = Relationship(
        back_populates="term_connections", sa_relationship_kwargs={"foreign_keys": "TermConnection.source_term_id"}
    )
    target_term: VocabularyTerm = Relationship(
        back_populates="connected_terms", sa_relationship_kwargs={"foreign_keys": "TermConnection.target_term_id"}
    )


# Hero's Diary Feature
class HistoricalFigure(SQLModel, table=True):
    __tablename__ = "historical_figures"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    birth_date: Optional[datetime] = Field(default=None)
    death_date: Optional[datetime] = Field(default=None)
    biography: str = Field(max_length=5000)
    historical_period_id: int = Field(foreign_key="historical_periods.id")
    role_description: str = Field(max_length=1000)
    portrait_url: Optional[str] = Field(default=None, max_length=500)
    achievements: List[str] = Field(default=[], sa_column=Column(JSON))
    famous_quotes: List[str] = Field(default=[], sa_column=Column(JSON))
    historical_significance: str = Field(max_length=2000)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    historical_period: HistoricalPeriod = Relationship(back_populates="historical_figures")
    diary_entries: List["DiaryEntry"] = Relationship(back_populates="historical_figure")
    multimedia_items: List["MultimediaItem"] = Relationship(back_populates="historical_figure")
    ar_models: List["ARModel"] = Relationship(back_populates="historical_figure")


class DiaryEntry(SQLModel, table=True):
    __tablename__ = "diary_entries"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    historical_figure_id: int = Field(foreign_key="historical_figures.id")
    title: str = Field(max_length=200)
    content: str = Field(max_length=5000)
    entry_date: datetime  # Historical date the entry represents
    emotional_tone: Optional[str] = Field(default=None, max_length=100)
    key_events: List[str] = Field(default=[], sa_column=Column(JSON))
    historical_context: str = Field(max_length=2000)
    display_order: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    historical_figure: HistoricalFigure = Relationship(back_populates="diary_entries")


class MultimediaItem(SQLModel, table=True):
    __tablename__ = "multimedia_items"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    historical_figure_id: int = Field(foreign_key="historical_figures.id")
    title: str = Field(max_length=200)
    description: str = Field(max_length=1000)
    media_type: str = Field(max_length=50)  # photo, document, audio, video
    file_url: str = Field(max_length=500)
    thumbnail_url: Optional[str] = Field(default=None, max_length=500)
    media_metadata: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    display_order: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    historical_figure: HistoricalFigure = Relationship(back_populates="multimedia_items")


# Augmented Reality Feature
class ARModel(SQLModel, table=True):
    __tablename__ = "ar_models"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    historical_figure_id: int = Field(foreign_key="historical_figures.id")
    model_name: str = Field(max_length=200)
    model_file_url: str = Field(max_length=500)
    texture_urls: List[str] = Field(default=[], sa_column=Column(JSON))
    animation_data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    trigger_images: List[str] = Field(default=[], sa_column=Column(JSON))  # Images that trigger AR
    interaction_scripts: List[Dict[str, Any]] = Field(default=[], sa_column=Column(JSON))
    scale_factor: float = Field(default=1.0)
    position_offset: Dict[str, float] = Field(default={}, sa_column=Column(JSON))
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    historical_figure: HistoricalFigure = Relationship(back_populates="ar_models")


# Gamification System
class Badge(SQLModel, table=True):
    __tablename__ = "badges"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    description: str = Field(max_length=1000)
    badge_type: BadgeType
    icon_url: str = Field(max_length=500)
    requirements: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    points_value: int = Field(default=50)
    rarity_level: int = Field(default=1)  # 1-5 scale
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user_badges: List["UserBadge"] = Relationship(back_populates="badge")


class UserBadge(SQLModel, table=True):
    __tablename__ = "user_badges"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    badge_id: int = Field(foreign_key="badges.id")
    earned_at: datetime = Field(default_factory=datetime.utcnow)
    progress_data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))

    # Relationships
    user: User = Relationship(back_populates="user_badges")
    badge: Badge = Relationship(back_populates="user_badges")


class UserProgress(SQLModel, table=True):
    __tablename__ = "user_progress"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    quiz_level_id: Optional[int] = Field(default=None, foreign_key="quiz_levels.id")
    historical_figure_id: Optional[int] = Field(default=None, foreign_key="historical_figures.id")
    progress_type: str = Field(max_length=100)  # quiz_completed, diary_read, vocab_explored, ar_viewed
    total_points: int = Field(default=0)
    completion_percentage: float = Field(default=0.0)
    streak_count: int = Field(default=0)
    last_activity_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="user_progress")


# Schema Models for API/Forms (non-persistent)
class UserCreate(SQLModel, table=False):
    username: str = Field(max_length=50)
    email: str = Field(max_length=255)
    full_name: str = Field(max_length=100)
    role: UserRole = Field(default=UserRole.STUDENT)
    grade_level: Optional[GradeLevel] = Field(default=None)
    school_name: Optional[str] = Field(default=None, max_length=200)


class UserUpdate(SQLModel, table=False):
    full_name: Optional[str] = Field(default=None, max_length=100)
    grade_level: Optional[GradeLevel] = Field(default=None)
    school_name: Optional[str] = Field(default=None, max_length=200)
    is_active: Optional[bool] = Field(default=None)


class QuizQuestionCreate(SQLModel, table=False):
    quiz_level_id: int
    question_text: str = Field(max_length=1000)
    question_type: QuizQuestionType
    options: List[str] = Field(default=[])
    correct_answer: str = Field(max_length=500)
    explanation: str = Field(max_length=1000)
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.EASY)
    points_value: int = Field(default=10)
    image_url: Optional[str] = Field(default=None, max_length=500)


class QuizAttemptCreate(SQLModel, table=False):
    user_id: int
    quiz_level_id: int
    max_score: int


class VocabularyTermCreate(SQLModel, table=False):
    term: str = Field(max_length=200)
    definition: str = Field(max_length=2000)
    pronunciation: Optional[str] = Field(default=None, max_length=500)
    audio_url: Optional[str] = Field(default=None, max_length=500)
    image_urls: List[str] = Field(default=[])
    historical_context: Optional[str] = Field(default=None, max_length=2000)
    related_periods: List[int] = Field(default=[])
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.EASY)


class HistoricalFigureCreate(SQLModel, table=False):
    name: str = Field(max_length=200)
    birth_date: Optional[datetime] = Field(default=None)
    death_date: Optional[datetime] = Field(default=None)
    biography: str = Field(max_length=5000)
    historical_period_id: int
    role_description: str = Field(max_length=1000)
    portrait_url: Optional[str] = Field(default=None, max_length=500)
    achievements: List[str] = Field(default=[])
    famous_quotes: List[str] = Field(default=[])
    historical_significance: str = Field(max_length=2000)


class DiaryEntryCreate(SQLModel, table=False):
    historical_figure_id: int
    title: str = Field(max_length=200)
    content: str = Field(max_length=5000)
    entry_date: datetime
    emotional_tone: Optional[str] = Field(default=None, max_length=100)
    key_events: List[str] = Field(default=[])
    historical_context: str = Field(max_length=2000)
    display_order: int = Field(default=0)
