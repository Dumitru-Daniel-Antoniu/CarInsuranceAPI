"""Initial migration

Revision ID: d59bb5449cfa
Revises: 
Create Date: 2025-10-22 16:48:07.339999

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd59bb5449cfa'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'owners',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(70), nullable=False),
        sa.Column('email', sa.String(50), nullable=True, unique=True),
    )

    op.create_table(
        'cars',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('vin', sa.String(50), nullable=False, unique=True),
        sa.Column('make', sa.String(30), nullable=True),
        sa.Column('model', sa.String(50), nullable=True),
        sa.Column('year_of_manufacture', sa.Integer, nullable=False),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('owners.id'), nullable=False),
    )

    op.create_table(
        'policies',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('provider', sa.String(100), nullable=True),
        sa.Column('start_date', sa.Date, nullable=False),
        sa.Column('end_date', sa.Date, nullable=False),
        sa.Column('logged_expiry_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('car_id', sa.Integer, sa.ForeignKey('cars.id'), nullable=False),
    )

    op.create_table(
        'claims',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('claim_date', sa.Date, nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('car_id', sa.Integer, sa.ForeignKey('cars.id'), nullable=False),
    )


def downgrade():
    op.drop_table('claims')
    op.drop_table('policies')
    op.drop_table('cars')
    op.drop_table('owners')
