import typing
import sqlalchemy as sa
from sqlalchemy_utils import JSONType, StringEncryptedType
from sqlmodel import SQLModel, Field, Relationship
from . import base


class User(base.TimestampModel, table=True):
    __tablename__ = 'user'

    id: typing.Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True)
    compiled_profile: dict[typing.Any, typing.Any] = Field(
        default={},
        sa_column=sa.Column(JSONType, nullable=False)
    )
    profile_history: list[typing.Any] = Field(
        default=[],
        sa_column=sa.Column(JSONType, nullable=False)
    )

    auth0_credentials: typing.Optional['Auth0Credentials'] = Relationship(
        sa_relationship_kwargs={
            'uselist': False,  # One-to-one relationship
            'cascade': 'all, delete',  # Instruct the ORM how to track changes to local objects
        },
        back_populates='user'
    )


class Auth0Credentials(SQLModel, table=True):
    __tablename__ = 'auth0_credentials'

    id: typing.Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            sa.ForeignKey('user.id', ondelete='CASCADE'),  # Set the foreign key behavior on the table metadata
            nullable=False,
            unique=True
        )
    )
    access_token: str = Field(
        sa_column=sa.Column(StringEncryptedType(sa.String, base.get_key), nullable=False)
    )

    user: User = Relationship(back_populates='auth0_credentials')
