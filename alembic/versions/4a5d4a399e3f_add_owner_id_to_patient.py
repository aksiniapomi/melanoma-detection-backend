"""Add owner_id to patient

Revision ID: 4a5d4a399e3f
Revises: df868509ff1b
Create Date: 2025-06-27 13:47:38.294334
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4a5d4a399e3f'
down_revision = 'df868509ff1b'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1) Add as nullable
    with op.batch_alter_table("patient") as batch_op:
        batch_op.add_column(sa.Column("owner_id", sa.Integer(), nullable=True))

    # 2) Backfill: assign all existing patients to a default user (e.g. user id=1)
    op.execute(
        "UPDATE patient "
        "SET owner_id = (SELECT id FROM user ORDER BY id LIMIT 1)"
    )

    # 3) make it non-nullable and add the FK
    with op.batch_alter_table("patient") as batch_op:
        batch_op.alter_column(
            "owner_id", existing_type=sa.Integer(), nullable=False
        )
        batch_op.create_foreign_key(
            "fk_patient_owner",  # give the constraint a name
            "user",              # referent table
            ["owner_id"],        # local cols
            ["id"],              # remote cols
        )

def downgrade() -> None:
    with op.batch_alter_table("patient") as batch_op:
        batch_op.drop_constraint("fk_patient_owner", type_="foreignkey")
        batch_op.drop_column("owner_id")
