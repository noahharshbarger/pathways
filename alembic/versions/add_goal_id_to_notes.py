"""add goal_id to notes

Revision ID: add_goal_id_to_notes
Revises: c3fda48595a3
Create Date: 2025-09-18 16:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'add_goal_id_to_notes'
down_revision: Union[str, Sequence[str], None] = 'c3fda48595a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('notes', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_notes_goal_id',
        'notes',
        'goals',
        ['goal_id'],
        ['id']
    )


def downgrade() -> None:
    op.drop_constraint('fk_notes_goal_id', 'notes', type_='foreignkey')
    op.drop_column('notes', 'goal_id')
