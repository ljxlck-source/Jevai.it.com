## A complete comment-triage example

The article’s author started Claude Code in a directory containing `comments.txt`, with eight synthetic comments written for the demonstration. The translated instruction was:

> Use the TypeSafe skill. Write a Python script named triage.py that reads comments.txt, one comment per line. Use Jev to classify each comment as a question, partnership, advertising, praise, complaint or other. Also judge whether I need to reply personally. Mark classifications below 0.6 confidence for manual review. Run the script on comments.txt and print a table. The API key is already in TYPESAFE_API_KEY. Work only in this directory.

The article reports that the agent wrote a 72-line Python script and ran it. The table below translates the original Chinese inputs and preserves the reported output values.

| Input, translated | Category | Confidence | Personal reply | Status |
| --- | --- | --- | --- | --- |
| Is there a Chinese version? I got an error at step three. | Question | 1.00 | Yes, 0.89 | Automatic |
| Add me for an AI side-hustle course. Earn thousands daily! | Advertising | 1.00 | No, 0.05 | Automatic |
| We are an AI education company interested in a sponsored collaboration. | Partnership | 1.00 | No, 0.38 | Automatic |
| Great article. Bookmarked! | Praise | 1.00 | No, 0.06 | Automatic |
| Another sponsored post. Boring. | Complaint | 1.00 | No, 0.09 | Automatic |
| Can the model you mentioned be used commercially? | Question | 1.00 | Yes, 0.82 | Automatic |
| Such amazing service. Nobody has replied for three days. | Complaint | 1.00 | Yes, 0.58 | Automatic |
| Could you make a tutorial on automation with Codex? | Question | 1.00 | No, 0.41 | Automatic |

The classification review path was not exercised: every classification was above the chosen threshold. The reply decision also exposed an important mismatch. A partnership inquiry and a tutorial request were both marked as not requiring a reply, which the author’s agent considered inappropriate.

That is the useful lesson from this example. If partnerships must always receive a personal response, make that an explicit business rule. A model should not have to infer an unwritten policy. High classification confidence also says nothing by itself about a separate reply decision.

## Anatomy of a request

The article describes requests in terms of `state`, the material to inspect, and `questions`, the decisions to evaluate. This translated example uses a duplicate-payment support ticket:

```json
{
  "model": "jev-latest",
  "state": {
    "ticket": "My headphones order was charged twice. Please refund the duplicate payment."
  },
  "questions": {
    "department": {
      "type": "choice",
      "instructions": "Which team should handle the ticket?",
      "criteria": {
        "billing": "Charges, refunds, invoices and payment issues",
        "technical": "Application failures, crashes or access problems",
        "sales": "Quotes, bulk orders and business partnerships",
        "other": "None of these categories, or not enough information"
      }
    }
  }
}
```

The source reports this answer for its original Chinese ticket:

```json
{
  "model": "jev-1.13.0",
  "answers": {
    "department": {
      "type": "choice",
      "choice": "billing",
      "confidence": 1.0,
      "probabilities": {
        "billing": 1.0,
        "technical": 0.0,
        "sales": 0.0,
        "other": 0.0
      }
    }
  }
}
```

The output is constrained to a defined structure and candidate set. That prevents an arbitrary invented option, but it does not prevent choosing the wrong valid option. The response does not issue a refund; code must decide what actions are permitted.

Confirm the current contract in the [official API documentation](https://docs.typesafe.ai/) when implementing a request.


## Ask independent questions together

Questions about the same state can be evaluated together. Each is assessed independently; one answer does not become evidence for another question in the same call. Your code combines the results and applies business rules.

[Explore more worked examples](/use-cases/) or [learn the three question types](/question-types/).
