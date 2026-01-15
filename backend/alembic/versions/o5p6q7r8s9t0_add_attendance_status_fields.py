"""add_attendance_status_fields

Revision ID: o5p6q7r8s9t0
Revises: n4o5p6q7r8s9
Create Date: 2026-01-15 19:37:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'o5p6q7r8s9t0'
down_revision = 'n4o5p6q7r8s9'
branch_labels = None
depends_on = None


def upgrade():
    # Add state lifecycle fields to attendance table
    op.add_column('attendance', sa.Column('record_status', sa.String(length=20), server_default='draft', nullable=True))
    op.add_column('attendance', sa.Column('submitted_by', sa.String(length=36), nullable=True))
    op.add_column('attendance', sa.Column('submitted_at', sa.DateTime(), nullable=True))
    op.add_column('attendance', sa.Column('locked_by', sa.String(length=36), nullable=True))
    op.add_column('attendance', sa.Column('locked_at', sa.DateTime(), nullable=True))
    op.add_column('attendance', sa.Column('unlock_reason', sa.Text(), nullable=True))
    
    # Add foreign key constraints
    op.create_foreign_key('fk_attendance_submitted_by', 'attendance', 'users', ['submitted_by'], ['id'])
    op.create_foreign_key('fk_attendance_locked_by', 'attendance', 'users', ['locked_by'], ['id'])
    
    # Update existing records to 'draft' status (they will use the server_default)
    # No need to explicitly update since server_default handles it


def downgrade():
    # Remove foreign key constraints
    op.drop_constraint('fk_attendance_locked_by', 'attendance', type_='foreignkey')
    op.drop_constraint('fk_attendance_submitted_by', 'attendance', type_='foreignkey')
    
    # Drop columns
    op.drop_column('attendance', 'unlock_reason')
    op.drop_column('attendance', 'locked_at')
    op.drop_column('attendance', 'locked_by')
    op.drop_column('attendance', 'submitted_at')
    op.drop_column('attendance', 'submitted_by')
    op.drop_column('attendance', 'record_status')
