"""Align the initial schema with the current SQLAlchemy models.

Revision ID: b1c2d3e4f5a6
Revises: a0f6469f1e76
Create Date: 2026-08-04
"""

from alembic import op
import sqlalchemy as sa


revision = 'b1c2d3e4f5a6'
down_revision = 'a0f6469f1e76'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP"))
        )

    with op.batch_alter_table('password_reset_tokens', schema=None) as batch_op:
        batch_op.drop_column('is_used')
        batch_op.alter_column('expirats_at', new_column_name='expires_at', existing_type=sa.DateTime())

    op.create_table(
        'token_blocklist',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('jti', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    with op.batch_alter_table('token_blocklist', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_token_blocklist_jti'), ['jti'], unique=False)


def downgrade():
    with op.batch_alter_table('token_blocklist', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_token_blocklist_jti'))
    op.drop_table('token_blocklist')

    with op.batch_alter_table('password_reset_tokens', schema=None) as batch_op:
        batch_op.alter_column('expires_at', new_column_name='expirats_at', existing_type=sa.DateTime())
        batch_op.add_column(sa.Column('is_used', sa.Boolean(), nullable=False, server_default=sa.false()))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('created_at')
