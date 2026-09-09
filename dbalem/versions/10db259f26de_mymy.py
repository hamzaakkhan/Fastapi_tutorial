"""mymy

Revision ID: 10db259f26de
Revises: 963c2a0dd434
Create Date: 2026-09-04 18:52:43.965674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10db259f26de'
down_revision: Union[str, Sequence[str], None] = '963c2a0dd434'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts" , sa.Column("content",
                                    sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
