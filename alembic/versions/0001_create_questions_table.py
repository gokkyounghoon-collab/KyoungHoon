"""create questions table

Revision ID: 0001_create_questions_table
Revises: 
Create Date: 2026-06-28 00:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_create_questions_table"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("subject", sa.String(), nullable=False),
        sa.Column("author", sa.String(), nullable=False),
        sa.Column("range", sa.String(), nullable=False),
        sa.Column("difficulty", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=True),
        sa.Column("answer_idx", sa.Integer(), nullable=False, default=0),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("question_type", sa.String(), nullable=False, default="multiple_choice"),
        sa.Column("short_answer", sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("questions")
