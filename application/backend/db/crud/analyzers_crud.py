from typing import List
from sqlalchemy.orm import Session
from schemas.analyzer_schema import (
    AnalyzerBase,
    AnalyzerInputCreate,
    AnalyzerOutputCreate,
)
import json

from db.models import (
    Analyzer,
    AnalyzerInput,
    AnalyzerOutput,
    Assignment,
    assignment_analyzer_association,
)


class AnalyzerRepository:
    @staticmethod
    def get_analyzers(db: Session):
        """
        Retrieves all analyzers.

        Parameters:
        - db (Session): The database session.

        Returns:
        A list of all analyzers.
        """
        return db.query(Analyzer).all()

    @staticmethod
    def get_analyzer(db: Session, analyzer_id: int):
        """
        Retrieves a specific analyzer.

        Parameters:
        - db (Session): The database session.
        - analyzer_id (int): The ID of the analyzer.

        Returns:
        The requested analyzer if found, otherwise None.
        """
        return db.query(Analyzer).filter(Analyzer.id == analyzer_id).first()

    @staticmethod
    def get_analyzer_by_name(db: Session, analyzer_name: str):
        """
        Retrieves a specific analyzer by name.

        Parameters:
        - db (Session): The database session.
        - analyzer_name (str): The name of the analyzer.

        Returns:
        The requested analyzer if found, otherwise None.
        """
        return db.query(Analyzer).filter(Analyzer.name == analyzer_name).first()

    @staticmethod
    def get_analyzers_by_assignment_id(db: Session, assignment_id: int):
        """
        Retrieves all analyzers connected to a specific assignment.

        Parameters:
        - db (Session): The database session.
        - assignment_id (int): The ID of the assignment.

        Returns:
        A list of analyzers connected to the specified assignment.
        """
        return (
            db.query(Analyzer)
            .select_from(Analyzer)
            .join(
                assignment_analyzer_association,
                Analyzer.id == assignment_analyzer_association.c.analyzer_id,
            )
            .join(
                Assignment,
                Assignment.id == assignment_analyzer_association.c.assignment_id,
            )
            .filter(Assignment.id == assignment_id)
            .all()
        )

    @staticmethod
    def get_analyzer_inputs(db: Session, analyzer_id: int):
        """
        Retrieves a specific analyzer along with its inputs and outputs.

        Parameters:
        - db (Session): The database session.
        - analyzer_id (int): The ID of the analyzer.

        Returns:
        The requested analyzer inputs
        """
        return (
            db.query(AnalyzerInput)
            .filter(AnalyzerInput.analyzer_id == analyzer_id)
            .all()
        )

    @staticmethod
    def get_analyzer_outputs(db: Session, analyzer_id: int):
        """
        Retrieves a specific analyzer along with its inputs and outputs.

        Parameters:
        - db (Session): The database session.
        - analyzer_id (int): The ID of the analyzer.

        Returns:
        The requested analyzer outputs
        """
        return (
            db.query(AnalyzerOutput)
            .filter(AnalyzerOutput.analyzer_id == analyzer_id)
            .all()
        )

    @staticmethod
    def create_analyzer(db: Session, analyzer: AnalyzerBase):
        """
        Creates a new analyzer.

        Parameters:
        - db (Session): The database session.
        - name (str): The name of the analyzer.
        - creator (str, optional): The creator of the analyzer. Defaults to None.

        Returns:
        The created analyzer.
        """
        # Create a new Analyzer object

        new_analyzer = Analyzer(**analyzer.model_dump())
        db.add(new_analyzer)
        db.commit()
        db.refresh(new_analyzer)

        return new_analyzer

    @staticmethod
    def update_analyzer(db: Session, analyzer_id: int, analyzer: AnalyzerBase):
        """
        Update an existing Analyzer.

        Parameters:
        - db (Session): The database session.
        - analyzer_id (int): The analyzer ID.
        - analyzer (AnalyzerBase): The updated analyzer data.

        Returns:
        The updated analyzer.
        """
        db_analyzer = db.query(Analyzer).filter(Analyzer.id == analyzer_id).first()
        for key, value in analyzer.model_dump().items():
            setattr(db_analyzer, key, value)
        db.commit()
        db.refresh(db_analyzer)
        return db_analyzer

    @staticmethod
    def create_analyzer_inputs(
        db: Session, analyzer_id: int, inputs: List[AnalyzerInputCreate]
    ):
        """
        Creates analyzer inputs.

        Parameters:
        - db (Session): The database session.
        - analyzer_id (int): The ID of the analyzer to which the inputs belong.
        - inputs (List[AnalyzerInputCreate]): A list of inputs to be created.

        Returns:
        A list of created analyzer inputs.
        """

        for input_data in inputs:
            new_input = AnalyzerInput(
                analyzer_id=analyzer_id, **input_data.model_dump()
            )
            db.add(new_input)
        db.commit()
        return (
            db.query(AnalyzerInput)
            .filter(AnalyzerInput.analyzer_id == analyzer_id)
            .all()
        )

    @staticmethod
    def create_analyzer_outputs(
        db: Session, analyzer_id: int, outputs: List[AnalyzerOutputCreate]
    ):
        """
        Creates analyzer outputs.

        Parameters:
        - db (Session): The database session.
        - analyzer_id (int): The ID of the analyzer to which the outputs belong.
        - outputs (List[AnalyzerOutputCreate]): A list of outputs to be created.

        Returns:
        A list of created analyzer outputs.
        """

        for output_data in outputs:
            model = output_data.model_dump()
            new_output = AnalyzerOutput(
                analyzer_id=analyzer_id,
                extended_metadata=json.dumps(model["extended_metadata"]),
                value_type=model["value_type"],
                key_name=model["key_name"],
                display_name=model["display_name"],
            )
            db.add(new_output)
        db.commit()
        return (
            db.query(AnalyzerOutput)
            .filter(AnalyzerOutput.analyzer_id == analyzer_id)
            .all()
        )

    @staticmethod
    def update_analyzer(db: Session, analyzer_id: int, analyzer: AnalyzerBase):
        """
        Update an existing Analyzer.

        Parameters:
        - db (Session): The database session.
        - Analyzer_id (int): The Analyzer ID.
        - Analyzer (AnalyzerBase): The updated analyzer data.

        Returns:
        The updated Analyzer.
        """
        db_analyzer = db.query(Analyzer).filter(Analyzer.id == analyzer_id).first()
        for key, value in analyzer.model_dump().items():
            setattr(db_analyzer, key, value)
        db.commit()
        db.refresh(db_analyzer)
        return db_analyzer
