"""
Database models for Rapport contact memory system.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base
import enum


class MeetingStatus(str, enum.Enum):
    """Meeting processing status."""
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class User(Base):
    """User model for authentication."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    contacts = relationship("Contact", back_populates="user", cascade="all, delete-orphan")
    meetings = relationship("Meeting", back_populates="user", cascade="all, delete-orphan")


class Contact(Base):
    """
    Contact model representing a person in the user's network.
    Stores Layer A (Identity) and Layer B (Status) information.
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Basic info (Layer A: Identity)
    name = Column(String(100), index=True)
    nickname = Column(String(100))
    gender = Column(String(20))
    age_group = Column(String(50))
    hometown = Column(String(100))
    city = Column(String(100))
    phone = Column(String(50))
    email = Column(String(255))
    wechat = Column(String(100))
    linkedin = Column(String(255))

    # Education (Layer A: Identity)
    education_school = Column(String(200))
    education_major = Column(String(200))
    education_degree = Column(String(50))

    # Career summary (Layer A: Identity)
    career_summary = Column(Text)

    # Communication preferences (Layer A: Identity)
    preferred_contact_method = Column(String(50))
    preferred_contact_time = Column(String(100))
    communication_style = Column(String(100))

    # Current status (Layer B: Status)
    current_company = Column(String(200))
    current_position = Column(String(200))
    current_industry = Column(String(100))
    current_location = Column(String(100))
    startup_status = Column(String(100))

    # Focus areas (Layer B: Status)
    focus_topics = Column(JSON)  # List of topics
    current_projects = Column(JSON)  # List of projects

    # Goals (Layer B: Status)
    short_term_goals = Column(JSON)  # List of goals
    long_term_goals = Column(JSON)  # List of goals

    # Needs (Layer B: Status)
    resource_needs = Column(JSON)  # What they need: people, funding, channels, etc.
    resource_offers = Column(JSON)  # What they can offer

    # Emotional context (Layer B: Status)
    excitement_points = Column(JSON)  # Recent excitement sources
    anxiety_points = Column(JSON)  # Recent anxiety sources
    sensitive_points = Column(JSON)  # Sensitive topics to avoid

    # Metadata
    last_meeting_date = Column(DateTime(timezone=True))
    last_verified_at = Column(DateTime(timezone=True))
    relationship_stage = Column(String(50))  # new, acquaintance, friend, ally, key_partner
    temperature_score = Column(Float)  # 0-100 relationship health score
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="contacts")
    meetings = relationship("Meeting", back_populates="contact", cascade="all, delete-orphan")
    action_playbooks = relationship("ActionPlaybook", back_populates="contact", cascade="all, delete-orphan", uselist=False)


class Meeting(Base):
    """
    Meeting model representing a single interaction/conversation.
    Stores Layer C (Timeline) information - append-only interaction history.
    """
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)

    # Basic info
    meeting_date = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(200))
    scenario = Column(String(200))  # Activity, dinner, meeting, etc.

    # Content
    raw_text = Column(Text, nullable=False)  # Original conversation text
    topics = Column(JSON)  # List of topics discussed
    key_facts = Column(JSON)  # Facts explicitly stated
    sentiment = Column(String(20))  # positive, neutral, negative

    # Commitments
    my_commitments = Column(JSON)  # What I promised
    their_commitments = Column(JSON)  # What they promised

    # Conversation hooks
    open_loops = Column(JSON)  # Unfinished topics for next time
    next_conversation_hooks = Column(JSON)  # Questions/topics for next conversation

    # Processing status
    status = Column(Enum(MeetingStatus), default=MeetingStatus.PROCESSING)
    error_message = Column(Text)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="meetings")
    contact = relationship("Contact", back_populates="meetings")


class ActionPlaybook(Base):
    """
    Action Playbook model storing Layer D (Action Playbook) information.
    Derived from Identity/Status/Timeline to provide actionable insights.
    """
    __tablename__ = "action_playbooks"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False, unique=True)

    # D1. Gift & Care
    preferences = Column(JSON)  # Food, drinks, sports, hobbies, brand preferences
    taboos = Column(JSON)  # Dislikes, sensitive topics, allergies, values to avoid
    gift_occasions = Column(JSON)  # Birthday, holidays, project milestones
    gift_recommendations = Column(JSON)  # Suggested gifts by tier (small/medium/formal)

    # D2. Conversation Hooks
    top_topics = Column(JSON)  # Top 3 most engaging topics
    open_loops = Column(JSON)  # Unfinished conversation threads
    conversation_questions = Column(JSON)  # 5-10 questions for next conversation
    conversation_avoid = Column(JSON)  # Topics/phrases to avoid

    # D3. Collaboration Map
    how_i_can_help_them = Column(JSON)  # Ways I can assist them
    how_they_can_help_me = Column(JSON)  # Ways they can assist me
    exchange_boundaries = Column(JSON)  # Principles to avoid transactional relationships
    contact_rhythm = Column(JSON)  # Frequency, style of communication

    # D4. Relationship Health
    relationship_stage = Column(String(50))
    temperature_score = Column(Float)  # 0-100
    recent_risks = Column(JSON)  # Outstanding follow-ups, sensitivity,误会 risks
    next_action = Column(JSON)  # Suggested next action

    # Evidence tracking
    evidence_refs = Column(JSON)  # References to meetings for each recommendation

    # Metadata
    last_updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    contact = relationship("Contact", back_populates="action_playbooks")
