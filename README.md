# Flexilyzer

### Master's thesis in Informatics at Norwegian University of Science and Technology (NTNU)

### Creators: Petter Lauvrak & Jacob Theisen

## About

Flexilyzer is an innovative platform developed to address the challenges of analyzing and evaluating student code projects across diverse programming environments. This project was created by the authors with a vision to streamline and ease the work for professors and Teaching Assistants (TAs) of analyzing student code projects. Flexilyzer offers a multipurpose solution by enabling the execution of fully customizable Python scripts for the purpose of analysis and testing. This makes the system useful for a wide range of student projects and programming languages.

The main workflow of the system begins when a professor or TA creates an analyzer script by specifying input parameters from a student's code project, such as a `URL` to their GitHub repository or a `.zip` file, alongside desired outputs like test results and code quality scores. Following this, the script is executed on a specific assignment through Flexilyzer's backend infrastructure. The analyzer outputs are finally displayed on Flexilyzer's frontend Dashboard in a clear and tailored manner.


## Prerequisites
Before you can set up the project locally, ensure you have the following prerequisites installed on your system:

```
node: ^18.17
python: ^3.11
celery: ^5.3.4
docker
docker-compose
```

## Setup Locally

Follow these steps to set up and run Flexilyzer on your local machine:

### Clone the Repository

```
git clone https://github.com/yourusername/flexilyzer.git
cd flexilyzer
```

### Install Dependencies

```
cd application/backend && pip -r requirements.txt
cd ../client && npm i
```

### Configure Environment Variables

To run the system locally with the default setup, you may simply copy the content of `.env.example` located in `application/backend` to a new `.env` file without any further modifications. The connection URLs will by default match the setup in `/application/container/docker-compose.yaml`.
The Environment variables below `# Upload folder structure` in `.env.example` defines the paths to where all files (Analyzer scripts or Student Deliveries) are uploaded. This may also remain unchanged for local development, but can easily be changed in the future if the locaction for uploaded files are changed to e.g. a separated directory.

### Running the project

In application/containers run:

```
docker compose up
```
In application/backend run:
```
python main.py
celery -A celery_app.main worker --loglevel=info
```

In application/client run:
```
npm run dev
```

### Other commands

To seed the db and set up the tables go to application/backend and run:

```
python run_seed.py
```

In our project we´ve used `Swagger` to create most of the `TypeScript Types` as well most API request logic for us, using the `openapi.json` schema automatically generated from `FastAPI`.

To update these `TypeScript Types` schemas for the `frontend` whenever there has been a relevate change to the `backend`, go to `application/client` and run

```
npx swagger-typescript-api -p http://127.0.0.1:8000/openapi.json -o ./extensions --modulart f
```

## Further reading

This project is a part of our master thesis at NTNU. For further reading and more in depth explanations of the system, read our thesis, which can be searched for at https://ntnuopen.ntnu.no/ntnu-xmlui/handle/11250/227489.

## Contact

If you have any questions, please don't hesitate to reach out to us at `petter.lauvrak@hotmail.com` or `jacobtheisen2211@gmail.com`.



