# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. Human writing is almost never labelled AI

Of 10 pieces of human writing (at least 5 written by me, and at least 3 written
plainly: short sentences, everyday words), **at most 1** is labelled
high-confidence AI, and **none of the 3 plain pieces** is, in **every one of
three trials**.

**Why this target:** on a writing site a wrong accusation costs the writer far
more than a missed detection costs the site, and plainly written human text is
exactly what signal one is most likely to accuse (see `trace.md`). One in ten
is already a lot of people; I would rather miss AI text than let the plain
writers carry the error.

---

## 2. Clearly-AI and clearly-human text score far apart

Across 5 clearly AI-generated pieces and 5 clearly human pieces, the mean
`confidence` of the AI pieces is **at least 0.30 higher** than the mean of the
human pieces, and **no human piece scores above the lowest-scoring AI piece**,
in every one of three trials.

**Why this target:** a gap of 0.30 is roughly one whole label band on my scale.
If the two easiest groups don't land a band apart, the score is not telling a
reader anything, and the harder cases (edited AI, plain human) have no room to
fall into "unsure" between them.

---

## 3. All three labels are reachable

From a fixed set of 9 inputs chosen to span the range (3 I expect to read as
AI, 3 as human, 3 borderline), **each of the three labels appears at least
once**, and **at least 2 of the 3 borderline inputs** land in "unsure", in
every one of three trials.

**Why this target:** a label no score can reach is a gap in the ranges, and a
service that never says "unsure" is pretending to a certainty it doesn't
have. Borderline text is the case "unsure" exists for, so most of it should
end up there.

---

## 4. Every appeal changes status and is recorded

For 5 appeals sent against real `content_id`s from earlier submissions,
**5 of 5** return `200` with `status: "under_review"`, and for each one
`GET /log` shows the original `decided` entry still unchanged **followed by**
an `appeal` entry carrying the writer's reasoning. An appeal against a made-up
`content_id` returns `404` and adds **no** `under_review` entry.

**Why this target:** the appeal is the only thing between a wrong label and the
writer. One lost appeal in five is one writer silently ignored, so anything
below 5 of 5 is a failure. The made-up id matters because an appeal that
"succeeds" against nothing tells the writer they were heard when they weren't.

---

## 5. Bad input is refused, never crashes, and leaves a trace

For 6 malformed requests to `/submit` (no `text` field, `text` empty, `text`
only whitespace, `text` not a string, `text` over 20,000 characters, body that
is JSON but not an object), **6 of 6** return a `4xx` status with a JSON
`error` field, **0** return a `5xx`, and each one adds a `rejected` entry to
the audit log. `/ping` still answers afterwards.

**Why this target:** a crash on malformed input is one of the most common real
failures there is, and an attack that only shows up as an absence is one I'll
never find. Every bad request should get a clear answer and a log line, with
no exceptions.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
