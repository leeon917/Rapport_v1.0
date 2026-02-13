"""Initial migration

Revision ID: 001
Revises:
Create Date: 2025-01-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_email', 'users', ['email'])

    # Create contacts table
    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('nickname', sa.String(length=100), nullable=True),
        sa.Column('gender', sa.String(length=20), nullable=True),
        sa.Column('age_group', sa.String(length=50), nullable=True),
        sa.Column('hometown', sa.String(length=100), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('wechat', sa.String(length=100), nullable=True),
        sa.Column('linkedin', sa.String(length=255), nullable=True),
        sa.Column('education_school', sa.String(length=200), nullable=True),
        sa.Column('education_major', sa.String(length=200), nullable=True),
        sa.Column('education_degree', sa.String(length=50), nullable=True),
        sa.Column('career_summary', sa.Text(), nullable=True),
        sa.Column('preferred_contact_method', sa.String(length=50), nullable=True),
        sa.Column('preferred_contact_time', sa.String(length=100), nullable=True),
        sa.Column('communication_style', sa.String(length=100), nullable=True),
        sa.Column('current_company', sa.String(length=200), nullable=True),
        sa.Column('current_position', sa.String(length=200), nullable=True),
        sa.Column('current_industry', sa.String(length=100), nullable=True),
        sa.Column('current_location', sa.String(length=100), nullable=True),
        sa.Column('startup_status', sa.String(length=100), nullable=True),
        sa.Column('focus_topics', sa.JSON(), nullable=True),
        sa.Column('current_projects', sa.JSON(), nullable=True),
        sa.Column('short_term_goals', sa.JSON(), nullable=True),
        sa.Column('long_term_goals', sa.JSON(), nullable=True),
        sa.Column('resource_needs', sa.JSON(), nullable=True),
        sa.Column('resource_offers', sa.JSON(), nullable=True),
        sa.Column('excitement_points', sa.JSON(), nullable=True),
        sa.Column('anxiety_points', sa.JSON(), nullable=True),
        sa.Column('sensitive_points', sa.JSON(), nullable=True),
        sa.Column('last_meeting_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('relationship_stage', sa.String(length=50), nullable=True),
        sa.Column('temperature_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_contacts_id', 'contacts', ['id'])
    op.create_index('ix_contacts_name', 'contacts', ['name'])

    # Create meetings table
    op.create_table(
        'meetings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('contact_id', sa.Integer(), nullable=False),
        sa.Column('meeting_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('location', sa.String(length=200), nullable=True),
        sa.Column('scenario', sa.String(length=200), nullable=True),
        sa.Column('raw_text', sa.Text(), nullable=False),
        sa.Column('topics', sa.JSON(), nullable=True),
        sa.Column('key_facts', sa.JSON(), nullable=True),
        sa.Column('sentiment', sa.String(length=20), nullable=True),
        sa.Column('my_commitments', sa.JSON(), nullable=True),
        sa.Column('their_commitments', sa.JSON(), nullable=True),
        sa.Column('open_loops', sa.JSON(), nullable=True),
        sa.Column('next_conversation_hooks', sa.JSON(), nullable=True),
        sa.Column('status', sa.Enum('processing', 'completed', 'failed', name='meetingstatus'), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['contact_id'], ['contacts.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_meetings_id', 'meetings', ['id'])

    # Create action_playbooks table
    op.create_table(
        'action_playbooks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('contact_id', sa.Integer(), nullable=False),
        sa.Column('preferences', sa.JSON(), nullable=True),
        sa.Column('taboos', sa.JSON(), nullable=True),
        sa.Column('gift_occasions', sa.JSON(), nullable=True),
        sa.Column('gift_recommendations', sa.JSON(), nullable=True),
        sa.Column('top_topics', sa.JSON(), nullable=True),
        sa.Column('open_loops', sa.JSON(), nullable=True),
        sa.Column('conversation_questions', sa.JSON(), nullable=True),
        sa.Column('conversation_avoid', sa.JSON(), nullable=True),
        sa.Column('how_i_can_help_them', sa.JSON(), nullable=True),
        sa.Column('how_they_can_help_me', sa.JSON(), nullable=True),
        sa.Column('exchange_boundaries', sa.JSON(), nullable=True),
        sa.Column('contact_rhythm', sa.JSON(), nullable=True),
        sa.Column('relationship_stage', sa.String(length=50), nullable=True),
        sa.Column('temperature_score', sa.Float(), nullable=True),
        sa.Column('recent_risks', sa.JSON(), nullable=True),
        sa.Column('next_action', sa.JSON(), nullable=True),
        sa.Column('evidence_refs', sa.JSON(), nullable=True),
        sa.Column('last_updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['contact_id'], ['contacts.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('contact_id')
    )
    op.create_index('ix_action_playbooks_id', 'action_playbooks', ['id'])


def downgrade() -> None:
    op.drop_index('ix_action_playbooks_id', table_name='action_playbooks')
    op.drop_table('action_playbooks')
    op.drop_index('ix_meetings_id', table_name='meetings')
    op.drop_table('meetings')
    op.drop_index('ix_contacts_name', table_name='contacts')
    op.drop_index('ix_contacts_id', table_name='contacts')
    op.drop_table('contacts')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
