import uuid

from sqlalchemy import Column, DateTime, Integer, LargeBinary, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, JSON


class Base(DeclarativeBase):
    pass


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    user_id = Column(String, nullable=True)
    session_id = Column(String, nullable=True)
    name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    status = Column(String, default="processing")
    target_column = Column(String, nullable=True)
    rows = Column(Integer, nullable=True)
    columns = Column(Integer, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


# model report

class Report(Base):
    __tablename__ = "reports"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    dataset_id = Column(
        String,
        ForeignKey("datasets.id"),
    )

    report_json = Column(JSON)

    score = Column(Integer)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class AnalysisPlot(Base):
    __tablename__ = "analysis_plots"
    __table_args__ = (
        UniqueConstraint("dataset_id", "plot_type", name="uq_analysis_plots_dataset_plot_type"),
    )

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    dataset_id = Column(
        String,
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False,
    )
    plot_type = Column(String, nullable=False)
    image_data = Column(LargeBinary, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
