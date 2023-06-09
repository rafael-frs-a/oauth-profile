"""Create user models

Revision ID: e296be8fd619
Revises:
Create Date: 2023-03-12 14:56:42.256871

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'e296be8fd619'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'user',
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('compiled_profile', sqlalchemy_utils.types.json.JSONType(), nullable=False),
        sa.Column('profile_history', sqlalchemy_utils.types.json.JSONType(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_table(
        'auth0_credentials',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('access_token', sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('auth0_credentials')
    op.drop_table('user')
    # ### end Alembic commands ###
