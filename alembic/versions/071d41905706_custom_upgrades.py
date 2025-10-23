"""custom upgrades

Revision ID: 071d41905706
Revises: d59bb5449cfa
Create Date: 2025-10-22 17:41:22.225028

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import Date, func
from sqlalchemy.sql import column, table

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '071d41905706'
down_revision: Union[str, Sequence[str], None] = 'd59bb5449cfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    policy_table = table(
        'policies',
        column('id', sa.Integer),
        column('start_date', Date),
        column('end_date', Date)
    )
    op.execute(
        policy_table.update()
        .where(policy_table.c.end_date == None)
        .values(end_date=func.date(policy_table.c.start_date, '+1 year'))
    )

    with op.batch_alter_table('policies') as batch_op:
        batch_op.alter_column('end_date', nullable=False)

    op.create_index('ix_cars_vin', 'cars', ['vin'], unique=True)
    op.create_index('ix_policies_car_id_start_end', 'policies', ['car_id', 'start_date', 'end_date'])
    op.create_index('ix_claims_car_id_claim_date', 'claims', ['car_id', 'claim_date'])

    op.execute(
        "CREATE INDEX ix_policies_active ON policies (car_id, start_date, end_date) WHERE end_date > start_date"
    )


def downgrade():
    op.drop_index('ix_cars_vin', table_name='cars')
    op.drop_index('ix_policies_car_id_start_end', table_name='policies')
    op.drop_index('ix_claims_car_id_claim_date', table_name='claims')
    op.execute("DROP INDEX IF EXISTS ix_policies_active")
    op.alter_column('policies', 'end_date', nullable=True)
