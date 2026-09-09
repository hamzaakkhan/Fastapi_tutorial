"""user_table

Revision ID: acb5ea596359
Revises: 10db259f26de
Create Date: 2026-09-05 01:16:21.649152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acb5ea596359'
down_revision: Union[str, Sequence[str], None] = '10db259f26de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint("email")
                    )
    
    
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
