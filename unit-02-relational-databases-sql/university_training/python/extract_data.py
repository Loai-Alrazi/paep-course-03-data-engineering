from pathlib import Path
import sqlite3

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE = BASE_DIR / "database" / "university.db"

OUTPUT_FILE = BASE_DIR / "data" / "student_performance.csv"


QUERY = """
SELECT
    s.student_id,
    s.full_name AS student_name,
    c.course_name,
    AVG(a.score) AS average_score
FROM assessments a
INNER JOIN students s
    ON a.student_id = s.student_id
INNER JOIN courses c
    ON a.course_id = c.course_id
GROUP BY
    s.student_id,
    s.full_name,
    c.course_id,
    c.course_name
ORDER BY average_score DESC
"""

def extract_data() -> pd.DataFrame:
    if not DATABASE.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE}"
        )

    connection = sqlite3.connect(DATABASE)

    try:
        df = pd.read_sql_query(
            QUERY,
            connection
        )
    finally:
        connection.close()

    return df


def validate_data(
    df: pd.DataFrame
) -> None:
    required_columns = {
        "student_id",
        "student_name",
        "course_name",
        "average_score"
    }

    missing = (
        required_columns
        - set(df.columns)
    )

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    if df.empty:
        raise ValueError(
            "Query returned no data."
        )

    if not df["average_score"].between(
        0, 100
    ).all():
        raise ValueError(
            "Invalid average scores."
        )


def save_data(
    df: pd.DataFrame
) -> None:
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )


def load_output_data() -> pd.DataFrame:
    return pd.read_csv(OUTPUT_FILE)

def print_summary(
    df: pd.DataFrame
) -> None:
    total_students = df["student_id"].nunique()
    average_score = df["average_score"].mean()
    highest_score = df["average_score"].max()
    lowest_score = df["average_score"].min()

    print(f"Total Students: {total_students}")
    print(f"Average Score: {average_score:.2f}")
    print(f"Highest Score: {highest_score:.2f}")
    print(f"Lowest Score: {lowest_score:.2f}")



def main() -> None:
    df = extract_data()
    validate_data(df)
    save_data(df)

    report_df = load_output_data()
    print_summary(report_df)

    print(
        "Student performance dataset created."
    )


if __name__ == "__main__":
    main()    
            


                