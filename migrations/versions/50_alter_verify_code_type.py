"""empty message

Revision ID: 50_alter_verify_code_type
Revises: 40_verify_codes
Create Date: 2015-12-11 10:21:24.098275

"""

# revision identifiers, used by Alembic.
revision = '50_alter_verify_code_type'
down_revision = '40_verify_codes'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('verify_codes', 'code_type',
               existing_type=postgresql.ENUM('email', 'sms', name='verify_code_types'),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('verify_codes', 'code_type',
               existing_type=postgresql.ENUM('email', 'sms', name='verify_code_types'),
               nullable=True)
    ### end Alembic commands ###
