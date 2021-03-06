"""empty message

Revision ID: c53c4c342521
Revises: 
Create Date: 2018-09-22 17:46:18.605964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c53c4c342521'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('expenses_tracker_account',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('password', sa.String(length=128, collation='latin1_swedish_ci'), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('username', sa.String(length=150), nullable=True),
    sa.Column('first_name', sa.String(length=30, collation='latin1_swedish_ci'), nullable=True),
    sa.Column('last_name', sa.String(length=30, collation='latin1_swedish_ci'), nullable=True),
    sa.Column('email', sa.String(length=254, collation='latin1_swedish_ci'), nullable=True),
    sa.Column('is_staff', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('date_joined', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expenses_tracker_category',
    sa.Column('CategoryId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('CategoryName', sa.String(length=100), nullable=True),
    sa.Column('CreatedAt', sa.DateTime(), nullable=True),
    sa.Column('IsDeleted', sa.Boolean(), nullable=True),
    sa.Column('UserId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['UserId'], ['expenses_tracker_account.id'], ),
    sa.PrimaryKeyConstraint('CategoryId')
    )
    op.create_table('expenses_tracker_currency',
    sa.Column('CurrencyId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('CreatedAt', sa.DateTime(), nullable=True),
    sa.Column('CurrencyName', sa.String(length=100), nullable=True),
    sa.Column('CurrencySlug', sa.String(length=100), nullable=True),
    sa.Column('IsDeleted', sa.Boolean(), nullable=True),
    sa.Column('UserId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['UserId'], ['expenses_tracker_account.id'], ),
    sa.PrimaryKeyConstraint('CurrencyId')
    )
    op.create_table('expenses_tracker_token',
    sa.Column('Id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Token', sa.String(length=100), nullable=True),
    sa.Column('UserId', sa.Integer(), nullable=True),
    sa.Column('CreationDate', sa.DateTime(), nullable=True),
    sa.Column('TimeToLive', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['UserId'], ['expenses_tracker_account.id'], ),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('expenses_tracker_record',
    sa.Column('ExpensesId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('PaymentDate', sa.Date(), nullable=True),
    sa.Column('PaymentReason', sa.String(length=300), nullable=True),
    sa.Column('PaymentValue', sa.Integer(), nullable=True),
    sa.Column('PaymentCurrency_id', sa.Integer(), nullable=False),
    sa.Column('CategoryId_Id', sa.Integer(), nullable=False),
    sa.Column('UserId_Id', sa.Integer(), nullable=False),
    sa.Column('CreatedAt', sa.DateTime(), nullable=True),
    sa.Column('IsDeleted', sa.Boolean(), nullable=True),
    sa.Column('IsIncome', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['CategoryId_Id'], ['expenses_tracker_category.CategoryId'], ),
    sa.ForeignKeyConstraint(['PaymentCurrency_id'], ['expenses_tracker_currency.CurrencyId'], ),
    sa.ForeignKeyConstraint(['UserId_Id'], ['expenses_tracker_account.id'], ),
    sa.PrimaryKeyConstraint('ExpensesId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('expenses_tracker_record')
    op.drop_table('expenses_tracker_token')
    op.drop_table('expenses_tracker_currency')
    op.drop_table('expenses_tracker_category')
    op.drop_table('expenses_tracker_account')
    # ### end Alembic commands ###
