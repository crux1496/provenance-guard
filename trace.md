# Milestone 1 — tracing a submission before building one

Written before any of `/submit`, `/appeal`, `stylometry.py` or `scoring.py`
existed. This is the contract the rest of the build has to keep.

## The path a piece of text takes

1. **The writer's site sends a request.** `POST /submit` with JSON
   `{"text": ..., "creator_id": ...}`. Nothing has been judged yet.
2. **The route checks the input** (`app.py::submit`). Is the body a JSON
   object? Is `text` a string with real words in it, and not enormous? Is
   `creator_id` a non-empty string? If not, the request stops here with a
   `400` and a plain error, and the refusal is written to the log as a
   `rejected` entry. Adds: a guarantee that everything below gets clean input.
3. **The route gives the submission an identity.** A fresh `content_id`
   (a UUID). Adds: the handle the writer needs later to appeal.
4. **Signal one reads the text** (`detector.py::model_signal`). gpt2, running
   locally, measures how predictable the text is. Adds: `model_score`, 0–1,
   higher = more AI-like.
5. **Signal two measures the text as text** (`stylometry.py::style_signal`).
   Sentence-length spread, word variety, punctuation. No model, no meaning.
   Adds: `style_score`, 0–1, higher = more AI-like.
6. **The combining rule makes one number** (`scoring.py::combine_signals`).
   Adds: `combined_score`, which is what the response calls `confidence`.
7. **The label mapping turns the number into words** (`scoring.py::score_to_label`).
   Adds: `guess` (`ai` / `unsure` / `human`) and the sentence a reader sees.
8. **The decision is logged, then returned.** `audit.log_decision` writes all
   nine fields to `logs/audit.jsonl` with status `decided`; the same fields go
   back to the caller.

The appeal path is a second, shorter trip: `POST /appeal` → does this
`content_id` exist in the log? → append an `appeal` entry with the writer's
reasoning and status `under_review` → confirm. The original decision is never
edited; the appeal sits after it.

## The two signals

### Signal one — the model signal (`detector.py`)

- **Measures:** perplexity under gpt2, i.e. how surprised a language model is
  by each next word, squashed onto 0–1 so that *low* surprise scores *high*.
- **Why it might differ:** a model writes by picking likely next words, so its
  own output is the kind of text a model finds easy to predict. People pick
  odd, specific words more often.
- **What it can't see:** who wrote it. Predictability is a property of the
  vocabulary and sentence shape, not of the author. Someone writing plainly on
  purpose, a younger writer, or someone writing in a second language and
  sticking to words they are sure of all produce predictable text, and gpt2
  scores them as machine-like. The reverse also holds: AI text prompted to use
  rare or ornate words reads as human. It also only looks at the first 400
  tokens.

### Signal two — the style signal (`stylometry.py`)

- **Measures:** the shape of the text. How much sentence lengths vary
  (spread / mean), how much of the vocabulary is new rather than repeated
  (type-token ratio, made length-fair), and how much "interesting"
  punctuation (commas, semicolons, dashes, colons, brackets, question and
  exclamation marks) appears per word.
- **Why it might differ:** generated prose tends toward even, mid-length
  sentences, a safe vocabulary and tidy, regular punctuation. Human writing is
  lumpier: a three-word sentence next to a forty-word one, a dash, an aside.
- **What it can't see:** anything the text says. It cannot read. Typos, chopping
  a sentence in two, adding a stray dash or a pasted quotation all move it
  without changing a single idea. That makes it very cheap to game on
  purpose, and it can't tell a list or a poem (deliberately even lines) from
  a machine.

## Tracing the false positive

Maya writes a short personal essay in plain English. It is her second
language, so she uses words she is sure of and keeps sentences short and
regular.

- **Signal one** finds her text very predictable: `model_score` comes out
  high, maybe 0.75.
- **Signal two** sees even sentence lengths and few commas or dashes:
  `style_score` is also on the AI side, maybe 0.6.
- **The combining rule** has two signals agreeing, so her combined score lands
  around 0.68. With an AI threshold at 0.65 she would be labelled
  high-confidence AI.
- **What the label says to her:** whatever the AI label says. If it says
  "this was written by AI" she has been accused of cheating by a sentence she
  can't argue with.
- **What she can do:** appeal with her `content_id` and her reasoning. The
  item moves to `under_review` and a person looks at it. That is all she has.

What this trace decides:

1. The AI threshold has to sit **high**, so that two signals that merely lean
   AI land in "unsure", not "AI". Only text both signals are fairly sure of
   should get the AI label.
2. The AI label must say *we think*, not *this is*, and must tell her the
   appeal exists in the same breath.
3. The "unsure" label will be the one most real writers see. It cannot read
   like an accusation.
4. The appeal must always work and always be recorded, because it is the only
   thing between Maya and a wrong label.

## The endpoint contract

### `POST /submit`

Request:

| Field | Type | Required | Rule |
|---|---|---|---|
| `text` | string | yes | at least 5 words after trimming; at most 20,000 characters |
| `creator_id` | string | yes | non-empty after trimming |

`200` response:

| Field | Type | What it is |
|---|---|---|
| `content_id` | string | UUID for this submission; what `/appeal` needs |
| `creator_id` | string | echoed back |
| `guess` | string | `"ai"`, `"unsure"` or `"human"` |
| `confidence` | float 0–1 | the combined score: 0 = confidently human, 1 = confidently AI |
| `label` | string | the full sentence a reader sees |
| `model_score` | float 0–1 | signal one, higher = more AI-like |
| `style_score` | float 0–1 | signal two, higher = more AI-like |
| `combined_score` | float 0–1 | same number as `confidence`, under its log name |
| `status` | string | `"decided"` |

`400` response (bad input): `{"error": "<code>", "message": "<plain sentence>"}`
with codes `invalid_json`, `missing_text`, `text_not_string`, `empty_text`,
`text_too_short`, `text_too_long`, `missing_creator_id`.

`503` response if the detector model can't load:
`{"error": "detector_unavailable", "message": ...}`.

### `POST /appeal`

Request:

| Field | Type | Required | Rule |
|---|---|---|---|
| `content_id` | string | yes | must match a submission in the log |
| `reasoning` | string | yes | non-empty after trimming; at most 5,000 characters |

`200` response:

| Field | Type | What it is |
|---|---|---|
| `content_id` | string | echoed back |
| `status` | string | `"under_review"` |
| `previous_status` | string | what it was before (normally `"decided"`) |
| `original_guess` | string | the decision being appealed |
| `message` | string | plain confirmation to the writer |

`400` for missing or empty fields, `404` with `{"error": "unknown_content_id"}`
when the id isn't in the log.
