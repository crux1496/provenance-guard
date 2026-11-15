"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.

Criterion 4 ("every appeal changes status and is recorded") can't be
expressed here — `run_eval.py` only ever calls `/submit`, and the appeal path
needs a real `content_id` from one submission before it can call `/appeal`.
I tested that one by hand instead, with a short script run three times; see
README > Run Log and Verdicts for the output.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # Ten pieces I actually wrote. The first three are plain on purpose —
        # short sentences, everyday words — because that's exactly the shape
        # of writing trace.md predicted my system would be most likely to
        # accuse.
        "texts": [
            "I work on this project after dinner. I open my laptop and read "
            "the code. Some nights it goes fast. Some nights it does not. I "
            "take a break and come back to it.",
            "My dog sleeps next to my desk while I type. He does not care "
            "about perplexity scores. He just wants a walk. I finish one "
            "more test and then we go outside.",
            "I like coffee in the morning before I start coding. It helps me "
            "think. Without it I feel slow. The code still runs the same "
            "either way, but I feel better.",
            "Running the attack set for the first time was nerve wracking. I "
            "kept expecting the server to crash, but it mostly just returned "
            "calm little JSON objects telling me I was wrong about my own "
            "thresholds.",
            "The part of this assignment that stuck with me most was "
            "realizing my style signal couldn't tell a deliberately even "
            "poem from a machine. That blind spot felt obvious once I saw "
            "it, and invisible before.",
            "I almost skipped writing the criteria before building anything, "
            "because it felt backwards to grade myself before I had results. "
            "Doing it anyway was the point, and I only understood that after "
            "the attack set actually surprised me.",
            "Debugging the detector load failure taught me more about my own "
            "laptop's memory than about machine learning. Closing a dozen "
            "background apps fixed a problem I was ready to blame on the "
            "model.",
            "I wrote my appeal label text by imagining a classmate getting "
            "it on an essay they wrote themselves at midnight before a "
            "deadline. That image changed three words I would have "
            "otherwise left alone.",
            "This was the first class project where I cared more about "
            "being wrong honestly than about passing a target I set for "
            "myself. That's a strange thing to say about a grade, but it's "
            "true.",
            "On the second attempt I finally got the server to answer "
            "without a five hundred error, and I sat there for a second "
            "just staring at the terminal before I remembered to actually "
            "check if the answer was right.",
        ],
    },
    {
        "name": "clearly AI vs clearly human",
        "criterion": 2,
        # 5 generic, AI-typical paragraphs, then 5 specific, first-person
        # human ones. Compared as two groups of 5 in the write-up, not
        # individually.
        "texts": [
            # --- AI-typical (generic, even, safe vocabulary) ---
            "In today's fast-paced world, effective time management has "
            "become more important than ever. By prioritizing tasks and "
            "setting clear goals, individuals can significantly improve "
            "their productivity. Furthermore, taking regular breaks helps "
            "maintain focus and prevents burnout. Ultimately, a balanced "
            "approach to work and rest leads to sustainable long-term "
            "success.",
            "Cloud computing continues to transform the way businesses "
            "operate. Organizations can scale their infrastructure "
            "efficiently, reducing costs while increasing flexibility. "
            "However, it is important to consider security implications "
            "when migrating sensitive data. Overall, the benefits of cloud "
            "adoption often outweigh the associated risks when implemented "
            "thoughtfully.",
            "Maintaining a healthy diet is essential for overall "
            "well-being. Incorporating a variety of fruits, vegetables, and "
            "whole grains provides the body with necessary nutrients. "
            "Additionally, staying hydrated supports many bodily functions. "
            "Making small, consistent changes to one's eating habits can "
            "lead to significant long-term health benefits.",
            "Effective communication is a cornerstone of successful "
            "teamwork. When team members share information openly, "
            "misunderstandings are reduced and collaboration improves. "
            "Moreover, active listening plays a crucial role in building "
            "trust. By fostering an environment of transparency, "
            "organizations can achieve better outcomes.",
            "The rise of remote work has changed how companies approach "
            "employee engagement. Providing flexible schedules and clear "
            "expectations helps maintain productivity. At the same time, "
            "regular check-ins foster a sense of connection among team "
            "members. Ultimately, successful remote work depends on trust "
            "and communication.",
            # --- clearly human (specific, first-person, uneven) ---
            "My grandmother used to burn the first pancake every single "
            "time, on purpose, she said, to wake up the pan. I thought she "
            "was joking until I started cooking myself and realized she "
            "probably wasn't.",
            "The bus was twenty minutes late again this morning, and the "
            "guy next to me kept checking his phone like that would make it "
            "come faster. It didn't. We just stood there, annoyed, "
            "together.",
            "I don't actually like jazz that much, but my roommate plays it "
            "constantly, and somewhere around month three I caught myself "
            "humming along to a Coltrane solo in the shower. Make of that "
            "what you will.",
            "There's a crack in my ceiling shaped vaguely like Florida "
            "that I've been staring at for two years instead of calling "
            "the landlord. At this point fixing it almost feels like "
            "losing a pet.",
            "I tried to teach my little cousin chess last weekend and she "
            "immediately invented a rule where the queen can also fly, and "
            "honestly her version was more fun than real chess.",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # 3 expected-AI, 3 expected-human (reusing the pairs from criterion
        # 2's two groups), plus 3 genuinely borderline inputs that mix a
        # hedge, an aside, and an even, generic opening.
        "texts": [
            "In today's fast-paced world, effective time management has "
            "become more important than ever. By prioritizing tasks and "
            "setting clear goals, individuals can significantly improve "
            "their productivity. Furthermore, taking regular breaks helps "
            "maintain focus and prevents burnout. Ultimately, a balanced "
            "approach to work and rest leads to sustainable long-term "
            "success.",
            "Cloud computing continues to transform the way businesses "
            "operate. Organizations can scale their infrastructure "
            "efficiently, reducing costs while increasing flexibility. "
            "However, it is important to consider security implications "
            "when migrating sensitive data. Overall, the benefits of cloud "
            "adoption often outweigh the associated risks when implemented "
            "thoughtfully.",
            "Maintaining a healthy diet is essential for overall "
            "well-being. Incorporating a variety of fruits, vegetables, and "
            "whole grains provides the body with necessary nutrients. "
            "Additionally, staying hydrated supports many bodily functions. "
            "Making small, consistent changes to one's eating habits can "
            "lead to significant long-term health benefits.",
            "My grandmother used to burn the first pancake every single "
            "time, on purpose, she said, to wake up the pan. I thought she "
            "was joking until I started cooking myself and realized she "
            "probably wasn't.",
            "The bus was twenty minutes late again this morning, and the "
            "guy next to me kept checking his phone like that would make it "
            "come faster. It didn't. We just stood there, annoyed, "
            "together.",
            "I don't actually like jazz that much, but my roommate plays it "
            "constantly, and somewhere around month three I caught myself "
            "humming along to a Coltrane solo in the shower. Make of that "
            "what you will.",
            "Team communication matters. When people talk openly, less "
            "gets missed, and projects tend to move faster — at least "
            "that's been my experience here, though I could be wrong about "
            "the general case.",
            "Robotics research has advanced considerably in recent years, "
            "driven by better sensors and faster processors; still, most "
            "warehouse robots today just follow a line on the floor, which "
            "is less exciting than it sounds.",
            "Our team decided to try daily standups. Some days it helped, "
            "some days it felt like busywork, and I honestly can't tell yet "
            "if it's worth keeping, which is probably its own kind of "
            "answer.",
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing"},                 # no text field at all
            {"text": "", "creator_id": "eval_bad_empty"},       # empty text
            {"text": "   ", "creator_id": "eval_bad_whitespace"},  # whitespace only
            {"text": 12345, "creator_id": "eval_bad_number"},   # text not a string
            {"text": "word " * 5000, "creator_id": "eval_bad_huge"},  # ~25,000 chars
            ["not", "an", "object"],                            # JSON, but not an object
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, (dict, list)):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict or list — bodies are "
                        f"whole request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
