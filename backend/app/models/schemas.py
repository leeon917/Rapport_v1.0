"""
Pydantic schemas for API requests and responses.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any, Dict
from datetime import datetime


# ==================== Auth Schemas ====================
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


# ==================== Contact Schemas ====================
class ContactBase(BaseModel):
    """Base contact fields."""
    name: Optional[str] = None
    nickname: Optional[str] = None
    gender: Optional[str] = None
    age_group: Optional[str] = None
    hometown: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    wechat: Optional[str] = None
    linkedin: Optional[str] = None


class ContactIdentity(BaseModel):
    """Layer A: Identity fields."""
    education_school: Optional[str] = None
    education_major: Optional[str] = None
    education_degree: Optional[str] = None
    career_summary: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    preferred_contact_time: Optional[str] = None
    communication_style: Optional[str] = None


class ContactStatus(BaseModel):
    """Layer B: Status fields."""
    current_company: Optional[str] = None
    current_position: Optional[str] = None
    current_industry: Optional[str] = None
    current_location: Optional[str] = None
    startup_status: Optional[str] = None
    focus_topics: Optional[List[str]] = None
    current_projects: Optional[List[str]] = None
    short_term_goals: Optional[List[str]] = None
    long_term_goals: Optional[List[str]] = None
    resource_needs: Optional[List[str]] = None
    resource_offers: Optional[List[str]] = None
    excitement_points: Optional[List[str]] = None
    anxiety_points: Optional[List[str]] = None
    sensitive_points: Optional[List[str]] = None


class ContactCreate(ContactBase):
    """Schema for creating a contact."""
    pass


class ContactUpdate(BaseModel):
    """Schema for updating a contact."""
    name: Optional[str] = None
    nickname: Optional[str] = None
    gender: Optional[str] = None
    age_group: Optional[str] = None
    hometown: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    wechat: Optional[str] = None
    linkedin: Optional[str] = None
    education_school: Optional[str] = None
    education_major: Optional[str] = None
    education_degree: Optional[str] = None
    career_summary: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    preferred_contact_time: Optional[str] = None
    communication_style: Optional[str] = None
    current_company: Optional[str] = None
    current_position: Optional[str] = None
    current_industry: Optional[str] = None
    current_location: Optional[str] = None
    startup_status: Optional[str] = None
    focus_topics: Optional[List[str]] = None
    current_projects: Optional[List[str]] = None
    short_term_goals: Optional[List[str]] = None
    long_term_goals: Optional[List[str]] = None
    resource_needs: Optional[List[str]] = None
    resource_offers: Optional[List[str]] = None
    excitement_points: Optional[List[str]] = None
    anxiety_points: Optional[List[str]] = None
    sensitive_points: Optional[List[str]] = None
    relationship_stage: Optional[str] = None
    temperature_score: Optional[float] = None


class ContactListItem(BaseModel):
    """Contact in list view."""
    id: int
    name: Optional[str] = None
    current_company: Optional[str] = None
    current_position: Optional[str] = None
    last_meeting_date: Optional[datetime] = None
    relationship_stage: Optional[str] = None
    temperature_score: Optional[float] = None

    class Config:
        from_attributes = True


class ContactDetail(ContactBase, ContactIdentity, ContactStatus):
    """Full contact detail with all layers."""
    id: int
    last_meeting_date: Optional[datetime] = None
    last_verified_at: Optional[datetime] = None
    relationship_stage: Optional[str] = None
    temperature_score: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== Meeting Schemas ====================
class MeetingCreate(BaseModel):
    """Schema for creating a meeting from conversation text."""
    contact_name: Optional[str] = None
    raw_text: str = Field(..., min_length=10)
    meeting_date: Optional[datetime] = None
    location: Optional[str] = None
    scenario: Optional[str] = None


class MeetingListItem(BaseModel):
    """Meeting in list view."""
    id: int
    meeting_date: datetime
    location: Optional[str] = None
    scenario: Optional[str] = None
    topics: Optional[List[str]] = None
    sentiment: Optional[str] = None
    status: str

    class Config:
        from_attributes = True


class MeetingDetail(BaseModel):
    """Full meeting detail."""
    id: int
    contact_id: int
    meeting_date: datetime
    location: Optional[str] = None
    scenario: Optional[str] = None
    raw_text: str
    topics: Optional[List[str]] = None
    key_facts: Optional[List[Dict[str, Any]]] = None
    sentiment: Optional[str] = None
    my_commitments: Optional[List[Dict[str, Any]]] = None
    their_commitments: Optional[List[Dict[str, Any]]] = None
    open_loops: Optional[List[str]] = None
    next_conversation_hooks: Optional[List[str]] = None
    status: str
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Action Playbook Schemas ====================
class GiftCareSection(BaseModel):
    """D1: Gift & Care section."""
    preferences: Optional[List[str]] = None
    taboos: Optional[List[str]] = None
    gift_occasions: Optional[List[str]] = None
    gift_recommendations: Optional[Dict[str, List[str]]] = None


class ConversationHooksSection(BaseModel):
    """D2: Conversation Hooks section."""
    top_topics: Optional[List[str]] = None
    open_loops: Optional[List[str]] = None
    conversation_questions: Optional[List[str]] = None
    conversation_avoid: Optional[List[str]] = None


class CollaborationMapSection(BaseModel):
    """D3: Collaboration Map section."""
    how_i_can_help_them: Optional[List[str]] = None
    how_they_can_help_me: Optional[List[str]] = None
    exchange_boundaries: Optional[List[str]] = None
    contact_rhythm: Optional[Dict[str, Any]] = None


class RelationshipHealthSection(BaseModel):
    """D4: Relationship Health section."""
    relationship_stage: Optional[str] = None
    temperature_score: Optional[float] = None
    recent_risks: Optional[List[str]] = None
    next_action: Optional[Dict[str, Any]] = None


class ActionPlaybookDetail(BaseModel):
    """Full action playbook with all sections."""
    id: int
    contact_id: int
    gift_care: Optional[GiftCareSection] = None
    conversation_hooks: Optional[ConversationHooksSection] = None
    collaboration_map: Optional[CollaborationMapSection] = None
    relationship_health: Optional[RelationshipHealthSection] = None
    evidence_refs: Optional[Dict[str, Any]] = None
    last_updated_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Combined Response Schemas ====================
class ContactWithTimeline(ContactDetail):
    """Contact with timeline of meetings and action playbook."""
    meetings: List[MeetingListItem] = []
    action_playbook: Optional[ActionPlaybookDetail] = None


# ==================== Export Schema ====================
class ContactExport(BaseModel):
    """Schema for exporting contact data."""
    name: Optional[str] = None
    contact_info: Dict[str, Any] = {}
    identity: Dict[str, Any] = {}
    status: Dict[str, Any] = {}
    timeline: List[Dict[str, Any]] = []
    action_playbook: Dict[str, Any] = {}
