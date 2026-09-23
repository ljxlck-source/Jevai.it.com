## Speed, cost and quality

The supplied article cites launch pricing of $0.042 per million input tokens, with no output-token charge, and a published 70–500 ms response-time range. Check [TypeSafe’s current information](https://typesafe.ai/) before budgeting.

The author reports requests from mainland China taking about 0.25–0.58 seconds. Network location, payload and workload affect end-to-end time.

A vendor demonstration described in the article compared 27 judgments: Jev completed the demonstrated run in 0.114 seconds at an estimated $0.000081, while the compared GPT-5.6 Terra run took 8.566 seconds at $0.013880. One judgment differed between them, and the short, dense inputs suited Jev. These are reported demonstration figures, not an all-task comparison.

The article also describes four workflow evaluations where Jev’s agreement with reference judgments was around 68%, compared with roughly 74% and 73% for the other named models. The reference answers came from models; agreement is not equivalent to objectively measured truth. The useful trade-off is whether a cheaper judgment is good enough for a particular branch, with review or fallback when needed.

<div class="media-source">Original charts and demonstrations: <a href="https://typesafe.ai/blog/introducing-system-one-models-and-jev" rel="noopener noreferrer">view the TypeSafe announcement and its evaluation context ↗</a></div>

### Estimate savings across the whole workflow

The article attributes a useful budgeting approximation to technical author Flavio Copes:

```text
Overall savings share
≈ decision-call share of spending × savings on those calls
```

If $6,000 of a $10,000 monthly bill goes to classification, routing and preliminary checks, reducing that part by 95% yields an illustrative $5,700 saving. If most spending goes to long-form generation and decisions account for only 10%, the opportunity is much smaller.

Include preprocessing, retries, fallback model calls and human review. Use your own billing data to test these assumptions.


## Related topics

[Quick overview](/what-is-jev/) · [Getting started](/how-to-use-jev/) · [Examples](/examples/) · [Official TypeSafe resources](/typesafe/)
