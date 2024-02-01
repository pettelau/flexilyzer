from fastapi import UploadFile, HTTPException
from pathlib import Path
import aiofiles
from configs.config import settings


def createIfNotExists(path: Path):
    return path.mkdir(parents=True, exist_ok=True)


async def store_file(analyzer_id: int, file: UploadFile, requirements: bool = False):
    try:
        directory = Path(settings.BASE_DIR) / str(analyzer_id)
        createIfNotExists(directory)

        file_path = directory / (
            settings.DEFAULT_SCRIPT_NAME
            if not requirements
            else settings.DEFAULT_REQUIREMENTS_NAME
        )

        async with aiofiles.open(file_path, mode="wb") as buffer:
            while content := await file.read(1024):
                await buffer.write(content)

    except OSError as e:
        print(e)
        raise HTTPException(status_code=500, detail="File storage failed.")


def validate_file(analyzer_id: int, requirements: bool = False):
    file_path = (
        Path(settings.BASE_DIR)
        / str(analyzer_id)
        / (
            settings.DEFAULT_SCRIPT_NAME
            if not requirements
            else settings.DEFAULT_REQUIREMENTS_NAME
        )
    )

    return file_path.is_file()


def validate_venv(analyzer_id: int):
    venv_path = Path(settings.BASE_DIR) / str(analyzer_id) / settings.DEFAULT_VENV_NAME
    return venv_path.is_dir()


def read_file(analyzer_id: int):
    try:
        file_path = (
            Path(settings.BASE_DIR) / str(analyzer_id) / settings.DEFAULT_SCRIPT_NAME
        )
        with file_path.open() as f:
            content = f.read()
    except OSError as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error reading file")

    return content


def delete_file(analyzer_id: int):
    try:
        file_path = (
            Path(settings.BASE_DIR) / str(analyzer_id) / settings.DEFAULT_SCRIPT_NAME
        )
        file_path.unlink(missing_ok=True)
    except OSError as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error deleting file")

    return None
