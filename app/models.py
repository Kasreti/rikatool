import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, app
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

class Dictionary(db.Model):
    __tablename__ = 'Dictionary'
    id: Mapped[int] = mapped_column(primary_key=True)
    word: so.Mapped[str] = so.mapped_column(sa.String(50), index=True)
    defin: so.Mapped[str] = so.mapped_column(sa.String(255), index=True)
    anim: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)
    pos: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)
    etym: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=True)
    def __repr__(self):
        return '{} (class {}) {} with definition {}'.format(self.pos, self.anim, self.word, self.defin)

    def __init__(self, word, defin, anim, pos, etym):
        self.word = word
        self.defin = defin
        self.anim = anim
        self.pos = pos
        self.etym = etym

with app.app_context():
    db.create_all()