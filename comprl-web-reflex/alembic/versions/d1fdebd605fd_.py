"""empty message

Revision ID: d1fdebd605fd
Revises: 
Create Date: 2024-12-16 13:34:49.285363

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "d1fdebd605fd"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "localauthsession",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.String(length=255), nullable=False),
        sa.Column(
            "expiration",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("localauthsession", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_localauthsession_session_id"), ["session_id"], unique=True
        )
        batch_op.create_index(
            batch_op.f("ix_localauthsession_user_id"), ["user_id"], unique=False
        )

    op.create_table(
        "localuser",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.LargeBinary(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("localuser", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_localuser_username"), ["username"], unique=True
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("localuser", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_localuser_username"))

    op.drop_table("localuser")
    with op.batch_alter_table("localauthsession", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_localauthsession_user_id"))
        batch_op.drop_index(batch_op.f("ix_localauthsession_session_id"))

    op.drop_table("localauthsession")
    # ### end Alembic commands ###
