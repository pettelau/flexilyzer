from datetime import datetime
from sqlalchemy import (
    Boolean,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    JSON,
    Enum,
)
from sqlalchemy.orm import relationship
from db.database import Base
from schemas.shared import BatchEnum, ValueTypesInput, ValueTypesOutput

# Association table for the many-to-many relationship between Assignment and Analyzer
assignment_analyzer_association = Table(
    "assignment_analyzer",
    Base.metadata,
    Column(
        "assignment_id",
        Integer,
        ForeignKey("assignments.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "analyzer_id",
        Integer,
        ForeignKey("analyzers.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tag = Column(String, unique=True, index=True)
    name = Column(String, index=True, nullable=True)

    assignments = relationship("Assignment", back_populates="course")
    teams = relationship("Team", back_populates="course")


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    due_date = Column(DateTime, index=True, nullable=True)

    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    course = relationship("Course", back_populates="assignments")

    projects = relationship("Project", back_populates="assignment")

    analyzers = relationship(
        "Analyzer",
        secondary=assignment_analyzer_association,
        back_populates="assignments",
    )


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    course = relationship("Course", back_populates="teams")

    projects = relationship("Project", back_populates="team")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    assignment_id = Column(Integer, ForeignKey("assignments.id", ondelete="CASCADE"))
    assignment = relationship("Assignment", back_populates="projects")

    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    team = relationship("Team", back_populates="projects")

    reports = relationship("Report", back_populates="project")

    project_metadata = relationship("ProjectMetadata", back_populates="project")


class ProjectMetadata(Base):
    __tablename__ = "project_metadata"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value = Column(JSON, nullable=True)

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    project = relationship("Project", back_populates="project_metadata")
    assignment_metadata_id = Column(
        Integer, ForeignKey("assignment_metadata.id", ondelete="CASCADE")
    )


class Analyzer(Base):
    __tablename__ = "analyzers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    creator = Column(String, index=True, nullable=True)
    description = Column(String, index=True, nullable=True)
    has_script = Column(Boolean, index=True, default=False)
    has_requirements = Column(Boolean, index=True, default=False)

    analyzer_inputs = relationship("AnalyzerInput", back_populates="analyzer")
    analyzer_outputs = relationship("AnalyzerOutput", back_populates="analyzer")

    batches = relationship("Batch", back_populates="analyzer")

    assignments = relationship(
        "Assignment",
        secondary=assignment_analyzer_association,
        back_populates="analyzers",
    )


class AnalyzerInput(Base):
    __tablename__ = "analyzer_inputs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key_name = Column(String, index=True)
    value_type = Column(Enum(ValueTypesInput), index=True)

    analyzer_id = Column(Integer, ForeignKey("analyzers.id", ondelete="CASCADE"))
    analyzer = relationship("Analyzer", back_populates="analyzer_inputs")


class AnalyzerOutput(Base):
    __tablename__ = "analyzer_outputs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key_name = Column(String, index=True)
    value_type = Column(Enum(ValueTypesOutput), index=True)
    display_name = Column(String, index=True, nullable=True)
    extended_metadata = Column(JSON, nullable=True)

    analyzer_id = Column(Integer, ForeignKey("analyzers.id", ondelete="CASCADE"))
    analyzer = relationship("Analyzer", back_populates="analyzer_outputs")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    report = Column(JSON, nullable=True)

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    project = relationship("Project", back_populates="reports")

    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="CASCADE"))


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id", ondelete="CASCADE"))
    status = Column(Enum(BatchEnum), index=True, default=BatchEnum.STARTED)
    analyzer_id = Column(Integer, ForeignKey("analyzers.id", ondelete="CASCADE"))
    analyzer = relationship("Analyzer", back_populates="batches")


class AssignmentMetadata(Base):
    __tablename__ = "assignment_metadata"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_id = Column(
        Integer, ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False
    )
    key_name = Column(String, nullable=False)
    value_type = Column(String, nullable=False)
