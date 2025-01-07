"""rename metadata column to chunk_metadata

Revision ID: 002
Revises: 001
Create Date: 2024-03-14
"""

from alembic import op

# revision identifiers
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename the column from metadata to chunk_metadata
    op.alter_column(
        table_name="document_chunks",
        column_name="metadata",
        new_column_name="chunk_metadata",
    )


def downgrade() -> None:
    # Rename back if needed
    op.alter_column(
        table_name="document_chunks",
        column_name="chunk_metadata",
        new_column_name="metadata",
    )
