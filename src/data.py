from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


@dataclass
class DatasetSplit:
    x_train: list[str]
    x_test: list[str]
    y_train: list[str]
    y_test: list[str]


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV introuvable: {path}")
    return pd.read_csv(path)


def tabular_row_to_text(df: pd.DataFrame, label_column: str) -> list[str]:
    feature_cols = [c for c in df.columns if c != label_column]
    texts = []
    for _, row in df.iterrows():
        parts = [f"{col}={row[col]}" for col in feature_cols]
        texts.append(" ; ".join(parts))
    return texts


def extract_text_and_label(
    df: pd.DataFrame,
    label_column: str,
    text_column: str | None = None,
    auto_text_from_tabular: bool = False,
) -> tuple[list[str], list[str]]:
    if label_column not in df.columns:
        raise ValueError(f"Colonne label absente: {label_column}")

    labels = df[label_column].astype(str).tolist()

    if text_column and text_column in df.columns:
        texts = df[text_column].astype(str).tolist()
        return texts, labels

    if auto_text_from_tabular:
        texts = tabular_row_to_text(df, label_column=label_column)
        return texts, labels

    raise ValueError(
        "Aucune colonne texte valide. Donne --text-column ou active --auto-text-from-tabular."
    )


def split_dataset(
    texts: list[str], labels: list[str], test_size: float = 0.2, seed: int = 42
) -> DatasetSplit:
    x_train, x_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=test_size,
        random_state=seed,
        stratify=labels,
    )
    return DatasetSplit(x_train=x_train, x_test=x_test, y_train=y_train, y_test=y_test)
