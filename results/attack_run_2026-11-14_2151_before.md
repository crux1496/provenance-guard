# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-14 21:51
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

**My verdict rule, applied by hand below** (written in `README.md` too):

- `evasion`: BROKE if the final `guess` is anything other than `ai` — every one
  of these inputs is genuinely AI-written, so "unsure" is the evasion partly
  working, not a wash.
- `false_positive`: BROKE only if the final `guess` is `ai` — a false
  accusation. `unsure` carries no accusation ("no action is needed"), so it
  counts as held even though it's not where I'd want these to land.
- `prompt_injection`: HELD across the board. Neither signal ever runs text
  through a model that follows instructions — gpt2 only scores perplexity,
  it never generates — so there is no step where attacker-written text can
  be read as a command. I checked each response and log entry by hand for
  anything that looks like the injected instruction took effect; none did.
- `malformed` / `flood_same_creator`: HELD if the request got a clean 400 or
  429 with no crash, or a clean 200 with no crash. Two malformed inputs
  (`MF04`, `MF07`) weren't actually rejected — see the diagnosis below.

**Worst outcome:** `FP05` — technical documentation written by a person —
scored `ai` at 0.759, the single highest-confidence false accusation in the
whole set. I would least want to explain this one to the writer: this isn't
a plain or especially formal piece, it's ordinary professional writing, and
my system was more *confident* it was AI than it was for some of the
deliberately-evasive AI text in the `evasion` family (e.g. `EV09` at 0.553).
A real technical writer handed this label would have a strong case that the
system is actively worse than useless for them.

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `a5b43925-e0db-4fda-8ca1-05c29867bee5` | human | 0.325 |  BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `078a03ca-fff0-456a-8fde-0839e4c27fd0` | human | 0.271 |  BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `dc192003-6f26-4ff7-8ed5-aea77cf18f12` | human | 0.326 |  BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c667e3f8-5f9e-47e0-aa0a-e69f651d438d` | ai | 0.653 |  HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c48d59f2-3394-4f6a-af6c-da2e4b229282` | human | 0.292 |  BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `e6ebff47-ae41-4476-b476-84b47f43b97f` | unsure | 0.517 |  BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `1963dd5a-1e86-438d-bc69-e37642fe5691` | unsure | 0.395 |  BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `9404d417-eab1-4f29-8ae1-bce7d2dcd419` | unsure | 0.351 |  BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `b26504e5-152f-4273-ac45-fdc770317fc3` | unsure | 0.553 |  BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `baea3eab-93b7-4cc4-9833-4be07b97ea5d` | ai | 0.820 |  HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `73af924e-806a-4690-a8ce-e277270380ed` | unsure | 0.575 |  HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `9fc900ed-0e60-4354-9f8f-e6ab39ae4391` | ai | 0.721 |  BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `705ba147-309c-42a1-b8e2-098f7df321a4` | ai | 0.710 |  BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `c8de6919-9320-4dc4-b8d9-ced409e41f4b` | ai | 0.709 |  BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `cd514b92-5cf4-4b75-b9fd-ba4fcd6eb368` | ai | 0.759 |  BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `f00d0261-35ab-4b57-89fc-16904ed92a62` | ai | 0.703 |  BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `8646be21-16f9-48fa-a8c2-ef54d48965ba` | ai | 0.723 |  BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `4cf05a1e-c143-43f4-807f-85385c920958` | unsure | 0.405 |  HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `d1e07801-2257-4256-acf1-26c38ad16405` | unsure | 0.454 |  HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `a2af5743-7b54-41a1-8770-cf0419ac5b96` | human | 0.167 |  HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `6254879f-ffee-48ca-8b43-b4ab1cc78ae1` | unsure | 0.355 |  HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `06fab68a-3478-4a5f-8f15-05718f74c81e` | unsure | 0.366 |  HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `3886850a-93f1-4c06-a0ae-8c6b277195c3` | human | 0.304 |  HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `9db3d491-f266-42ed-87d6-7ef4b4aabd49` | unsure | 0.548 |  HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  HELD |
| MF04 | malformed | text is only punctuation | 200 | `2dd864cb-b177-4c55-8594-0c6496a62633` | human | 0.294 |  HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  HELD |
| MF07 | malformed | text is right-to-left script | 200 | `e2335751-a535-4eac-a2d7-e86d45f9645e` | ai | 0.854 |  HELD |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8b1ef864-7e3c-44b1-8e86-40f641b1530c` | human | 0.195 |  HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a81fbad6-0060-4b0e-84d2-ae7c317b5ad4` | human | 0.195 |  HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3c630ea6-8676-44e5-8e8a-5de3473eb681` | human | 0.195 |  HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d20ab885-d2fd-45a2-9066-c668f7336585` | human | 0.195 |  HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bdcbb914-0c62-4d4b-9bcb-e4166a7853dc` | human | 0.195 |  HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e8b9394e-cb2d-4c21-9376-3042b63ab7b6` | human | 0.195 |  HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8c206f5c-3ed7-4d03-99ab-3e40d5728271` | human | 0.195 |  HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3074e766-f48b-4c7a-b271-5bb04765187f` | human | 0.195 |  HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "a5b43925-e0db-4fda-8ca1-05c29867bee5",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3249,
  "model_score": 0.1635,
  "style_score": 0.7016,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "078a03ca-fff0-456a-8fde-0839e4c27fd0",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.2709,
  "model_score": 0.5943,
  "style_score": 0.1323,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "dc192003-6f26-4ff7-8ed5-aea77cf18f12",
  "creator_id": "attacker_EV03",
  "guess": "human",
  "confidence": 0.3257,
  "model_score": 0.6662,
  "style_score": 0.1798,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c667e3f8-5f9e-47e0-aa0a-e69f651d438d",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.6527,
  "model_score": 0.6114,
  "style_score": 0.694,
  "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.",
  "error": null,
  "verdict": "HELD"
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "c48d59f2-3394-4f6a-af6c-da2e4b229282",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2919,
  "model_score": 0.3212,
  "style_score": 0.2627,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "e6ebff47-ae41-4476-b476-84b47f43b97f",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5175,
  "model_score": 0.5727,
  "style_score": 0.4623,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "1963dd5a-1e86-438d-bc69-e37642fe5691",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.3946,
  "model_score": 0.5862,
  "style_score": 0.3125,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "9404d417-eab1-4f29-8ae1-bce7d2dcd419",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3512,
  "model_score": 0.2452,
  "style_score": 0.5985,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "b26504e5-152f-4273-ac45-fdc770317fc3",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5534,
  "model_score": 0.7042,
  "style_score": 0.4888,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "baea3eab-93b7-4cc4-9833-4be07b97ea5d",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8196,
  "model_score": 0.9792,
  "style_score": 0.6599,
  "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.",
  "error": null,
  "verdict": "HELD"
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "73af924e-806a-4690-a8ce-e277270380ed",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5752,
  "model_score": 0.6175,
  "style_score": 0.5329,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "HELD"
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "9fc900ed-0e60-4354-9f8f-e6ab39ae4391",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7206,
  "model_score": 0.7387,
  "style_score": 0.7025,
  "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "705ba147-309c-42a1-b8e2-098f7df321a4",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.71,
  "model_score": 0.8051,
  "style_score": 0.6149,
  "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "c8de6919-9320-4dc4-b8d9-ced409e41f4b",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7085,
  "model_score": 0.8329,
  "style_score": 0.5841,
  "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "cd514b92-5cf4-4b75-b9fd-ba4fcd6eb368",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7593,
  "model_score": 0.8005,
  "style_score": 0.7181,
  "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "f00d0261-35ab-4b57-89fc-16904ed92a62",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7034,
  "model_score": 0.8814,
  "style_score": 0.5254,
  "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "8646be21-16f9-48fa-a8c2-ef54d48965ba",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7228,
  "model_score": 0.8816,
  "style_score": 0.5641,
  "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "4cf05a1e-c143-43f4-807f-85385c920958",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4048,
  "model_score": 0.3223,
  "style_score": 0.4873,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "HELD"
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "d1e07801-2257-4256-acf1-26c38ad16405",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4538,
  "model_score": 0.4625,
  "style_score": 0.4451,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "HELD"
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "a2af5743-7b54-41a1-8770-cf0419ac5b96",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1673,
  "model_score": 0.2044,
  "style_score": 0.1303,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "HELD"
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "6254879f-ffee-48ca-8b43-b4ab1cc78ae1",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.3555,
  "model_score": 0.5943,
  "style_score": 0.2532,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "HELD"
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "06fab68a-3478-4a5f-8f15-05718f74c81e",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.3664,
  "model_score": 0.4998,
  "style_score": 0.233,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "HELD"
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "3886850a-93f1-4c06-a0ae-8c6b277195c3",
  "creator_id": "attacker_PI05",
  "guess": "human",
  "confidence": 0.3042,
  "model_score": 0.6401,
  "style_score": 0.1602,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "HELD"
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "9db3d491-f266-42ed-87d6-7ef4b4aabd49",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5476,
  "model_score": 0.5583,
  "style_score": 0.5369,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "HELD"
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "2dd864cb-b177-4c55-8594-0c6496a62633",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.2936,
  "model_score": 0.0112,
  "style_score": 0.9526,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "HELD"
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "e2335751-a535-4eac-a2d7-e86d45f9645e",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.854,
  "model_score": 0.9064,
  "style_score": 0.8017,
  "label": "We think this was most likely written by AI. This is not certain, and you can appeal if you believe it's wrong.",
  "error": null,
  "verdict": "HELD"
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "8b1ef864-7e3c-44b1-8e86-40f641b1530c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1954,
  "model_score": 0.0287,
  "style_score": 0.5843,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "a81fbad6-0060-4b0e-84d2-ae7c317b5ad4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1954,
  "model_score": 0.0287,
  "style_score": 0.5843,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "3c630ea6-8676-44e5-8e8a-5de3473eb681",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1954,
  "model_score": 0.0287,
  "style_score": 0.5843,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "d20ab885-d2fd-45a2-9066-c668f7336585",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1954,
  "model_score": 0.0287,
  "style_score": 0.5843,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "bdcbb914-0c62-4d4b-9bcb-e4166a7853dc",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1954,
  "model_score": 0.0287,
  "style_score": 0.5843,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "e8b9394e-cb2d-4c21-9376-3042b63ab7b6",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1954,
  "model_score": 0.0287,
  "style_score": 0.5843,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "8c206f5c-3ed7-4d03-99ab-3e40d5728271",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1954,
  "model_score": 0.0287,
  "style_score": 0.5843,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "3074e766-f48b-4c7a-b271-5bb04765187f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.1954,
  "model_score": 0.0287,
  "style_score": 0.5843,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```
