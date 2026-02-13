"""
Contacts API endpoints.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.models.database import get_db
from app.models.schemas import (
    ContactCreate, ContactUpdate, ContactListItem, ContactDetail,
    ContactWithTimeline, MeetingCreate, MeetingListItem, ActionPlaybookDetail
)
from app.services.contact_service import contact_service, meeting_service
from app.api.dependencies import CurrentUser

router = APIRouter(prefix="/contacts", tags=["Contacts"])


# ==================== Contacts ====================
@router.get("", response_model=list[ContactListItem])
async def list_contacts(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None, description="Search by name, company, or position"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """
    List all contacts for the current user.

    - **search**: Optional search term to filter by name, company, or position
    - **skip**: Number of results to skip (pagination)
    - **limit**: Maximum number of results to return
    """
    contacts, _ = contact_service.list_contacts(db, current_user.id, search, skip, limit)
    return contacts


@router.post("", response_model=ContactDetail, status_code=201)
async def create_contact(
    contact: ContactCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Create a new contact.

    All fields are optional except for basic identification.
    """
    return contact_service.create_contact(db, current_user.id, contact)


@router.get("/{contact_id}", response_model=ContactDetail)
async def get_contact(
    contact_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Get a specific contact by ID.
    """
    contact = contact_service.get_contact(db, contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactDetail)
async def update_contact(
    contact_id: int,
    contact_update: ContactUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Update a contact.

    Only include fields that should be updated.
    """
    contact = contact_service.update_contact(db, contact_id, current_user.id, contact_update)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", status_code=204)
async def delete_contact(
    contact_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Delete a contact.

    This will also delete all associated meetings and action playbooks.
    """
    success = contact_service.delete_contact(db, contact_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return Response(status_code=204)


# ==================== Contact Detail with Timeline ====================
class ContactTimelineResponse(BaseModel):
    """Response for contact with timeline."""
    contact: ContactDetail
    meetings: list[MeetingListItem]
    action_playbook: Optional[ActionPlaybookDetail] = None


@router.get("/{contact_id}/timeline", response_model=ContactTimelineResponse)
async def get_contact_timeline(
    contact_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Get a contact with full timeline and action playbook.

    This includes:
    - All contact information (Identity + Status)
    - All meetings (Timeline)
    - Action playbook recommendations
    """
    data = contact_service.get_contact_with_timeline(db, contact_id, current_user.id)
    if not data:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {
        "contact": data["contact"],
        "meetings": data["meetings"],
        "action_playbook": data["action_playbook"]
    }


# ==================== Export ====================
@router.get("/{contact_id}/export")
async def export_contact_markdown(
    contact_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Export a contact as a Markdown file.

    Returns a downloadable Markdown file with all contact information.
    """
    markdown = contact_service.export_contact_markdown(db, contact_id, current_user.id)
    if not markdown:
        raise HTTPException(status_code=404, detail="Contact not found")

    contact = contact_service.get_contact(db, contact_id, current_user.id)
    filename = f"{contact.name or 'contact'}_{contact_id}.md"

    return Response(
        content=markdown,
        media_type="text/markdown",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )


# ==================== Meetings ====================
@router.post("/{contact_id}/meetings", response_model=MeetingListItem, status_code=201)
async def add_meeting_to_contact(
    contact_id: int,
    meeting: MeetingCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Add a meeting to a specific contact.

    The meeting text will be processed by LLM to extract structured information.
    """
    # Verify contact exists
    contact = contact_service.get_contact(db, contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    # Create meeting (overwrite contact_name with actual contact name)
    meeting.contact_name = contact.name
    result = await meeting_service.create_meeting_from_text(db, current_user.id, meeting)
    return result


@router.get("/{contact_id}/meetings", response_model=list[MeetingListItem])
async def list_contact_meetings(
    contact_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """
    List all meetings for a specific contact.
    """
    # Verify contact exists
    contact = contact_service.get_contact(db, contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    meetings, _ = meeting_service.list_meetings(db, current_user.id, contact_id, skip, limit)
    return meetings


# ==================== Standalone Meetings ====================
standalone_router = APIRouter(prefix="/meetings", tags=["Meetings"])


@standalone_router.post("", response_model=MeetingListItem, status_code=201)
async def create_meeting(
    meeting: MeetingCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Create a new meeting from conversation text.

    If contact_name is provided, will try to match existing contact.
    Otherwise, will create a new contact automatically.
    """
    result = await meeting_service.create_meeting_from_text(db, current_user.id, meeting)
    return result


@standalone_router.get("", response_model=list[MeetingListItem])
async def list_meetings(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
    contact_id: Optional[int] = Query(None, description="Filter by contact ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """
    List all meetings for the current user.

    Can be filtered by contact_id.
    """
    meetings, _ = meeting_service.list_meetings(db, current_user.id, contact_id, skip, limit)
    return meetings


@standalone_router.get("/{meeting_id}", response_model=MeetingListItem)
async def get_meeting(
    meeting_id: int,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """
    Get a specific meeting by ID.
    """
    meeting = meeting_service.get_meeting(db, meeting_id, current_user.id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting
