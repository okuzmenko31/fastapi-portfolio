import datetime
import uuid

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey, Text, DateTime

from src.settings.database import Base
from src.auth.models import User


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True),
                                           primary_key=True,
                                           default=uuid.uuid4)
    author_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey('users.id'))
    author = relationship('User', back_populates='posts')
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    short_description: Mapped[str] = mapped_column(String(10000),
                                                   nullable=True)
    preview: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                                          default=datetime.datetime.now)
    likes: Mapped[list['Like']] = relationship(back_populates='post')
    comments: Mapped[list['Comment']] = relationship(back_populates='post')
    category_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey('categories.id'))
    category: Mapped['PostCategory'] = relationship(back_populates='posts')

    def __repr__(self):
        return f'Post: {self.title}'


class PostCategory(Base):
    __tablename__ = 'categories'

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True),
                                           primary_key=True,
                                           default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150),
                                      nullable=False)
    posts: Mapped[list['Post']] = relationship(back_populates='category')

    def __repr__(self):
        return f'Category: {self.name}'


class Like(Base):
    __tablename__ = 'likes'

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True),
                                           primary_key=True,
                                           default=uuid.uuid4)
    user_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship()
    post_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey('posts.id'))
    post: Mapped['Post'] = relationship(back_populates='likes')

    def __str__(self):
        return f'Like from {self.user.username}. Post: {self.post.title}'


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True),
                                           primary_key=True,
                                           default=uuid.uuid4)
    parent_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey('comments.id'),
                                                  nullable=True)
    parent: Mapped['Comment'] = relationship(remote_side=id)
    author_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey('users.id'))
    author = relationship('User', back_populates='posts')
    post_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey('posts.id'))
    post: Mapped['Post'] = relationship(back_populates='likes')
    content: Mapped[str] = mapped_column(nullable=False)

    def __str__(self):
        return f'Comment from {self.user.username}. Post: {self.post.title}'
