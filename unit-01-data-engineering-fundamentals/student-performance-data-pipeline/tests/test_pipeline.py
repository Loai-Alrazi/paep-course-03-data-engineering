from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import pandas as pd

from src import pipeline


class PipelineTests(unittest.TestCase):
    def sample(self):
        return pd.DataFrame({
            "student_id": [1, 2],
            "name": [" Ahmed ", "Sara"],
            "age": [20, 21],
            "gpa": [3.0, 4.0],
            "attendance": [90, 95],
            "city": [" sanaa ", "Taiz"],
        })

    def test_current_dataset(self):
        raw = pipeline.load_data(pipeline.RAW_FILE)
        pipeline.validate_schema(raw)
        result = pipeline.clean_data(pipeline.convert_data_types(raw))
        pipeline.validate_data(result)
        self.assertEqual(len(result), 8)
        self.assertEqual(result.loc[result.student_id == 1004, "gpa"].item(), 3.5)
        self.assertEqual(result.loc[result.student_id == 1005, "age"].item(), 22)
        self.assertEqual(result.loc[result.student_id == 1006, "attendance"].item(), 92)

    def test_blank_and_missing_names_rejected(self):
        for name in ["", "   ", None]:
            with self.subTest(name=name):
                frame = self.sample()
                frame.loc[0, "name"] = name
                with self.assertRaisesRegex(ValueError, "name contains"):
                    pipeline.validate_data(pipeline.clean_data(frame))

    def test_invalid_student_ids_rejected(self):
        for student_id in [1.5, float("inf"), float("-inf"), None, "invalid"]:
            with self.subTest(student_id=student_id):
                frame = self.sample()
                frame["student_id"] = [student_id, 2]
                frame = pipeline.convert_data_types(frame)
                with self.assertRaisesRegex(ValueError, "student_id"):
                    pipeline.validate_data(frame)

    def test_nullable_missing_numbers_rejected(self):
        for column in ["age", "gpa", "attendance"]:
            with self.subTest(column=column):
                frame = self.sample()
                frame[column] = pd.Series([pd.NA, frame[column][1]], dtype="Float64")
                with self.assertRaisesRegex(ValueError, "Invalid"):
                    pipeline.validate_data(frame)

    def test_all_invalid_column_has_clear_error(self):
        for column in ["age", "gpa", "attendance"]:
            with self.subTest(column=column):
                frame = self.sample()
                frame[column] = [-1, None]
                with self.assertRaisesRegex(ValueError, f"Cannot fill {column}"):
                    pipeline.clean_data(frame)

    def test_fractional_median_for_nullable_integers(self):
        frame = pd.concat([self.sample(), self.sample().iloc[[0]]], ignore_index=True)
        frame["student_id"] = [1, 2, 3]
        frame["age"] = pd.Series([20, 21, pd.NA], dtype="Int64")
        result = pipeline.clean_data(frame)
        self.assertEqual(result.loc[2, "age"], 20.5)
        pipeline.validate_data(result)

    def test_duplicates_and_text_cleaning(self):
        frame = pd.concat([self.sample(), self.sample()], ignore_index=True)
        result = pipeline.clean_data(frame)
        self.assertEqual(len(result), 2)
        self.assertEqual(result.loc[0, "name"], "Ahmed")
        self.assertEqual(result.loc[0, "city"], "Sanaa")

    def test_missing_schema_column(self):
        with self.assertRaisesRegex(ValueError, "Missing columns.*gpa"):
            pipeline.validate_schema(self.sample().drop(columns="gpa"))

    def test_missing_and_empty_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.csv"
            with self.assertRaises(FileNotFoundError):
                pipeline.load_data(path)
            self.sample().iloc[:0].to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, "empty"):
                pipeline.load_data(path)

    def test_empty_quality_report_rejected(self):
        with self.assertRaisesRegex(ValueError, "empty dataset"):
            pipeline.generate_quality_report(self.sample().iloc[:0])

    def test_run_from_another_directory_and_preserve_output_on_invalid_input(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            source = root / "src" / "pipeline.py"
            source.parent.mkdir(parents=True)
            shutil.copyfile(pipeline.__file__, source)
            raw = root / "data" / "raw" / "students_raw.csv"
            raw.parent.mkdir(parents=True)
            frame = self.sample()
            frame.loc[0, "name"] = "أحمد"
            frame.to_csv(raw, index=False)
            completed = subprocess.run(
                [sys.executable, str(source)], cwd=directory,
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            output = root / "data" / "processed" / "students_ml_ready.csv"
            self.assertEqual(pd.read_csv(output).loc[0, "name"], "أحمد")
            self.assertTrue((root / "logs" / "pipeline.log").exists())
            self.assertFalse((Path(directory) / "logs").exists())
            original = output.read_bytes()
            frame["name"] = "   "
            frame.to_csv(raw, index=False)
            failed = subprocess.run(
                [sys.executable, str(source)], cwd=directory,
                capture_output=True, text=True, timeout=30,
            )
            self.assertNotEqual(failed.returncode, 0)
            self.assertEqual(output.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
