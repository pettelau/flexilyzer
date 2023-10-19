from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.models import (
    Course,
    Assignment,
    Team,
    Repository,
    Analyzer,
    MetricDefinition,
    Report,
)
import json
from .database import DATABASE_URL

# Create the engine and session. Replace the connection string with your database connection string.
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def main():
    session = SessionLocal()
    try:
        print("Cleaning DB ...")
        session.query(Course).delete()
        session.query(Assignment).delete()
        session.query(Team).delete()
        session.query(Repository).delete()
        session.query(Analyzer).delete()
        session.query(MetricDefinition).delete()
        session.query(Report).delete()
        print("Cleaning finished")

        print("Creating course ...")
        course = Course(tag="IT2810", name="Webutvikling")
        session.add(course)

        print("Creating assignment ...")
        assignment = Assignment(
            name="Øving 3", due_date=datetime(2023, 12, 20, 23, 59), course=course
        )
        session.add(assignment)

        print("Creating team ...")
        team = Team(github_link="https://github.com/pettelau/tsffbet", course=course)
        session.add(team)

        print("Creating repository ...")
        repository = Repository(
            github_link="https://github.com/pettelau/tsffbet",
            team=team,
            assignment=assignment,
        )
        session.add(repository)

        print("Creating analyzer ...")
        analyzer = Analyzer(name="Lighthouse Analyzer", creator="Enthe Nu")
        session.add(analyzer)

        print("Creating metrics ...")
        metric_definitions = [
            MetricDefinition(
                key_name="performance",
                display_name="Performance rating",
                value_type="range",
                extended_metadata=json.dumps({"fromRange": 1, "toRange": 100}),
                analyzer=analyzer,
            ),
            MetricDefinition(
                key_name="hasViewport",
                display_name="Viewport",
                value_type="bool",
                analyzer=analyzer,
            ),
            MetricDefinition(
                key_name="hasHTTPS",
                display_name="HTTPS",
                value_type="bool",
                analyzer=analyzer,
            ),
            MetricDefinition(
                key_name="js_workload",
                display_name="JS Main thread work",
                value_type="text",
                analyzer=analyzer,
            ),
        ]
        session.add_all(metric_definitions)

        print("Creating report 1 ...")
        report1_data = {
            "performance": 65,
            "hasViewport": False,
            "hasHTTPS": False,
            "js_workload": "JS main thread workload is high, consider optimizing JS code.",
        }
        report1 = Report(
            report=json.dumps(report1_data), repository=repository, analyzer=analyzer
        )
        session.add(report1)

        print("Creating report 2...")
        report2_data = {
            "performance": 88,
            "hasViewport": True,
            "hasHTTPS": False,
            "js_workload": "JS main thread workload is high, consider optimizing JS code.",
        }
        report2 = Report(
            report=json.dumps(report2_data), repository=repository, analyzer=analyzer
        )
        session.add(report2)

        session.commit()
        print("Finished!")
    except Exception as e:
        session.rollback()
        print("Something went wrong: ", e)
    finally:
        session.close()


if __name__ == "__main__":
    main()
