import os
import uuid
import pandas as pd
from werkzeug.utils import secure_filename
from flask import current_app

from app.extensions import db
from app.models import Dataset
from app.utils.exceptions import ValidationAppError, NotFoundError


class DatasetService:

    @staticmethod
    def upload_dataset(user_id: int, file, display_name: str) -> dict:
        original_filename = secure_filename(file.filename)
        if not original_filename.endswith(".csv"):
            raise ValidationAppError({"file": ["Only .csv files are supported"]})

        try:
            df = pd.read_csv(file)
        except Exception:
            raise ValidationAppError({"file": ["Could not parse file as CSV"]})

        max_rows = current_app.config["MAX_DATASET_ROWS"]
        if len(df) > max_rows:
            raise ValidationAppError({
                "file": [f"Dataset has {len(df)} rows. MLab is optimized for "
                         f"learning — max {max_rows} rows."]
            })
        if len(df) < 10:
            raise ValidationAppError({"file": ["Dataset too small — at least 10 rows required"]})

        upload_dir = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_dir, exist_ok=True)
        stored_filename = f"{uuid.uuid4().hex}.csv"
        df.to_csv(os.path.join(upload_dir, stored_filename), index=False)

        columns_info = {col: str(dtype) for col, dtype in df.dtypes.items()}

        dataset = Dataset(
            user_id=user_id, name=display_name or original_filename,
            filename=stored_filename, original_filename=original_filename,
            row_count=len(df), column_count=len(df.columns),
            columns_info=columns_info, is_builtin=False,
        )
        db.session.add(dataset)
        db.session.commit()
        return dataset.to_dict()

    @staticmethod
    def get_user_datasets(user_id: int) -> list:
        datasets = Dataset.query.filter_by(user_id=user_id).order_by(Dataset.created_at.desc()).all()
        return [d.to_dict() for d in datasets]

    @staticmethod
    def get_dataset_or_404(dataset_id: int, user_id: int) -> Dataset:
        dataset = Dataset.query.filter_by(id=dataset_id, user_id=user_id).first()
        if not dataset:
            raise NotFoundError("Dataset not found")
        return dataset

    @staticmethod
    def load_dataframe(dataset_id: int, user_id: int) -> pd.DataFrame:
        dataset = DatasetService.get_dataset_or_404(dataset_id, user_id)   # ← reused, DRY
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], dataset.filename)
        return pd.read_csv(path)