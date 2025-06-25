"""tie prediction → patient

Revision ID: df868509ff1b
Revises: 4e9d859ce8f1
Create Date: 2025-06-25 11:45:20.842515
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'df868509ff1b'
down_revision = '4e9d859ce8f1'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # use batch_alter_table so SQLite will actually rebuild the table
    with op.batch_alter_table("prediction", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("patient_id", sa.Integer(), nullable=False)
        )
        batch_op.create_foreign_key(
            "fk_prediction_patient",
            "patient",
            ["patient_id"],
            ["id"],
        )

def downgrade() -> None:
    with op.batch_alter_table("prediction", schema=None) as batch_op:
        batch_op.drop_constraint("fk_prediction_patient", type_="foreignkey")
        batch_op.drop_column("patient_id")

