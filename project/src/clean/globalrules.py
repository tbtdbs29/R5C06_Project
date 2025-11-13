from __future__ import annotations
from typing import TypedDict, Literal, NotRequired
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DEFAULT_GRAPHS_FOLDER = PROJECT_ROOT / "project" / "src" / "graphs"
DEFAULT_CONVERTION_RULES = PROJECT_ROOT / "project" / "src" / "clean"
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "out"

JSON_PATH = PROJECT_ROOT / "project" / "src" / "clean" / "convertion_rules.json"

type validation_rule_name = Literal[
    "notNull",
    "notNegative",
    "positiveNumber",
    "toLowerCase",
    "toUpperCase",
    "beforeNow",
    "afterNow",
    "int",
    "string",
    "float",
    "double",
    "boolean",
    "array",
    "date",
    "unique",
]

type standardisation_rule_name = Literal[
    "toLowerCase",
    "toUpperCase",
    "trimSpaces",
    "parseDate",
    "normalizeDuration",
    "extractGenreIds",
    "normalizeTags",
    "normalizeBoolean",
    "toArray",
    "toInt",
    "toFloat",
    "toDouble",
    "toString",
    "toBoolean",
    "trimEmoji",
    "convertToQuantitative"
]

class CsvConfig(TypedDict):
    header_rows: list[int]
    skip_rows: list[int]
    rename_columns: dict[str, str]
    validation_rules: dict[str, list[validation_rule_name]]
    standardisation_rules: NotRequired[dict[str, list[standardisation_rule_name]]]

type RulesByCsv = dict[str, CsvConfig]

# F - 1 à 4 ans,F - 5 à 9 ans,F - 10 à 14 ans,F - 15 à 19 ans,F - 20 à 24 ans,F - 25 à 29 ans,F - 30 à 34 ans,F - 35 à 39 ans,F - 40 à 44 ans,F - 45 à 49 ans,F - 50 à 54 ans,F - 55 à 59 ans,F - 60 à 64 ans,F - 65 à 69 ans,F - 70 à 74 ans,F - 75 à 79 ans,F - 80 à 99 ans, F - NR,
# H - 1 à 4 ans,H - 5 à 9 ans,H - 10 à 14 ans,H - 15 à 19 ans,H - 20 à 24 ans,H - 25 à 29 ans,H - 30 à 34 ans,H - 35 à 39 ans,H - 40 à 44 ans,H - 45 à 49 ans,H - 50 à 54 ans,H - 55 à 59 ans,H - 60 à 64 ans,H - 65 à 69 ans,H - 70 à 74 ans,H - 75 à 79 ans,H - 80 à 99 ans, H - NR,

RULES_BY_CSV: RulesByCsv = {
    "sports_light.csv": {
        "header_rows": [0],
        "skip_rows": [],
        "rename_columns": {
            "Commune": "commune",
            "Région": "region",
            "Fédération": "federation",
            "Total": "total",
        },
        "standardisation_rules": {
            "commune": ["trimSpaces", "toString", "toLowerCase"],
            "region": ["trimSpaces", "toString", "toLowerCase"],
            "federation": ["trimSpaces", "toString", "toLowerCase"],
            "total": ["trimSpaces", "toInt"],
        },
        "validation_rules": {
            "commune": ["notNull", "string"],
            "region": ["notNull", "string"],
            "federation": ["notNull", "string"],
            "total": ["notNull", "positiveNumber"],
        },
    },
}

def get_rules() -> RulesByCsv:
    return RULES_BY_CSV


def get_rule_for(csv_name: str) -> CsvConfig | None:
    return RULES_BY_CSV.get(csv_name)


__all__ = [
    "DEFAULT_DATA_DIR",
    "DEFAULT_OUTPUT_DIR",
    "RULES_BY_CSV",
    "get_rules",
    "get_rule_for",
]
