"""fix_vacancy_composite_pk

Revision ID: 230ccd353dd8
Revises: 1f08c4e9de47
Create Date: 2026-06-03 20:23:39.524780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '230ccd353dd8'
down_revision: Union[str, Sequence[str], None] = '1f08c4e9de47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Для SQlite

def upgrade() -> None:
    # Принудительно пересоздаем таблицу, чтобы обновить первичный ключ
    with op.batch_alter_table('vacancy', schema=None, recreate='always') as batch_op:
        # Просто создаем новый ключ на id, старый удалится автоматически при пересборке
        batch_op.create_primary_key('pk_vacancy', ['id'])


def downgrade() -> None:
    with op.batch_alter_table('vacancy', schema=None, recreate='always') as batch_op:
        batch_op.create_primary_key('pk_vacancy', ['id', 'company_id'])


# def upgrade() -> None:
#     """Upgrade schema."""
#     # 1. Удаляем старый составной первичный ключ
#     # Если имя старого ключа отличается, СУБД выдаст ошибку. Обычно имя 'vacancy_pkey'
#     op.drop_constraint('vacancy_pkey', 'vacancy', type_='primary')
    
#     # 2. Создаем новый первичный ключ только на поле id
#     op.create_primary_key('vacancy_pkey', 'vacancy', ['id'])


# def downgrade() -> None:
#     """Downgrade schema."""
#     # Откат изменений: возвращаем составной ключ обратно
#     op.drop_constraint('vacancy_pkey', 'vacancy', type_='primary')
#     op.create_primary_key('vacancy_pkey', 'vacancy', ['id', 'company_id'])
