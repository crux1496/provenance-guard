# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-14 22:00
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `caf96a74-6461-424a-a5b6-2908c2cb735e` | human | 0.325 |  BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `5f38418c-8907-47fb-a098-25c8229cb91c` | human | 0.271 |  BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `7202d35d-ca51-4e23-8331-6c42bf68f736` | human | 0.326 |  BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `5f8b8668-bec3-499e-a5ab-aaa45f825372` | unsure | 0.653 |  BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `fe779dfa-e0aa-4c74-a3f5-7ece6597b18a` | human | 0.292 |  BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `086a5e6e-b74e-48c9-bcfb-364bfe4777a5` | unsure | 0.517 |  BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `dd21d10a-4fd9-4cf0-b0ea-2391b9f9fdd4` | unsure | 0.395 |  BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `573b7408-40e4-4a4d-8d3a-09a3229175a1` | unsure | 0.351 |  BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `1dc79a94-3e87-4e74-95f0-90b26bd4beb6` | unsure | 0.553 |  BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `2481895f-b1ce-47ee-b822-358f6ebd0b79` | ai | 0.820 |  HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `f516d1a5-ca0e-4da9-bb47-49184fd28213` | unsure | 0.575 |  HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `d39f2631-767d-43e3-962a-eefb3eb75048` | unsure | 0.721 |  HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `eff58624-c730-47aa-a436-1e778b5fc627` | unsure | 0.710 |  HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `e4692227-5928-46c8-9a28-7a2cba41e7b1` | unsure | 0.709 |  HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `2c5b2a2e-f7f8-43f2-9efe-eca05eff7f1f` | unsure | 0.759 |  HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `cd9b0327-899e-4bf7-af00-3031986cfeb8` | unsure | 0.703 |  HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `2d904925-141e-4384-892f-a3746b9cf36c` | unsure | 0.723 |  HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `3dbec230-f099-4b8d-89f6-81a1ae01a7b5` | unsure | 0.405 |  HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `77e81205-8d9b-431d-8200-b01b46db99d4` | unsure | 0.454 |  HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `ef041c93-8fc3-4d8f-b207-da7ddfa21298` | human | 0.167 |  HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c296c2b9-9ff6-425e-9fad-89f946d0d4e2` | unsure | 0.355 |  HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `882aedae-1b09-4b12-b395-4caa7af4dc6d` | unsure | 0.366 |  HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `5bf31198-8f68-4b9f-b456-2ce58b98f0ee` | human | 0.304 |  HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `f4c13f7c-695a-4b5a-ab42-b30e2497e910` | unsure | 0.548 |  HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  HELD |
| MF04 | malformed | text is only punctuation | 200 | `718bf1c6-0055-4f1f-adc8-8203bbd22193` | human | 0.294 |  HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  HELD |
| MF07 | malformed | text is right-to-left script | 200 | `3c76ad8e-9379-4f19-a2e7-8c7203bbfee3` | ai | 0.854 |  HELD |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ad5eb7ae-363d-4017-8602-0f6eba0d2a00` | human | 0.195 |  HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7cd22a37-330f-4acd-acfe-82bb0c728d72` | human | 0.195 |  HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7bf41707-bbe4-4df4-afd3-cbbe89366f8c` | human | 0.195 |  HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f2f973cd-b045-4704-84fe-93abbd82446d` | human | 0.195 |  HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9601aced-867c-48db-bc4f-7caaa27523ab` | human | 0.195 |  HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `24cb73c6-dd95-49f3-97fd-7765405df073` | human | 0.195 |  HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ffc0f125-ddc0-4c0c-835d-561425c25fe0` | human | 0.195 |  HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `12816b96-a6d7-4cb1-aaf3-b5f9823cdf59` | human | 0.195 |  HELD |
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
  "content_id": "caf96a74-6461-424a-a5b6-2908c2cb735e",
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
  "content_id": "5f38418c-8907-47fb-a098-25c8229cb91c",
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
  "content_id": "7202d35d-ca51-4e23-8331-6c42bf68f736",
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
  "content_id": "5f8b8668-bec3-499e-a5ab-aaa45f825372",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6527,
  "model_score": 0.6114,
  "style_score": 0.694,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "fe779dfa-e0aa-4c74-a3f5-7ece6597b18a",
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
  "content_id": "086a5e6e-b74e-48c9-bcfb-364bfe4777a5",
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
  "content_id": "dd21d10a-4fd9-4cf0-b0ea-2391b9f9fdd4",
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
  "content_id": "573b7408-40e4-4a4d-8d3a-09a3229175a1",
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
  "content_id": "1dc79a94-3e87-4e74-95f0-90b26bd4beb6",
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
  "content_id": "2481895f-b1ce-47ee-b822-358f6ebd0b79",
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
  "content_id": "f516d1a5-ca0e-4da9-bb47-49184fd28213",
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
  "content_id": "d39f2631-767d-43e3-962a-eefb3eb75048",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.7206,
  "model_score": 0.7387,
  "style_score": 0.7025,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "HELD"
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "eff58624-c730-47aa-a436-1e778b5fc627",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.71,
  "model_score": 0.8051,
  "style_score": 0.6149,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "HELD"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "e4692227-5928-46c8-9a28-7a2cba41e7b1",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.7085,
  "model_score": 0.8329,
  "style_score": 0.5841,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "HELD"
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "2c5b2a2e-f7f8-43f2-9efe-eca05eff7f1f",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.7593,
  "model_score": 0.8005,
  "style_score": 0.7181,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "HELD"
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "cd9b0327-899e-4bf7-af00-3031986cfeb8",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.7034,
  "model_score": 0.8814,
  "style_score": 0.5254,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "HELD"
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "2d904925-141e-4384-892f-a3746b9cf36c",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.7228,
  "model_score": 0.8816,
  "style_score": 0.5641,
  "label": "We couldn't tell whether this was written by a person or by AI. That's on us, not on you \u2014 it isn't a judgment about your writing, and no action is needed.",
  "error": null,
  "verdict": "HELD"
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "3dbec230-f099-4b8d-89f6-81a1ae01a7b5",
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
  "content_id": "77e81205-8d9b-431d-8200-b01b46db99d4",
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
  "content_id": "ef041c93-8fc3-4d8f-b207-da7ddfa21298",
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
  "content_id": "c296c2b9-9ff6-425e-9fad-89f946d0d4e2",
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
  "content_id": "882aedae-1b09-4b12-b395-4caa7af4dc6d",
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
  "content_id": "5bf31198-8f68-4b9f-b456-2ce58b98f0ee",
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
  "content_id": "f4c13f7c-695a-4b5a-ab42-b30e2497e910",
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
  "content_id": "718bf1c6-0055-4f1f-adc8-8203bbd22193",
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
  "content_id": "3c76ad8e-9379-4f19-a2e7-8c7203bbfee3",
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
  "content_id": "ad5eb7ae-363d-4017-8602-0f6eba0d2a00",
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
  "content_id": "7cd22a37-330f-4acd-acfe-82bb0c728d72",
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
  "content_id": "7bf41707-bbe4-4df4-afd3-cbbe89366f8c",
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
  "content_id": "f2f973cd-b045-4704-84fe-93abbd82446d",
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
  "content_id": "9601aced-867c-48db-bc4f-7caaa27523ab",
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
  "content_id": "24cb73c6-dd95-49f3-97fd-7765405df073",
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
  "content_id": "ffc0f125-ddc0-4c0c-835d-561425c25fe0",
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
  "content_id": "12816b96-a6d7-4cb1-aaf3-b5f9823cdf59",
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
