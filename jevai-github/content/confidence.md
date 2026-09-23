## Confidence and review thresholds

TypeSafe describes RLCD as reinforcement learning for calibrated decisions. The objective is useful uncertainty, but an individual confidence field must not be read as a blanket guarantee of correctness.

In particular, Choice and Score confidence reflects distribution concentration. It is not interchangeable with “this whole workflow is correct X% of the time.” Measure reliability for your particular questions, candidates and data.

A practical policy can have three outcomes:

- Automatically handle sufficiently reliable, low-risk cases.
- Flag ambiguous cases or request confirmation.
- Use a person, another model or the existing workflow when the decision is unsuitable.

Thresholds depend on observed error rates and the consequences of mistakes. A model score does not replace authorization for a high-impact action.

The original article compares a clear balance inquiry with a vague message about “that money issue from last time.” For the vague message it reports a customer-support probability of 0.88, a transfer probability of 0.12 and confidence of 0.82. This demonstrates ambiguity, not permission to move money.

### The 200-title classification run

The article reports classifying 200 real Chinese AI-news titles into eight categories: new models, product features, papers, business and funding, open-source projects, tutorials, opinions and other.

| Reported metric | Value |
| --- | --- |
| Requests | 10, with concurrency 6 |
| Total time | 11.1 seconds |
| Input tokens | 42,498 |
| Estimated input cost at the article’s price | About $0.001785 |
| Median confidence | 0.78 |
| Items with confidence at least 0.9 | 66 |
| Items with confidence below 0.6 | 63 |
| Items retained for automatic routing at a 0.6 threshold | 137 |

The author’s inspection found that many uncertain titles genuinely crossed categories. A coding-tool release, for example, could be classified as either a feature update or an open-source project.

The report does not provide a complete, independently checked accuracy table for every class. Treat it as an exploratory run, not production validation.

The article also reports small repeated-run changes on an ambiguous bug: scores of 1.50 and 1.44, with confidence 0.25 and 0.34. Leave room for variation when designing thresholds.


## Ask independent questions together

Questions that share the same context and do not depend on one another can be evaluated together. They do not see each other’s answers. If one answer determines which new material to fetch, that dependent step still needs to happen later.

For a synthetic ticket, the article’s author asked four questions: department, refund intent, urgency and whether an order number was present.

| Approach | Reported elapsed time | Input tokens |
| --- | --- | --- |
| Four questions in one request | 274 ms | 603 |
| Four separate requests, run sequentially | 1,111 ms | 1,572 |

This run reduced repeated context and sequential waiting. It is one reported example rather than a universal speed-up ratio. Your own batching strategy should account for request limits, input size and error handling.


## Related topics

[Quick overview](/what-is-jev/) · [Getting started](/how-to-use-jev/) · [Examples](/examples/) · [Official TypeSafe resources](/typesafe/)
