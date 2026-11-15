#!/usr/bin/env python3
"""
Hand-written test for criterion 4 ("every appeal changes status and is
recorded"). ← UNIT 8, MILESTONE 3

`run_eval.py` only ever calls `/submit`; it has no way to take the
content_id one submission returns and feed it into a second call to
`/appeal`. This script does exactly that, three times, and also checks the
one case criterion 4 names explicitly: an appeal against a content_id that
was never submitted.

    python app.py                 # in one terminal
    python eval_appeal.py         # in another, three times or with --trials 3
"""

import argparse
import json

import requests

URL = "http://127.0.0.1:5000"


def run_trial(n):
    results = {"appeals": [], "unknown_id": None}

    for i in range(5):
        sub = requests.post(f"{URL}/submit", json={
            "text": f"Appeal-path check {n}-{i}: a short piece of text, long "
                    f"enough to pass validation, submitted only to produce a "
                    f"real content_id to appeal against.",
            "creator_id": f"eval_appeal_{n}_{i}",
        }, timeout=60).json()
        content_id = sub["content_id"]

        appeal = requests.post(f"{URL}/appeal", json={
            "content_id": content_id,
            "reasoning": "I wrote this myself; please have a person look at it.",
        }, timeout=30)
        results["appeals"].append({
            "content_id": content_id,
            "appeal_status_code": appeal.status_code,
            "appeal_body": appeal.json() if appeal.content else None,
        })

    unknown = requests.post(f"{URL}/appeal", json={
        "content_id": "not-a-real-content-id",
        "reasoning": "testing an id that was never submitted",
    }, timeout=30)
    results["unknown_id"] = {
        "status_code": unknown.status_code,
        "body": unknown.json() if unknown.content else None,
    }
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=3)
    args = parser.parse_args()

    all_trials = []
    for t in range(1, args.trials + 1):
        print(f"\ntrial {t}")
        result = run_trial(t)
        ok = sum(1 for a in result["appeals"] if a["appeal_status_code"] == 200
                 and a["appeal_body"].get("status") == "under_review")
        print(f"  {ok}/5 appeals returned 200 + under_review")
        print(f"  unknown id -> {result['unknown_id']['status_code']}")
        all_trials.append(result)

    with open("results/appeal_eval.json", "w", encoding="utf-8") as f:
        json.dump(all_trials, f, indent=2, ensure_ascii=False)
    print("\nWrote results/appeal_eval.json")


if __name__ == "__main__":
    main()
