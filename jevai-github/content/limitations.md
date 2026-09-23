## Known limitations

### Arithmetic and counting

Jev is not a calculator. In the article’s word-count example, it selected the correct count of four but also assigned substantial probability to five. Use ordinary code to count, compare amounts and calculate totals.

### Dates and time

The author’s two simple date tests succeeded, but the [official limitations page](https://docs.typesafe.ai/model-jaggedness/jev-1.13) warns about uneven behavior. Relative dates and mixed formats need careful handling. Resolve and compare dates with deterministic code.

### Extracting arbitrary text

Jev’s candidate-selection interface cannot simply invent an arbitrary email, amount or order identifier as generated text. A useful pattern is to extract candidate spans with code and then ask which one is relevant.

The source’s example contained amounts of 399, 50, 349 and 89 yuan. Code found the amounts first, and the reported judgment selected the relevant 89-yuan amount in 249 ms with confidence 1.0.

### Ambiguous wording

Questions should be direct and consistent with their answer descriptions. Avoid vague terms that conceal a business rule, or a yes/no question where the labels reverse the intended meaning.

### Separate questions are not logical complements

For one duplicate-charge ticket, the article reports 0.56 for a refund-intent question and 0.30 for a separately worded question about wanting something other than a refund. The two values did not sum to one. Independently evaluated questions are not guaranteed to satisfy a logical identity.

### Irrelevant context

Adding unrelated information can degrade judgments. Supply the context needed for the decision, and preserve important qualifiers when filtering it.

### Tasks that should remain in code or a larger model

Do not pay for a fallible model judgment when a deterministic rule already answers the question correctly. Use generative models for writing and substantial multi-step reasoning. A typed output narrows the answer space; it does not make the system infallible.


## Related topics

[Quick overview](/what-is-jev/) · [Getting started](/how-to-use-jev/) · [Examples](/examples/) · [Official TypeSafe resources](/typesafe/)
