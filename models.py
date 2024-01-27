from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class DKR(Base):
    __tablename__ = 'dkr_table'

    OBJECTID: Mapped[int] = mapped_column(primary_key=True)
    Shape: Mapped[bytes]
    LandType: Mapped[int]
    LandCode: Mapped[int]
    UserName: Mapped[str]
    Ball_PlPoch: Mapped[float] = mapped_column(nullable=True)
    NDohod_d: Mapped[float] = mapped_column(nullable=True)
    SOATO: Mapped[int]
    Area_ga: Mapped[float]
    MelioCode: Mapped[int]
    Forma22: Mapped[str]
    Oblast: Mapped[str]
    Rayon: Mapped[str]
    R_zem: Mapped[int]
    Data_Vvoda: Mapped[datetime]
    SVovlech: Mapped[int]
    Note_: Mapped[str] = mapped_column(nullable=True)
    Shape_Length: Mapped[float]
    Shape_Area: Mapped[float]
