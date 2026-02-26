from __future__ import annotations

import csv
from collections import Counter

import pandas as pd

_DELIMITER_CANDIDATES = [",", ";", "\t", "|"]


def _detect_primary_delimiter(header_line: str) -> str:
    counts = Counter({delimiter: header_line.count(delimiter) for delimiter in _DELIMITER_CANDIDATES})
    primary, occurrences = counts.most_common(1)[0]
    return primary if occurrences > 0 else ","


def inspect_csv_issues(file_path: str, max_lines: int = 2000) -> tuple[str, int, list[str]]:
    with open(file_path, "r", encoding="utf-8", errors="replace", newline="") as handle:
        first_line = handle.readline()
        if not first_line:
            return ",", 0, ["CSV appears to be empty."]

        primary_delimiter = _detect_primary_delimiter(first_line)
        expected_columns = len(
            next(
                csv.reader(
                    [first_line],
                    delimiter=primary_delimiter,
                    skipinitialspace=True,
                )
            )
        )

        mixed_delimiter_rows = 0
        inconsistent_column_rows = 0
        blank_rows = 0

        for idx, raw_line in enumerate(handle, start=2):
            if idx > max_lines:
                break

            if not raw_line.strip():
                blank_rows += 1
                continue

            if primary_delimiter == "," and raw_line.count(";") > raw_line.count(","):
                mixed_delimiter_rows += 1

            row = next(
                csv.reader(
                    [raw_line],
                    delimiter=primary_delimiter,
                    skipinitialspace=True,
                )
            )
            if len(row) != expected_columns:
                inconsistent_column_rows += 1

    warnings: list[str] = []
    if mixed_delimiter_rows:
        warnings.append(
            f"Detected {mixed_delimiter_rows} sampled row(s) with alternate delimiters; parser normalized to '{primary_delimiter}'."
        )
    if inconsistent_column_rows:
        warnings.append(
            f"Detected {inconsistent_column_rows} sampled row(s) with inconsistent column counts (often unquoted commas in values)."
        )
    if blank_rows:
        warnings.append(f"Detected {blank_rows} blank row(s) in sampled data.")

    return primary_delimiter, expected_columns, warnings


def load_tolerant_csv(file_path: str, nrows: int | None = None) -> tuple[pd.DataFrame, list[str]]:
    primary_delimiter, expected_columns, warnings = inspect_csv_issues(file_path)
    skipped_rows = 0

    def _on_bad_lines(_: list[str]) -> None:
        nonlocal skipped_rows
        skipped_rows += 1
        return None

    df = pd.read_csv(
        file_path,
        nrows=nrows,
        low_memory=True,
        encoding_errors="replace",
        engine="python",
        delimiter=primary_delimiter,
        on_bad_lines=_on_bad_lines,
    )

    if expected_columns and len(df.columns) != expected_columns:
        warnings.append(
            f"Header suggests {expected_columns} column(s), parser produced {len(df.columns)} column(s)."
        )
    if skipped_rows:
        warnings.append(f"Skipped {skipped_rows} malformed row(s) during parsing.")

    return df, warnings
