"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import math
import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies: the coefficient of variation (standard
    deviation of words-per-sentence divided by the mean).

    Returns:
        A float >= 0. **Higher means more human-like** (lumpier sentences).
        Typical prose lands between about 0.1 and 0.8.

    Edge case: with fewer than two sentences there is no spread to measure,
    so this returns 0.0, and `style_signal` treats that measure as having no
    opinion (0.5) rather than reading it as "perfectly even, so AI".
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return statistics.stdev(lengths) / mean if mean else 0.0


TTR_WINDOW = 50


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words, made fair across lengths.

    Plain TTR falls as text gets longer, so this is the moving-average TTR:
    the plain ratio inside every 50-word window, averaged. A 60-word text and
    a 300-word text are then on the same footing. Texts shorter than one
    window fall back to the plain ratio.

    Returns:
        A float between 0 and 1. **Higher means more varied vocabulary**,
        which I read as more human-like.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    if len(tokens) <= TTR_WINDOW:
        return len(set(tokens)) / len(tokens)
    ratios = [
        len(set(tokens[i:i + TTR_WINDOW])) / TTR_WINDOW
        for i in range(len(tokens) - TTR_WINDOW + 1)
    ]
    return statistics.mean(ratios)


# Full stops and plain commas are left out on purpose: every writer uses them,
# so they say little about who is writing. These are the marks that vary.
EXPRESSIVE_PUNCTUATION = set(";:—–-()!?\"'…")


def punctuation_density(text: str) -> float:
    """
    Expressive punctuation per 100 words: semicolons, colons, dashes,
    brackets, question and exclamation marks, quotation marks, ellipses.
    Apostrophes inside words (it's, don't) are not counted.

    Returns:
        A float >= 0. **Higher means more human-like**: generated prose tends
        to keep to full stops and commas.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    # Drop in-word apostrophes and hyphens so contractions and compounds
    # don't count as punctuation.
    stripped = re.sub(r"(?<=\w)['\-](?=\w)", "", text)
    count = sum(1 for ch in stripped if ch in EXPRESSIVE_PUNCTUATION)
    return 100.0 * count / len(tokens)


# ── Combining them ───────────────────────────────────────────────────────────

# Calibrated against the six inputs in calibration.py. Values above these
# midpoints score as more human-like on that measure; a logistic squashes
# each raw measure onto 0-1 the same way detector.py squashes perplexity.
SPREAD_MIDPOINT = 0.30
TTR_MIDPOINT = 0.78
PUNCT_MIDPOINT = 1.0


def _human_likeness(value: float, midpoint: float, steepness: float = 3.0) -> float:
    """0-1, higher = more human-like, saturating around the midpoint."""
    if midpoint <= 0:
        return 0.5
    return 1.0 / (1.0 + math.exp(-steepness * (value / midpoint - 1.0)))


def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    All three measures point the same way once scaled: higher sentence-length
    spread, higher (length-fair) type-token ratio, and more expressive
    punctuation all read as more human. So each is first turned into a
    0-1 "how human-like is this" score (`_human_likeness`, a logistic around a
    midpoint picked from the calibration inputs), then averaged and flipped
    with `1 - x` to match `detector.model_signal`'s direction, where higher
    means more likely AI.

    A one-sentence submission has no spread value at all
    (`sentence_length_spread` returns 0.0 for that edge case) — that is
    treated as "this measure has no opinion" (0.5 human-likeness) rather than
    as evidence of AI, so one short submission can't be swung by a measure
    that couldn't run.
    """
    spread = sentence_length_spread(text)
    ttr = type_token_ratio(text)
    punct = punctuation_density(text)

    spread_h = 0.5 if len(sentences(text)) < 2 else _human_likeness(spread, SPREAD_MIDPOINT)
    ttr_h = _human_likeness(ttr, TTR_MIDPOINT)
    punct_h = _human_likeness(punct, PUNCT_MIDPOINT)

    human_likeness = (spread_h + ttr_h + punct_h) / 3.0
    return round(1.0 - human_likeness, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
