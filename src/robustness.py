from __future__ import annotations

import random

from .evaluate import compute_metrics


CHAR_SUBS = {
    "a": "@",
    "e": "3",
    "i": "1",
    "o": "0",
    "s": "$",
}


def _random_delete_char(token: str, rng: random.Random) -> str:
    if len(token) <= 3:
        return token
    idx = rng.randint(1, len(token) - 2)
    return token[:idx] + token[idx + 1 :]


def _swap_adjacent(token: str, rng: random.Random) -> str:
    if len(token) <= 3:
        return token
    idx = rng.randint(1, len(token) - 2)
    chars = list(token)
    chars[idx], chars[idx + 1] = chars[idx + 1], chars[idx]
    return "".join(chars)


def _simple_substitute(token: str) -> str:
    return "".join(CHAR_SUBS.get(ch, ch) for ch in token)


def perturb_text(text: str, severity: float, seed: int = 42) -> str:
    rng = random.Random(seed)
    tokens = text.split()
    if not tokens:
        return text

    k = max(1, int(len(tokens) * severity))
    candidate_indices = [i for i, tok in enumerate(tokens) if len(tok) > 3]
    if not candidate_indices:
        return text

    rng.shuffle(candidate_indices)
    chosen = candidate_indices[:k]

    for i in chosen:
        op = rng.choice(["delete", "swap", "sub"])
        if op == "delete":
            tokens[i] = _random_delete_char(tokens[i], rng)
        elif op == "swap":
            tokens[i] = _swap_adjacent(tokens[i], rng)
        else:
            tokens[i] = _simple_substitute(tokens[i])

    return " ".join(tokens)


def evaluate_robustness(model, texts: list[str], labels: list[str], severity: float, seed: int = 42) -> dict:
    clean_pred = model.predict(texts)
    clean_metrics = compute_metrics(labels, clean_pred)

    perturbed = [perturb_text(t, severity=severity, seed=seed + i) for i, t in enumerate(texts)]
    pert_pred = model.predict(perturbed)
    pert_metrics = compute_metrics(labels, pert_pred)

    return {
        "severity": severity,
        "clean": clean_metrics,
        "perturbed": pert_metrics,
        "delta_accuracy": clean_metrics["accuracy"] - pert_metrics["accuracy"],
        "delta_f1_macro": clean_metrics["f1_macro"] - pert_metrics["f1_macro"],
    }
