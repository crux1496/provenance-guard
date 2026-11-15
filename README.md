# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. **The writer's site sends `POST /submit`** with `{"text": ..., "creator_id": ...}`.
2. **The route validates the input.** Missing or empty text, text that isn't a
   string, text under 5 words or over 20,000 characters, or a missing
   `creator_id` all stop here with a `400` and a logged `rejected` entry —
   nothing downstream ever sees a bad request.
3. **The route mints a `content_id`** (a UUID), the handle the writer will
   need to appeal later.
4. **Signal one reads the text for meaning** (`detector.model_signal`) — a
   local gpt2 model scores how predictable the text is.
5. **Signal two measures the text as text** (`stylometry.style_signal`) —
   sentence-length spread, vocabulary variety, and punctuation, with no idea
   what any of it says.
6. **The two signals combine into one score** (`scoring.combine_signals`) —
   averaged when they agree, weighted toward whichever one reads more human
   when they split.
7. **The score becomes a label** (`scoring.score_to_label`) — one of three
   full sentences a reader actually sees.
8. **The decision is logged and returned.** `audit.log_decision` writes all
   nine fields to `logs/audit.jsonl`; the same numbers go back in the
   response.

The full trace, written before any of this was code, is in `trace.md`.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** perplexity under a local gpt2 model — how surprised the
model is by each next word — squashed onto 0–1 so low surprise scores high.

**Why that might differ between human and AI writing:** a language model
writes by picking a likely next word, so its own output tends to be the kind
of text a model finds easy to predict. People wander: odd word choices,
abrupt turns, the specific instead of the typical.

**What it can't see:** who wrote it. Predictability is a property of
vocabulary and sentence shape, not of authorship. Someone writing plainly on
purpose, a younger writer, or someone sticking to words they're sure of in a
second language all produce predictable text — and this signal scores all of
them as machine-like. The reverse holds too: dense, rare-word prose (AI or
human) reads as human here, because rare words are exactly what gpt2 fails to
predict. It also only looks at the first 400 tokens.

### Signal two — the style signal

**What it measures:** the shape of the text, not its meaning — the
coefficient of variation of sentence length, a length-fair type-token ratio
(vocabulary variety), and the density of "expressive" punctuation
(semicolons, colons, dashes, brackets, `!`, `?`, quotation marks).

**Why that might differ between human and AI writing:** generated prose tends
toward even, mid-length sentences, a safe vocabulary, and tidy punctuation,
because that's what "most likely next word" produces on average. Human
writing is lumpier — a three-word sentence next to a forty-word one, a dash,
an aside.

**What it can't see:** anything the text actually says. It cannot read.
Typos, breaking a sentence in two, or pasting in a quotation all move the
score without changing a single idea — which is exactly what makes it cheap
to game on purpose. It also can't tell a deliberately even list or poem from
a machine.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Scale both signals so 0.5 is the midpoint for each. If they
**agree** — both on the same side of 0.5, or both close to it — average them
with equal weight. If they **disagree** by at least 0.15 (one signal reads
human, the other reads AI), don't average: weight the one reading more human
at 0.7 against 0.3 for the one reading more AI.

Why: the expensive mistake here is one-sided (`trace.md`'s false-positive
trace). A style signal that can't read a word, or a model signal that
mistakes plain writing for AI, shouldn't be able to drag a real writer's score
up on its own. Splitting a disagreement 50/50 lets either signal's blind spot
do exactly that. Weighting toward "human" when they split means a false
accusation needs *both* signals to agree, not just one.

**The numbers:** `WEIGHT_MODEL_SIGNAL = WEIGHT_STYLE_SIGNAL = 0.5` when they
agree; `0.7` / `0.3` toward the human-leaning signal when they disagree by
`>= 0.15`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

`calibration.py`'s `dense_ai_split` input is AI-generated text written with
deliberately rare, formal vocabulary ("epistemological frameworks,"
"ontological presuppositions"). Signal one reads it as `model_score = 0.266`
— human-leaning, because the unusual words are exactly what gpt2 doesn't see
coming. Signal two reads the same text as `style_score = 0.688` — AI-leaning,
because the sentences are even and there's almost no expressive punctuation.

That's a genuine split (gap of 0.42, both past the 0.15 threshold), so my
rule weights toward the human-leaning signal: `0.7 * 0.266 + 0.3 * 0.688 =
0.392`, which lands in **unsure** rather than being averaged up into
**high-confidence AI** at a plain 0.5 midpoint. I'd rather this genuinely
AI-written text land in "unsure" than risk the same rule, run on a real
writer whose formal prose confuses signal two, calling them AI.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | "We think this was probably written by a person." |
| unsure | 0.35 – 0.65 | "We couldn't tell whether this was written by a person or by AI. That's on us, not on you — it isn't a judgment about your writing, and no action is needed." |
| high-confidence AI | 0.65 – 1.00 | "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong." |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

I put the blame on the system, not the writer ("that's on us, not on you"),
because the person reading it may well have written every word themselves —
and both of my signals have a documented blind spot for exactly the writers
least able to argue back. "No action is needed" is there so an "unsure"
label doesn't read as a half-accusation that quietly expects a response. I
left the word "threshold" and any number out of all three labels; a writer
shouldn't need to understand perplexity or type-token ratio to know what the
site is telling them.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of inputs. Additionally, the overall performance of the solution depends on a number of important variables.", "creator_id": "cruz"}'
```

```json
{
  "content_id": "8d3ca2c2-01ea-4ec6-af74-03f1cb948c2b",
  "creator_id": "cruz",
  "guess": "ai",
  "confidence": 0.8075,
  "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.",
  "model_score": 0.8876,
  "style_score": 0.7275,
  "combined_score": 0.8075,
  "status": "decided"
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "8d3ca2c2-01ea-4ec6-af74-03f1cb948c2b", "reasoning": "I wrote this myself for a class assignment and used plain language on purpose."}'
```

```json
{
  "content_id": "8d3ca2c2-01ea-4ec6-af74-03f1cb948c2b",
  "status": "under_review",
  "previous_status": "decided",
  "original_guess": "ai",
  "message": "Your appeal was recorded. A person will review this decision."
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 2,
  "entries": [
    {
      "timestamp": "2026-11-05T00:22:59+00:00",
      "content_id": "8d3ca2c2-01ea-4ec6-af74-03f1cb948c2b",
      "creator_id": "cruz",
      "guess": "ai",
      "model_score": 0.8876,
      "style_score": 0.7275,
      "combined_score": 0.8075,
      "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.",
      "status": "decided"
    },
    {
      "timestamp": "2026-11-05T00:23:11+00:00",
      "content_id": "8d3ca2c2-01ea-4ec6-af74-03f1cb948c2b",
      "creator_id": "cruz",
      "event": "appeal",
      "status": "under_review",
      "reasoning": "I wrote this myself for a class assignment and used plain language on purpose."
    }
  ]
}
```

The original `decided` entry is untouched; the appeal sits after it, which is
the whole point of an append-only log.

---

## How I Used AI

**Moment 1**

- *What I asked for:* a combining rule for `scoring.py::combine_signals` that
  actually implements the false-positive decision from my Milestone 1 trace,
  not just a plain weighted average.
- *What came back:* a rule that averages the two signals when they agree, but
  weights toward whichever one reads more human (0.7/0.3) when they disagree
  by more than 0.15.
- *What I changed:* I picked the 0.15 disagreement threshold and the 0.7/0.3
  split myself after seeing how the calibration inputs scored — and I made
  sure the split case I document (`dense_ai_split`) is one I actually
  verified moves the number the way the rule claims, not a hypothetical.

**Moment 2**

- *What I asked for:* help after `python detector.py` crashed with "the
  paging file is too small" instead of loading gpt2.
- *What came back:* a diagnosis that it was a Windows virtual-memory limit
  (checked with `Get-CimInstance Win32_OperatingSystem`, which showed under
  1.5 GB of virtual memory free against 64 GB total), not a bug in the
  starter, with a list of processes to close to free it.
- *What I changed:* nothing in the code — I closed the processes it pointed
  at and re-ran the same command, which then worked.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 8 per minute, 150 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

A real writer proofreading or revising their own work a few times an hour
never gets near 8 in one minute. A script trying to map my thresholds by
sending a thousand variations hits the wall within a few seconds no matter
how it paces itself, because 8/minute caps it at roughly 480/hour even if it
never pauses. 150/day covers someone submitting fifteen separate short
pieces spread across a whole day with room to spare, while still keeping a
slow, patient drip-attack well under four digits for the day.

**What a caller counts as:** `creator_id`, with the caller's IP address as a
fallback only when the request body isn't a JSON object with a usable
`creator_id` string (`app.py`'s `rate_limit_key`, given in the starter). I
kept this as-is rather than switching to IP-only: per-`creator_id` is right
for this unit's attack set, where `flood_same_creator` deliberately shares
one `creator_id` to test the limiter — but I know it fails differently than
a per-address limit would. One script can claim a fresh `creator_id` on every
request and look like a thousand different callers (my rate limiter would
never catch that), and one household behind a shared address submitting
under their own separate accounts could look like one caller under IP
fallback. Per-`creator_id` assumes `creator_id` costs something to fake,
which it currently doesn't — see What's Still Broken.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 200 200 200 429 429 429 429 429 429 429
```

8 through, 7 rejected — exactly the 8/minute limit, from `results/flood_2026-11-14_2150.md`.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

56 attacks, from `attack_set/attacks.csv` and `attack_set/attacks_malformed_requests.csv`,
all run with `python run_attacks.py --set attack_set --label before`. Full
detail, including every response, is in
`results/attack_run_2026-11-14_2151_before.md`. My verdict rule:

- **`evasion`**: BROKE if the final `guess` is anything other than `ai` —
  every one of these inputs is genuinely AI-written, so landing in "unsure"
  is the evasion partly working, not a wash.
- **`false_positive`**: BROKE only if the final `guess` is `ai` — a real
  accusation. "unsure" carries none ("no action is needed"), so I count it
  as held even though it's not where I'd want these to land.
- **`prompt_injection`**: held automatically unless something attacker-written
  visibly changed the service's behavior — see below.
- **`malformed` / `flood_same_creator`**: held if the request got a clean
  4xx/429/200 with no crash.

| Family | Attacks | Held | Broke |
|---|---|---|---|
| `evasion` | 10 | 2 | **8** |
| `false_positive` | 8 | 2 | **6** |
| `prompt_injection` | 6 | 6 | 0 |
| `malformed` | 20 | 20 | 0 |
| `flood_same_creator` | 12 | 12 | 0 |
| **Total** | **56** | **42** | **14** |

`prompt_injection` held completely for a structural reason, not a clever
defense: neither signal ever runs attacker text through anything that
*generates* or *follows instructions* — gpt2 is only ever used for a forward
pass to compute perplexity, and the style signal is pure arithmetic over
sentence lengths, word sets and punctuation counts. There's no step where
text written as a command can be read as one. I checked every PI0x response
and log entry by hand for any sign the instruction took effect (a changed
label string, something injected into the log); none did.

`malformed` held completely — every deliberately-garbled input got a clean
400 (or a clean 200 in two cases, `MF04`/`MF07`, where the text was
structurally valid even though it wasn't meaningful; see diagnosis below) and
nothing crashed the service.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"combined_score": 0.3249, "content_id": "a5b43925-e0db-4fda-8ca1-05c29867bee5", "creator_id": "attacker_EV01", "guess": "human", "label": "We think this was probably written by a person.", "model_score": 0.1635, "status": "decided", "style_score": 0.7016, "timestamp": "2026-11-15T02:51:30+00:00"}
{"combined_score": 0.6527, "content_id": "c667e3f8-5f9e-47e0-aa0a-e69f651d438d", "creator_id": "attacker_EV04", "guess": "ai", "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.", "model_score": 0.6114, "status": "decided", "style_score": 0.694, "timestamp": "2026-11-15T02:51:30+00:00"}
{"combined_score": 0.7206, "content_id": "9fc900ed-0e60-4354-9f8f-e6ab39ae4391", "creator_id": "attacker_FP02", "guess": "ai", "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.", "model_score": 0.7387, "status": "decided", "style_score": 0.7025, "timestamp": "2026-11-15T02:51:31+00:00"}
{"combined_score": 0.7593, "content_id": "cd514b92-5cf4-4b75-b9fd-ba4fcd6eb368", "creator_id": "attacker_FP05", "guess": "ai", "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.", "model_score": 0.8005, "status": "decided", "style_score": 0.7181, "timestamp": "2026-11-15T02:51:31+00:00"}
{"combined_score": 0.3042, "content_id": "3886850a-93f1-4c06-a0ae-8c6b277195c3", "creator_id": "attacker_PI05", "guess": "human", "label": "We think this was probably written by a person.", "model_score": 0.6401, "status": "decided", "style_score": 0.1602, "timestamp": "2026-11-15T02:51:32+00:00"}
{"combined_score": 0.2936, "content_id": "2dd864cb-b177-4c55-8594-0c6496a62633", "creator_id": "attacker_MF04", "guess": "human", "label": "We think this was probably written by a person.", "model_score": 0.0112, "status": "decided", "style_score": 0.9526, "timestamp": "2026-11-15T02:51:32+00:00"}
{"creator_id": "attacker_MF08", "event": "rejected", "reason": "text_too_long", "status": "rejected", "timestamp": "2026-11-15T02:51:32+00:00"}
{"creator_id": "attacker_RQ01", "event": "rejected", "reason": "missing_text", "status": "rejected", "timestamp": "2026-11-15T02:51:32+00:00"}
{"combined_score": 0.1954, "content_id": "8b1ef864-7e3c-44b1-8e86-40f641b1530c", "creator_id": "attacker_flood", "guess": "human", "label": "We think this was probably written by a person.", "model_score": 0.0287, "status": "decided", "style_score": 0.5843, "timestamp": "2026-11-15T02:51:32+00:00"}
{"creator_id": "attacker_flood", "event": "rejected", "limit": "8 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-15T02:51:33+00:00"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

`FP05` — "technical documentation written by a person" — scored `ai` at
0.759, the single highest-confidence false accusation in the whole run. It
isn't especially plain or especially formal, it's just ordinary professional
writing, and my system was *more confident* it was AI than it was for some of
the attacks deliberately trying to look like AI (`EV09` landed at only
0.553). A real technical writer handed this label would have a solid case
that the system actively works against people doing their job normally.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

Produced by `run_eval.py::main` (criteria 1–3, 5) and `eval_appeal.py::main`
(criterion 4, written by hand — see `scenarios.py`'s note on why). Full
output: `results/run_2026-11-14_2156_before.md` and
`results/appeal_eval.json`. Every trial was identical to the others, which is
expected — nothing in either signal is random.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Human writing almost never AI | ≤1/10 "ai", 0/3 plain pieces "ai" | 1/10 "ai" **(the plain one)** | 1/10 "ai" **(the plain one)** | 1/10 "ai" **(the plain one)** | **MISSED** |
| 2. AI/human score far apart | mean gap ≥0.30, no overlap | gap 0.219, no overlap | gap 0.219, no overlap | gap 0.219, no overlap | **MISSED** |
| 3. All three labels reachable | 3/3 labels, ≥2/3 borderline "unsure" | 3/3 labels, 1/3 borderline unsure | 3/3 labels, 1/3 borderline unsure | 3/3 labels, 1/3 borderline unsure | **MISSED** |
| 4. Appeal always changes status | 5/5 appeals, unknown id → 404 | 5/5, 404 | 5/5, 404 | 5/5, 404 | MET |
| 5. Bad input never crashes | 6/6 → 4xx, 0 → 5xx, all logged | 6/6, 0 | 6/6, 0 | 6/6, 0 | MET |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json
// scenarios.py "my own writing" (criterion 1), run_eval.py::main, trial 1 —
// the first text is plain ("I work on this project after dinner...") and is
// the one that came back "ai":
{
  "status": 200,
  "guess": "ai",
  "confidence": 0.7218,
  "model_score": 0.7669,
  "style_score": 0.6768,
  "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.",
  "sent": "I work on this project after dinner. I open my laptop and read"
}
```

```json
// eval_appeal.py::run_trial, trial 1, one of the five appeals:
{
  "content_id": "…",
  "appeal_status_code": 200,
  "appeal_body": {
    "status": "under_review",
    "previous_status": "decided",
    "original_guess": "human",
    "message": "Your appeal was recorded. A person will review this decision."
  }
}
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

**One pattern covers criteria 1, 2 and 3, and most of the `evasion` and
`false_positive` attack families.** Both of my signals measure *surface
shape* — predictability to signal one, sentence/vocabulary/punctuation
regularity to signal two — and neither reads *content*: specificity, hedging,
whether the writer actually commits to a claim. Casual, plain, or
conversational human writing is surface-regular (common words, even
sentences, light punctuation) in exactly the same way generic AI prose is, so
the two groups don't separate on either signal's own terms. My combining rule
only protects a writer when the two signals *disagree* (Signals and Scoring's
0.7/0.3 rule) — it provides zero protection when both signals share the same
blind spot and agree with each other, which is exactly what happens to plain
writing, since plain writing reads as regular on both axes at once.

- **Criterion 1 — stage: signal one AND signal two, agreeing.** The plain
  piece ("I work on this project after dinner…") scored `model_score=0.7669`
  (common words, short clauses → low perplexity → high AI-likeness) *and*
  `style_score=0.6768` (five short, similarly-sized sentences → low spread;
  no semicolons/dashes → low punctuation density → also high AI-likeness).
  Both signals land on the same side of 0.5, so `combine_signals` takes the
  *agreement* branch and averages — there's no disagreement for my
  human-leaning weighting to even apply to. Mechanism: plain writing is
  AI-like on both axes at once, not just one, so the one safeguard I built
  specifically for this case never activates.

- **Criterion 2 — stage: signal one, mainly.** My "clearly human" paragraphs
  are casual and specific in *content*, but several (e.g. "I don't actually
  like jazz…", `model_score=0.6067`) still use short, common-word sentences,
  which signal one reads as predictable almost as readily as the generic
  marketing-copy "AI" paragraphs (`model_score` 0.58–0.89). Perplexity can't
  see that one text is about a specific jazz solo in a specific shower and
  the other is about "today's fast-paced world" in general — both are just
  sequences of common words to gpt2. Mechanism: casual human writing and
  generic AI writing are both unusually *predictable* in the way signal one
  measures, so the gap between the two groups' means collapses well short of
  my 0.30 target (0.219 observed).

- **Criterion 3 — stage: signal two, mainly.** My three "borderline" texts
  were written to be *semantically* uncertain (hedges like "I could be wrong
  about the general case"), but two of the three (`B1`, `B2`) still had very
  low punctuation density (`style_score` 0.10, 0.27) and fairly even
  sentences, so `combine_signals` read them as clearly human-leaning on both
  axes and landed them at "human," not "unsure." Mechanism: I built
  semantic ambiguity into the text, but neither signal reads semantics, so
  semantic ambiguity alone doesn't produce a borderline *score* — only
  surface ambiguity does, and I hadn't separately engineered that in.

- **Criteria 4 and 5 held because neither depends on either signal.** The
  appeal path is pure bookkeeping (`audit.entries_for` + `audit.log_appeal`),
  and bad-input handling runs entirely in `_validate_submission` before
  either signal is ever called. Nothing in this unit's run exercised a
  mechanism those two criteria could fail on, which is itself informative:
  my two cleanly-met criteria are exactly the two that don't touch the part
  of the system that's actually unreliable.

- **Attack set, `evasion` family (8 of 10 broke) — two different
  mechanisms, both ending at "human."** `EV02`, `EV03`, `EV05` broke
  sentences apart, pasted a quotation, or ran a heavy edit pass, and all
  three landed with *both* signals reading human-leaning (`style_score`
  0.13, 0.18, 0.26 — low spread/punctuation reads as human on my scale) —
  these are plain agreement-branch misses, the same mechanism as criterion 1.
  `EV01` ("typos raise word variety") is different and more interesting: it
  split the two signals (`model_score=0.16`, `style_score=0.70`) — the
  typos fooled signal *one* far more than they moved signal two, because
  misspelled words are exactly the kind of "surprising" token gpt2 wasn't
  expecting, which lowers perplexity-based AI-likeness. My disagreement rule
  then weighted toward the human-leaning signal (model) and landed it
  "human" at 0.3249 — the exact split-signal case I designed the rule around
  in Milestone 4, just working against me instead of for me here, because
  the rule can't tell *why* a signal reads human, only that it does. `EV06`
  –`EV09` landed "unsure" rather than "human," which I count as the evasion
  partially working: genuinely AI-written text no longer reads as
  confidently AI.

- **Attack set, `false_positive` family (6 of 8 broke) — the structural
  blind spot, landing exactly where `trace.md` predicted.** `FP02`–`FP07`
  are real human writing in a formal, templated, or carefully-non-native
  register, which reads as unusually regular on both signals the same way
  generic AI prose does, for the same reason as criterion 1 and 2. This is
  the single biggest problem in the whole run, by both count and
  confidence (`FP05` at 0.759 is the worst outcome in the set).

- **`MF04`/`MF07` (malformed, but not rejected) — stage: the route's
  validation, by design, not a bug.** `_validate_submission` only checks
  that `text` is a non-empty string of at least 5 "words" (whitespace-split
  tokens) under 20,000 characters — it has no idea whether those tokens are
  meaningful. Punctuation-only text and right-to-left script both pass that
  check and reach the signals, where `MF07` (RTL script) then scored `ai` at
  0.854 — the *second*-highest confidence in the whole run, and almost
  certainly for the wrong reason: gpt2's tokenizer and training data are
  overwhelmingly English/Latin-script, so non-Latin text is maximally
  "surprising" to it in a way that has nothing to do with authorship. This
  is a blind spot I hadn't named before this run: signal one may be
  systematically unreliable for any writer not writing in English.

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
