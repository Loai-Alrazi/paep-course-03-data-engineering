from pathlib import Path
import logging
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_ROOT / "data/raw/students_raw.csv"

OUTPUT_FILE = PROJECT_ROOT / "data/processed/students_ml_ready.csv"

LOG_FILE = PROJECT_ROOT / "logs/pipeline.log"

REQUIRED_COLUMNS = {
    "student_id",
    "name",
    "age",
    "gpa",
    "attendance",
    "city"
}

logger = logging.getLogger(__name__)

def load_data(file_path: Path) -> pd.DataFrame:
    logger.info(
        "Loading data from %s",
        file_path
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError(
            "Input dataset is empty."
        )

    logger.info(
        "Loaded %d rows and %d columns",
        len(df),
        len(df.columns)
    )

    return df


def validate_schema(
    df: pd.DataFrame
) -> None:
    missing_columns = (
        REQUIRED_COLUMNS
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Missing columns: "
            f"{sorted(missing_columns)}"
        )    

def convert_data_types(
    df: pd.DataFrame
) -> pd.DataFrame:
    df = df.copy()

    numeric_columns = [
        "student_id",
        "age",
        "gpa",
        "attendance"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df

def clean_data(
    df: pd.DataFrame
) -> pd.DataFrame:
    df = df.copy()

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Remove duplicate student IDs
    df = df.drop_duplicates(
        subset=["student_id"],
        keep="first"
    )

    # Clean text
    df["name"] = (
        df["name"]
        .astype("string")
        .str.strip()
        .replace("", pd.NA)
    )

    df["city"] = (
        df["city"]
        .astype("string")
        .str.strip()
        .str.title()
        .replace("", pd.NA)
    )

    # Invalid GPA
    df.loc[
        ~df["gpa"].between(0, 4),
        "gpa"
    ] = pd.NA

    # Invalid Age
    df.loc[
        ~df["age"].between(16, 80),
        "age"
    ] = pd.NA

    # Invalid attendance
    df.loc[
        ~df["attendance"].between(0, 100),
        "attendance"
    ] = pd.NA

    # Fill missing numeric values
    for column in [
        "age",
        "gpa",
        "attendance"
    ]:
        valid_values = df[column].dropna()
        if valid_values.empty:
            raise ValueError(
                f"Cannot fill {column}: no valid values available for the median."
            )
        # A median can be fractional even when the source values are integers.
        df[column] = df[column].astype("float64").fillna(valid_values.median())

    return df

def validate_data(
    df: pd.DataFrame
) -> None:
    errors = []

    if df.empty:
        errors.append(
            "Dataset is empty."
        )

    if df["student_id"].isnull().any():
        errors.append(
            "student_id contains NULL."
        )

    student_ids = df["student_id"].dropna()
    if (
        student_ids.isin([float("inf"), float("-inf")]).any()
        or student_ids.mod(1).ne(0).any()
    ):
        errors.append("student_id must contain finite integers.")

    if df["student_id"].duplicated().any():
        errors.append(
            "student_id is not unique."
        )

    if df["name"].astype("string").str.strip().fillna("").eq("").any():
        errors.append(
            "name contains NULL or blank values."
        )

    if not df["age"].between(
        16, 80
    ).fillna(False).all():
        errors.append(
            "Invalid age values."
        )

    if not df["gpa"].between(
        0, 4
    ).fillna(False).all():
        errors.append(
            "Invalid GPA values."
        )

    if not df["attendance"].between(
        0, 100
    ).fillna(False).all():
        errors.append(
            "Invalid attendance values."
        )

    if errors:
        raise ValueError(
            "Validation failed:\n"
            + "\n".join(
                f"- {error}"
                for error in errors
            )
        )


def generate_quality_report(
    df: pd.DataFrame
) -> pd.DataFrame:
    if df.empty:
        raise ValueError("Cannot generate a quality report for an empty dataset.")

    report = pd.DataFrame({
        "column": df.columns,

        "data_type": [
            str(dtype)
            for dtype in df.dtypes
        ],

        "missing_count": [
            df[column].isnull().sum()
            for column in df.columns
        ],

        "unique_count": [
            df[column].nunique()
            for column in df.columns
        ]
    })

    report["missing_percentage"] = (
        report["missing_count"]
        / len(df)
        * 100
    )

    return report


def save_data(
    df: pd.DataFrame,
    output_file: Path
) -> None:
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_file,
        index=False
    )

    logger.info(
        "Saved processed data to %s",
        output_file
    )


def run_pipeline() -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_FILE,
        encoding="utf-8",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    try:
        logger.info(
            "Pipeline started."
        )

        # Extract
        df = load_data(
            RAW_FILE
        )

        # Validate schema
        validate_schema(df)

        # Transform
        df = convert_data_types(df)

        # Clean
        df = clean_data(df)

        # Validate final data
        validate_data(df)

        # Convert student_id to integer after successful validation
        df["student_id"] = df["student_id"].astype("int64")

        # Generate data quality report 
        quality_report = generate_quality_report(df)
        print("\nData Quality Report:")
        print(quality_report)

        # Load
        save_data(
            df,
            OUTPUT_FILE
        )

        logger.info(
            "Pipeline completed successfully."
        )

        print(
            "Pipeline completed successfully."
        )

    except Exception as exc:
        logger.exception(
            "Pipeline failed: %s",
            exc
        )

        print(
            f"Pipeline failed: {exc}"
        )

        raise


if __name__ == "__main__":
    run_pipeline()        
        

