"""creating tables

Revision ID: 772b465a1ad6
Revises: 
Create Date: 2023-09-21 11:21:37.788051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '772b465a1ad6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('loan_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('STUDENT_LOAN', 'AUTO_LOAN', 'MORTGAGE_LOAN', name='loanproducttype'), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('loan_amount', sa.ARRAY(sa.Integer()), nullable=False),
    sa.Column('loan_term', sa.ARRAY(sa.Integer()), nullable=False),
    sa.Column('apr', sa.DECIMAL(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('loans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('fk_loans_loan_products', sa.Integer(), nullable=False),
    sa.Column('loan_contract_number', sa.String(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('currency', sa.Enum('USD', 'EUR', name='loancurrency'), nullable=False),
    sa.Column('stage', sa.Enum('LOAN_VERIFICATION', 'LOAN_PROCESSING', 'UNDERWRITING', 'CLOSURE', 'NONE', name='loanstage'), nullable=True),
    sa.Column('loan_term', sa.Interval(), nullable=False),
    sa.Column('loan_status', sa.Enum('ACTIVE', 'PAID_OFF', 'DEBT', 'APPROVED', 'IN_REVIEW', 'IN_PROGRESS', 'DRAFT', name='loanstatus'), nullable=False),
    sa.Column('loan_guarantors', sa.String(), nullable=True),
    sa.Column('application_date', sa.Date(), nullable=False),
    sa.Column('updated_at', sa.Date(), nullable=True),
    sa.Column('last_payment_date', sa.Date(), nullable=True),
    sa.Column('apr', sa.DECIMAL(), nullable=False),
    sa.Column('paid_amount', sa.DECIMAL(), nullable=True),
    sa.ForeignKeyConstraint(['fk_loans_loan_products'], ['loan_products.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('loan_contract_number')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('loans')
    op.drop_table('loan_products')
    # ### end Alembic commands ###
