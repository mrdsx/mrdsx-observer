from sqlalchemy import Integer, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from src.utils.db import serialize_rows


class Base(DeclarativeBase):
    pass


class DB_User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]


def test_serialize_rows():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all(
            [
                DB_User(name="Leonardo"),
                DB_User(name="Donatello"),
                DB_User(name="Michelangelo"),
                DB_User(name="Raphael"),
            ]
        )
        session.commit()

        result = session.execute(select(DB_User))
        serialized = serialize_rows(result)

        assert serialized == [
            {"id": 1, "name": "Leonardo"},
            {"id": 2, "name": "Donatello"},
            {"id": 3, "name": "Michelangelo"},
            {"id": 4, "name": "Raphael"},
        ]

    Base.metadata.drop_all(engine)
