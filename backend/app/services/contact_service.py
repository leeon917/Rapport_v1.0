"""
Contact service for managing contacts and meetings.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.models import Contact, Meeting, ActionPlaybook, User
from app.models.schemas import (
    ContactCreate, ContactUpdate, MeetingCreate,
    ActionPlaybookDetail
)
from app.services.llm_service import llm_service


class ContactService:
    """Service for contact-related operations."""

    @staticmethod
    def create_contact(db: Session, user_id: int, contact: ContactCreate) -> Contact:
        """Create a new contact."""
        db_contact = Contact(**contact.model_dump(exclude_none=True), user_id=user_id)
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact

    @staticmethod
    def get_contact(db: Session, contact_id: int, user_id: int) -> Optional[Contact]:
        """Get a contact by ID for a specific user."""
        return db.query(Contact).filter(
            Contact.id == contact_id,
            Contact.user_id == user_id
        ).first()

    @staticmethod
    def list_contacts(
        db: Session,
        user_id: int,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Contact], int]:
        """
        List contacts for a user with optional search.

        Returns:
            Tuple of (contacts list, total count)
        """
        query = db.query(Contact).filter(Contact.user_id == user_id)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Contact.name.ilike(search_pattern),
                    Contact.current_company.ilike(search_pattern),
                    Contact.current_position.ilike(search_pattern)
                )
            )

        total = query.count()
        contacts = query.order_by(Contact.last_meeting_date.desc().nullslast()) \
                       .offset(skip).limit(limit).all()

        return contacts, total

    @staticmethod
    def update_contact(
        db: Session,
        contact_id: int,
        user_id: int,
        contact_update: ContactUpdate
    ) -> Optional[Contact]:
        """Update a contact."""
        db_contact = ContactService.get_contact(db, contact_id, user_id)
        if not db_contact:
            return None

        update_data = contact_update.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(db_contact, field, value)

        db.commit()
        db.refresh(db_contact)
        return db_contact

    @staticmethod
    def delete_contact(db: Session, contact_id: int, user_id: int) -> bool:
        """Delete a contact."""
        db_contact = ContactService.get_contact(db, contact_id, user_id)
        if not db_contact:
            return False

        db.delete(db_contact)
        db.commit()
        return True

    @staticmethod
    def find_or_create_contact_by_name(
        db: Session,
        user_id: int,
        name: Optional[str]
    ) -> Optional[Contact]:
        """Find an existing contact by name or create a new one."""
        if not name:
            return None

        # Try to find exact match first
        contact = db.query(Contact).filter(
            Contact.user_id == user_id,
            Contact.name == name
        ).first()

        if not contact:
            # Try partial match
            contact = db.query(Contact).filter(
                Contact.user_id == user_id,
                Contact.name.ilike(f"%{name}%")
            ).first()

        if not contact:
            # Create new contact
            contact = Contact(user_id=user_id, name=name)
            db.add(contact)
            db.commit()
            db.refresh(contact)

        return contact

    @staticmethod
    def get_contact_with_timeline(db: Session, contact_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get contact with full timeline and action playbook.

        Returns:
            Dictionary with contact, meetings, and action_playbook
        """
        contact = ContactService.get_contact(db, contact_id, user_id)
        if not contact:
            return None

        # Get meetings ordered by date (newest first)
        meetings = db.query(Meeting).filter(
            Meeting.contact_id == contact_id,
            Meeting.status == "completed"
        ).order_by(Meeting.meeting_date.desc()).all()

        # Get action playbook
        playbook = db.query(ActionPlaybook).filter(
            ActionPlaybook.contact_id == contact_id
        ).first()

        return {
            "contact": contact,
            "meetings": meetings,
            "action_playbook": playbook
        }

    @staticmethod
    def export_contact_markdown(db: Session, contact_id: int, user_id: int) -> Optional[str]:
        """
        Export contact data as formatted markdown.

        Returns:
            Markdown string or None if contact not found
        """
        data = ContactService.get_contact_with_timeline(db, contact_id, user_id)
        if not data:
            return None

        contact = data["contact"]
        meetings = data["meetings"]
        playbook = data["action_playbook"]

        md_lines = []

        # Title
        md_lines.append(f"# {contact.name or '未命名联系人'}")
        md_lines.append("")

        # Identity Section
        md_lines.append("## 身份信息 (Identity)")
        md_lines.append("")

        if contact.nickname:
            md_lines.append(f"- **昵称**: {contact.nickname}")
        if contact.gender:
            md_lines.append(f"- **性别**: {contact.gender}")
        if contact.age_group:
            md_lines.append(f"- **年龄段**: {contact.age_group}")
        if contact.hometown:
            md_lines.append(f"- **家乡**: {contact.hometown}")
        if contact.city:
            md_lines.append(f"- **常驻城市**: {contact.city}")

        # Contact info
        contact_methods = []
        if contact.phone:
            contact_methods.append(f"电话: {contact.phone}")
        if contact.email:
            contact_methods.append(f"邮箱: {contact.email}")
        if contact.wechat:
            contact_methods.append(f"微信: {contact.wechat}")
        if contact.linkedin:
            contact_methods.append(f"LinkedIn: {contact.linkedin}")
        if contact_methods:
            md_lines.append("- **联系方式**")
            for cm in contact_methods:
                md_lines.append(f"  - {cm}")

        # Education
        if contact.education_school or contact.education_major or contact.education_degree:
            md_lines.append("- **教育背景**")
            if contact.education_school:
                md_lines.append(f"  - 学校: {contact.education_school}")
            if contact.education_major:
                md_lines.append(f"  - 专业: {contact.education_major}")
            if contact.education_degree:
                md_lines.append(f"  - 学位: {contact.education_degree}")

        # Career
        if contact.career_summary:
            md_lines.append(f"- **职业概述**: {contact.career_summary}")

        # Communication preferences
        if contact.preferred_contact_method or contact.preferred_contact_time or contact.communication_style:
            md_lines.append("- **沟通偏好**")
            if contact.preferred_contact_method:
                md_lines.append(f"  - 偏好方式: {contact.preferred_contact_method}")
            if contact.preferred_contact_time:
                md_lines.append(f"  - 偏好时间: {contact.preferred_contact_time}")
            if contact.communication_style:
                md_lines.append(f"  - 沟通风格: {contact.communication_style}")

        md_lines.append("")

        # Status Section
        md_lines.append("## 当前状态 (Status)")
        md_lines.append("")

        current_status = []
        if contact.current_company:
            current_status.append(f"公司: {contact.current_company}")
        if contact.current_position:
            current_status.append(f"职位: {contact.current_position}")
        if contact.current_industry:
            current_status.append(f"行业: {contact.current_industry}")
        if current_status:
            md_lines.append("### 当前工作")
            for item in current_status:
                md_lines.append(f"- {item}")

        if contact.focus_topics:
            md_lines.append("\n### 关注方向")
            for topic in contact.focus_topics:
                md_lines.append(f"- {topic}")

        if contact.current_projects:
            md_lines.append("\n### 当前项目")
            for project in contact.current_projects:
                md_lines.append(f"- {project}")

        if contact.short_term_goals or contact.long_term_goals:
            md_lines.append("\n### 目标")
            if contact.short_term_goals:
                md_lines.append("**短期目标**")
                for goal in contact.short_term_goals:
                    md_lines.append(f"- {goal}")
            if contact.long_term_goals:
                md_lines.append("**长期目标**")
                for goal in contact.long_term_goals:
                    md_lines.append(f"- {goal}")

        if contact.resource_needs or contact.resource_offers:
            md_lines.append("\n### 资源位")
            if contact.resource_needs:
                md_lines.append("**需要**")
                for need in contact.resource_needs:
                    md_lines.append(f"- {need}")
            if contact.resource_offers:
                md_lines.append("**可提供**")
                for offer in contact.resource_offers:
                    md_lines.append(f"- {offer}")

        md_lines.append("")

        # Timeline Section
        md_lines.append("## 互动历史 (Timeline)")
        md_lines.append("")

        if meetings:
            for meeting in meetings:
                md_lines.append(f"### {meeting.meeting_date.strftime('%Y-%m-%d')}")
                if meeting.location:
                    md_lines.append(f"**地点**: {meeting.location}")
                if meeting.scenario:
                    md_lines.append(f"**场景**: {meeting.scenario}")

                if meeting.topics:
                    md_lines.append("\n**讨论主题**:")
                    for topic in meeting.topics:
                        md_lines.append(f"- {topic}")

                if meeting.key_facts:
                    md_lines.append("\n**关键事实**:")
                    for fact in meeting.key_facts:
                        if isinstance(fact, dict):
                            md_lines.append(f"- {fact.get('fact', fact)}")
                        else:
                            md_lines.append(f"- {fact}")

                if meeting.sentiment:
                    md_lines.append(f"\n**情绪**: {meeting.sentiment}")

                if meeting.my_commitments or meeting.their_commitments:
                    md_lines.append("\n**承诺与待办**:")
                    if meeting.my_commitments:
                        md_lines.append("我的承诺:")
                        for c in meeting.my_commitments:
                            if isinstance(c, dict):
                                md_lines.append(f"- {c.get('commitment', c)}")
                            else:
                                md_lines.append(f"- {c}")
                    if meeting.their_commitments:
                        md_lines.append("对方承诺:")
                        for c in meeting.their_commitments:
                            if isinstance(c, dict):
                                md_lines.append(f"- {c.get('commitment', c)}")
                            else:
                                md_lines.append(f"- {c}")

                if meeting.open_loops or meeting.next_conversation_hooks:
                    md_lines.append("\n**续聊线索**:")
                    for loop in (meeting.open_loops or []):
                        md_lines.append(f"- 未完话题: {loop}")
                    for hook in (meeting.next_conversation_hooks or []):
                        md_lines.append(f"- 下次可聊: {hook}")

                md_lines.append("")
        else:
            md_lines.append("*暂无会谈记录*")
            md_lines.append("")

        # Action Playbook Section
        md_lines.append("## 行动剧本 (Action Playbook)")
        md_lines.append("")

        if playbook:
            # Gift & Care
            if playbook.preferences or playbook.taboos:
                md_lines.append("### 送礼与关怀 (Gift & Care)")
                if playbook.preferences:
                    md_lines.append("**偏好**:")
                    for pref in playbook.preferences:
                        md_lines.append(f"- {pref}")
                if playbook.taboos:
                    md_lines.append("**禁忌**:")
                    for taboo in playbook.taboos:
                        md_lines.append(f"- {taboo}")
                md_lines.append("")

            # Conversation Hooks
            if playbook.top_topics or playbook.conversation_questions:
                md_lines.append("### 续聊钩子 (Conversation Hooks)")
                if playbook.top_topics:
                    md_lines.append("**最投入话题**:")
                    for topic in playbook.top_topics:
                        md_lines.append(f"- {topic}")
                if playbook.conversation_questions:
                    md_lines.append("**下次可问**:")
                    for q in playbook.conversation_questions:
                        md_lines.append(f"- {q}")
                md_lines.append("")

            # Collaboration Map
            if playbook.how_i_can_help_them or playbook.how_they_can_help_me:
                md_lines.append("### 合作地图 (Collaboration Map)")
                if playbook.how_i_can_help_them:
                    md_lines.append("**我如何帮他**:")
                    for item in playbook.how_i_can_help_them:
                        md_lines.append(f"- {item}")
                if playbook.how_they_can_help_me:
                    md_lines.append("**他如何帮我**:")
                    for item in playbook.how_they_can_help_me:
                        md_lines.append(f"- {item}")
                md_lines.append("")

            # Relationship Health
            md_lines.append("### 关系健康 (Relationship Health)")
            if playbook.relationship_stage:
                md_lines.append(f"- **关系阶段**: {playbook.relationship_stage}")
            if playbook.temperature_score is not None:
                md_lines.append(f"- **温度分**: {playbook.temperature_score}/100")
            if playbook.next_action:
                na = playbook.next_action
                if isinstance(na, dict):
                    md_lines.append(f"- **建议动作**: {na.get('action', 'N/A')}")
                else:
                    md_lines.append(f"- **建议动作**: {na}")
            md_lines.append("")
        else:
            md_lines.append("*暂无行动建议*")
            md_lines.append("")

        # Footer
        md_lines.append("---")
        md_lines.append(f"*导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

        return "\n".join(md_lines)


class MeetingService:
    """Service for meeting-related operations."""

    @staticmethod
    async def create_meeting_from_text(
        db: Session,
        user_id: int,
        meeting_data: MeetingCreate
    ) -> Meeting:
        """
        Create a meeting from conversation text using LLM extraction.

        Args:
            db: Database session
            user_id: User ID
            meeting_data: Meeting creation data with raw text

        Returns:
            Created meeting with extracted information
        """
        # Find or create contact
        contact = ContactService.find_or_create_contact_by_name(
            db, user_id, meeting_data.contact_name
        )

        if not contact:
            # Create unnamed contact
            contact = Contact(user_id=user_id, name="未命名联系人")
            db.add(contact)
            db.commit()
            db.refresh(contact)

        # Create meeting with processing status
        db_meeting = Meeting(
            user_id=user_id,
            contact_id=contact.id,
            raw_text=meeting_data.raw_text,
            meeting_date=meeting_data.meeting_date or datetime.now(),
            location=meeting_data.location,
            scenario=meeting_data.scenario,
            status="processing"
        )
        db.add(db_meeting)
        db.commit()
        db.refresh(db_meeting)

        # Process with LLM
        try:
            extracted = llm_service.extract_contact_info(
                meeting_data.raw_text,
                meeting_data.contact_name
            )

            # Update contact with extracted information
            contact_data = extracted.get("contact", {})
            for key, value in contact_data.items():
                if value is not None and value != "" and value != []:
                    setattr(contact, key, value)

            # Update meeting with extracted information
            meeting_extracted = extracted.get("meeting", {})
            db_meeting.topics = meeting_extracted.get("topics")
            db_meeting.key_facts = meeting_extracted.get("key_facts")
            db_meeting.sentiment = meeting_extracted.get("sentiment")
            db_meeting.my_commitments = meeting_extracted.get("my_commitments")
            db_meeting.their_commitments = meeting_extracted.get("their_commitments")
            db_meeting.open_loops = meeting_extracted.get("open_loops")
            db_meeting.next_conversation_hooks = meeting_extracted.get("next_conversation_hooks")

            # Update contact last meeting date
            contact.last_meeting_date = db_meeting.meeting_date
            contact.last_verified_at = datetime.now()

            db_meeting.status = "completed"

            # Get or create action playbook
            playbook_data = extracted.get("action_playbook", {})
            playbook = db.query(ActionPlaybook).filter(
                ActionPlaybook.contact_id == contact.id
            ).first()

            if playbook:
                # Update existing playbook
                for section in ["preferences", "taboos", "gift_occasions", "gift_recommendations"]:
                    if section in playbook_data.get("gift_care", {}):
                        current = getattr(playbook, section, None) or []
                        new_val = playbook_data["gift_care"][section]
                        if isinstance(new_val, list):
                            merged = list(set((current or []) + new_val))
                            setattr(playbook, section, merged)

                if "conversation_hooks" in playbook_data:
                    ch = playbook_data["conversation_hooks"]
                    if ch.get("top_topics"):
                        current = playbook.top_topics or []
                        merged = list(set(current + ch["top_topics"]))
                        playbook.top_topics = merged
                    if ch.get("conversation_questions"):
                        current = playbook.conversation_questions or []
                        merged = list(set(current + ch["conversation_questions"]))
                        playbook.conversation_questions = merged

                if "collaboration_map" in playbook_data:
                    cm = playbook_data["collaboration_map"]
                    if cm.get("how_i_can_help_them"):
                        current = playbook.how_i_can_help_them or []
                        merged = list(set(current + cm["how_i_can_help_them"]))
                        playbook.how_i_can_help_them = merged
                    if cm.get("how_they_can_help_me"):
                        current = playbook.how_they_can_help_me or []
                        merged = list(set(current + cm["how_they_can_help_me"]))
                        playbook.how_they_can_help_me = merged

                if "relationship_health" in playbook_data:
                    rh = playbook_data["relationship_health"]
                    if rh.get("relationship_stage"):
                        playbook.relationship_stage = rh["relationship_stage"]
                    if rh.get("temperature_score") is not None:
                        playbook.temperature_score = rh["temperature_score"]
                    if rh.get("next_action"):
                        playbook.next_action = rh["next_action"]
            else:
                # Create new playbook
                playbook = ActionPlaybook(contact_id=contact.id)
                gc = playbook_data.get("gift_care", {})
                playbook.preferences = gc.get("preferences")
                playbook.taboos = gc.get("taboos")
                playbook.gift_occasions = gc.get("gift_occasions")
                playbook.gift_recommendations = gc.get("gift_recommendations")

                ch = playbook_data.get("conversation_hooks", {})
                playbook.top_topics = ch.get("top_topics")
                playbook.open_loops = ch.get("open_loops")
                playbook.conversation_questions = ch.get("conversation_questions")
                playbook.conversation_avoid = ch.get("conversation_avoid")

                cm = playbook_data.get("collaboration_map", {})
                playbook.how_i_can_help_them = cm.get("how_i_can_help_them")
                playbook.how_they_can_help_me = cm.get("how_they_can_help_me")
                playbook.exchange_boundaries = cm.get("exchange_boundaries")
                playbook.contact_rhythm = cm.get("contact_rhythm")

                rh = playbook_data.get("relationship_health", {})
                playbook.relationship_stage = rh.get("relationship_stage")
                playbook.temperature_score = rh.get("temperature_score")
                playbook.recent_risks = rh.get("recent_risks")
                playbook.next_action = rh.get("next_action")

                db.add(playbook)

            db.commit()
            db.refresh(db_meeting)

        except Exception as e:
            db_meeting.status = "failed"
            db_meeting.error_message = str(e)
            db.commit()
            db.refresh(db_meeting)

        return db_meeting

    @staticmethod
    def get_meeting(db: Session, meeting_id: int, user_id: int) -> Optional[Meeting]:
        """Get a meeting by ID for a specific user."""
        return db.query(Meeting).filter(
            Meeting.id == meeting_id,
            Meeting.user_id == user_id
        ).first()

    @staticmethod
    def list_meetings(
        db: Session,
        user_id: int,
        contact_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Meeting], int]:
        """
        List meetings for a user with optional contact filter.

        Returns:
            Tuple of (meetings list, total count)
        """
        query = db.query(Meeting).filter(Meeting.user_id == user_id)

        if contact_id:
            query = query.filter(Meeting.contact_id == contact_id)

        total = query.count()
        meetings = query.order_by(Meeting.meeting_date.desc()) \
                        .offset(skip).limit(limit).all()

        return meetings, total


contact_service = ContactService()
meeting_service = MeetingService()
