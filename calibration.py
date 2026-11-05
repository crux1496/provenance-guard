#!/usr/bin/env python3
"""
Calibration inputs for Milestones 3 and 4, and a table of how each signal
scores them.

    python calibration.py            # every input, every signal
    python calibration.py --model    # signal one only (Milestone 3)

The human passages are public-domain prose (Thoreau, Keller, Emerson, Twain),
so they're certainly human. The AI passages were generated for this purpose.
Neither stands in for criterion 1, which needs my own writing.
"""

import sys

CALIBRATION = {
    # Generic, even, model-typical prose.
    "clearly_ai": (
        "Artificial intelligence is transforming the way we live and work. "
        "From healthcare to education, AI-powered tools are helping people "
        "make better decisions and improve their productivity. However, it is "
        "important to consider the ethical implications of these technologies. "
        "By fostering collaboration between developers, policymakers, and the "
        "public, we can ensure that AI is used responsibly. Ultimately, the "
        "future of AI depends on our ability to balance innovation with "
        "accountability."
    ),
    # Thoreau, Walden (1854).
    "clearly_human": (
        "I went to the woods because I wished to live deliberately, to front "
        "only the essential facts of life, and see if I could not learn what "
        "it had to teach, and not, when I came to die, discover that I had not "
        "lived. I did not wish to live what was not life, living is so dear; "
        "nor did I wish to practise resignation, unless it was quite "
        "necessary. I wanted to live deep and suck out all the marrow of life, "
        "to live so sturdily and Spartan-like as to put to rout all that was "
        "not life, to cut a broad swath and shave close, to drive life into a "
        "corner, and reduce it to its lowest terms."
    ),
    # Helen Keller, The Story of My Life (1903). Plain, simple, human.
    "plain_human": (
        "The most important day I remember in all my life is the one on which "
        "my teacher, Anne Mansfield Sullivan, came to me. I am filled with "
        "wonder when I consider the immeasurable contrast between the two "
        "lives which it connects. It was the third of March, 1887, three "
        "months before I was seven years old. On the afternoon of that eventful "
        "day, I stood on the porch, dumb, expectant. I guessed vaguely from my "
        "mother's signs and from the hurrying to and fro in the house that "
        "something unusual was about to happen, so I went to the door and "
        "waited on the steps."
    ),
    # Emerson, Self-Reliance (1841). Formal human.
    "formal_human": (
        "There is a time in every man's education when he arrives at the "
        "conviction that envy is ignorance; that imitation is suicide; that he "
        "must take himself for better, for worse, as his portion; that though "
        "the wide universe is full of good, no kernel of nourishing corn can "
        "come to him but through his toil bestowed on that plot of ground "
        "which is given to him to till. The power which resides in him is new "
        "in nature, and none but he knows what that is which he can do, nor "
        "does he know until he has tried."
    ),
    # AI text, then lightly edited by hand: a contraction, a short sentence,
    # a dash, one specific detail.
    "edited_ai": (
        "Remote work has changed how teams communicate. It's not all good. "
        "Without the casual conversations of an office, people can feel "
        "isolated, and small problems go unnoticed for weeks. My old team "
        "tried a daily fifteen-minute call — nobody liked it at first. "
        "However, clear written updates and regular check-ins helped us stay "
        "aligned. In the end, remote work succeeds when teams are intentional "
        "about how they share information and support each other."
    ),
    # Plain, everyday writing of the kind signal one is said to accuse.
    "plain_everyday": (
        "I work at a shop near my house. I start at eight and I finish at four. "
        "The work is not hard but it is long. I like the people I work with. "
        "On Fridays we eat lunch together. After work I take the bus home and "
        "I cook dinner for my family. Then I help my son with his homework. "
        "It is a simple life but I am happy with it."
    ),
    # Dense AI prose, deliberately written with rare/unusual vocabulary.
    # Rare words are exactly what gpt2 fails to predict, so signal one reads
    # it as human-like even though it's AI-generated; signal two still sees
    # the even sentence lengths and bare punctuation and reads it as AI-like.
    # This is the Milestone 4 split case: the two signals land on opposite
    # sides of 0.5. See README > Signals and Scoring.
    "dense_ai_split": (
        "Contemporary epistemological frameworks necessitate wholesale "
        "reconsideration of anthropocentric paradigms underlying computational "
        "cognition itself. Interdisciplinary scholarship increasingly "
        "interrogates ontological presuppositions embedded within algorithmic "
        "determinism broadly construed. Such scholarship rarely transcends its "
        "own methodological circularity nonetheless. Practitioners must "
        "cultivate reflexive orientations toward emergent sociotechnical "
        "phenomena accordingly."
    ),
}

FIRST_THREE = ["clearly_ai", "clearly_human", "edited_ai"]


def main():
    import detector

    model_only = "--model" in sys.argv
    names = FIRST_THREE if model_only else list(CALIBRATION)

    if model_only:
        print(f"{'input':<16} {'perplexity':>10} {'model':>7}")
        for name in names:
            text = CALIBRATION[name]
            print(f"{name:<16} {detector.perplexity(text):>10.1f} "
                  f"{detector.model_signal(text):>7.3f}")
        return

    import scoring
    import stylometry

    print(f"{'input':<16} {'ppl':>6} {'model':>6} {'spread':>7} {'ttr':>6} "
          f"{'punct':>6} {'style':>6} {'comb':>6}  guess")
    for name in names:
        text = CALIBRATION[name]
        m = detector.model_signal(text)
        s = stylometry.style_signal(text)
        c = scoring.combine_signals(m, s)
        guess, _ = scoring.score_to_label(c)
        print(f"{name:<16} {detector.perplexity(text):>6.1f} {m:>6.3f} "
              f"{stylometry.sentence_length_spread(text):>7.3f} "
              f"{stylometry.type_token_ratio(text):>6.3f} "
              f"{stylometry.punctuation_density(text):>6.3f} "
              f"{s:>6.3f} {c:>6.3f}  {guess}")


if __name__ == "__main__":
    main()
