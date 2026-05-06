"""Create initial Ebook2LateX tables.

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-05-07
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

# revision identifiers, used by Alembic.
revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False, unique=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=False, server_default=sa.text("'Editor'")),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "documents",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True),
        sa.Column("file_name", sa.Text(), nullable=False),
        sa.Column("file_path_url", sa.Text(), nullable=False),
        sa.Column("upload_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("status", sa.String(length=50), nullable=False, server_default=sa.text("'Pending'")),
        sa.Column("latex_content", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "formula_entries",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("document_id", UUID(as_uuid=True), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("raw_image_path", sa.Text(), nullable=True),
        sa.Column("latex_content", sa.Text(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION set_updated_at()
        RETURNS trigger AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )

    op.execute(
        """
        CREATE TRIGGER trg_formula_entries_updated_at
        BEFORE UPDATE ON formula_entries
        FOR EACH ROW
        EXECUTE PROCEDURE set_updated_at();
        """
    )

    op.create_table(
        "logs",
        sa.Column("log_id", UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("formula_id", UUID(as_uuid=True), sa.ForeignKey("formula_entries.id", ondelete="CASCADE"), nullable=True),
        sa.Column("processing_time_ms", sa.Integer(), nullable=True),
        sa.Column("confidence_score", sa.Numeric(3, 2), nullable=True),
        sa.Column("error_type", sa.String(length=100), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("environment_info", JSONB, nullable=True),
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_formula_entries_updated_at ON formula_entries;")
    op.execute("DROP FUNCTION IF EXISTS set_updated_at();")
    op.drop_table("logs")
    op.drop_table("formula_entries")
    op.drop_table("documents")
    op.drop_table("users")
