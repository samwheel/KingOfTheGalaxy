#!/usr/bin/env python3
"""Markov-chain name generator with a small CLI.

Usage: python name_generator.py --count 20 --min 3 --max 8 --order 2
"""
from __future__ import annotations

import collections
import random
from typing import Dict, List


def read_names(path: str) -> List[str]:
    with open(path, "r", encoding="utf8") as fh:
        return [line.strip() for line in fh if line.strip()]


def train_model(names: List[str], order: int = 2) -> Dict[str, collections.Counter]:
    """Train an order-N character-level Markov model.

    Returns a mapping from state (string of length `order`) to Counter of next characters.
    Uses '^' as start padding and '$' as end token.
    """
    model: Dict[str, collections.Counter] = {}
    start_token = "^" * order
    end_token = "$"

    for raw in names:
        name = raw.strip()
        if not name:
            continue
        padded = f"{start_token}{name}{end_token}"
        for i in range(len(padded) - order):
            state = padded[i : i + order]
            nxt = padded[i + order]
            model.setdefault(state, collections.Counter())[nxt] += 1

    return model


def _weighted_choice(counter: collections.Counter) -> str:
    total = sum(counter.values())
    if total == 0:
        raise ValueError("Empty counter passed to weighted choice")
    r = random.randint(1, total)
    upto = 0
    for k, v in counter.items():
        upto += v
        if upto >= r:
            return k
    return next(iter(counter))


def generate_name(
    model: Dict[str, collections.Counter], order: int = 2, min_len: int = 2, max_len: int = 12, max_attempts: int = 20
) -> str:
    """Generate a single name using the trained model.

    Ensures produced name length is within [min_len, max_len] when possible.
    """
    start_state = "^" * order
    end_token = "$"

    chars: List[str] = []
    for attempt in range(max_attempts):
        state = start_state
        chars = []
        while True:
            counter = model.get(state)
            if not counter:
                break
            nxt = _weighted_choice(counter)
            if nxt == end_token:
                break
            chars.append(nxt)
            state = (state + nxt)[-order:]
            if len(chars) >= max_len:
                break

        name = "".join(chars)
        if min_len <= len(name) <= max_len:
            return name.capitalize()

    if chars:
        return ("".join(chars)[:max_len]).capitalize()
    return ""


def generate_names(
    model: Dict[str, collections.Counter], count: int = 20, order: int = 2, min_len: int = 2, max_len: int = 12
) -> List[str]:
    out = []
    seen = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        name = generate_name(model, order=order, min_len=min_len, max_len=max_len)
        if not name:
            continue
        if name in seen:
            continue
        seen.add(name)
        out.append(name)
    return out


def main():
    names = read_names("star_names.txt")
    if not names:
        print("No names found in star_names.txt")
        return

    model = train_model(names, order=2)
    for n in generate_names(model, count=20, order=2, min_len=3, max_len=8):
        print(n)


if __name__ == "__main__":
    main()