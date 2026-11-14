
"""add users table and resume relationship

Revision ID: 15eb34b0ece9
Revises: 470f13ea0347
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision: str = "15eb34b0ece9"
down_revision: Union[str, Sequence[str], None] = "470f13ea0347"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )

    # Create unique index on email
    op.create_index(
        op.f("ix_users_email"),
        "users",
        ["email"],
        unique=True
    )

    # Add user_id column to resumes
    op.add_column(
        "resumes",
        sa.Column("user_id", sa.Integer(), nullable=False)
    )

    # Create named foreign key
    op.create_foreign_key(
        "fk_resumes_user_id_users",
        "resumes",
        "users",
        ["user_id"],
        ["id"]
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Drop the named foreign key
    op.drop_constraint(
        "fk_resumes_user_id_users",
        "resumes",
        type_="foreignkey"
    )

    # Remove user_id column
    op.drop_column("resumes", "user_id")

    # Remove email index
    op.drop_index(
        op.f("ix_users_email"),
        table_name="users"
    )

    # Drop users table
    op.drop_table("users")
