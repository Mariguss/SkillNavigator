"""fix_composite_pks_to_id

Revision ID: 068b623cbca7
Revises: 6e969ac19376
Create Date: 2026-06-07 21:10:33.023848

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '068b623cbca7'
down_revision: Union[str, Sequence[str], None] = '6e969ac19376'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema via explicit table recreation for SQLite."""
    # --- 1. ИСПРАВЛЯЕМ USER_SKILLS (Переносим PK на колонку id) ---
    op.create_table(
        '_user_skills_new',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.UniqueConstraint('user_id', 'skill_id', name='uq_user_skill')
    )
    # Копируем данные (id сгенерируются автоматически, старые ключи сбросятся)
    op.execute("INSERT INTO _user_skills_new (user_id, skill_id) SELECT user_id, skill_id FROM user_skills")
    op.drop_table('user_skills')
    op.rename_table('_user_skills_new', 'user_skills')

    # --- 2. ИСПРАВЛЯЕМ VACANCY_SKILLS (Переносим PK на колонку id) ---
    op.create_table(
        '_vacancy_skills_new',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('vacancy_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.UniqueConstraint('vacancy_id', 'skill_id', name='uq_vacancy_skill')
    )
    # Копируем данные
    op.execute("INSERT INTO _vacancy_skills_new (vacancy_id, skill_id) SELECT vacancy_id, skill_id FROM vacancy_skills")
    op.drop_table('vacancy_skills')
    op.rename_table('_vacancy_skills_new', 'vacancy_skills')


def downgrade() -> None:
    """Downgrade schema."""
    pass
