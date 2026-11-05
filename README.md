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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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
