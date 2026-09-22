## 1. Define one useful decision

Choose a task with a clear outcome, such as selecting a support team for a ticket. Write down the context the model needs, the allowed answers and what the program should do when none is suitable.

Keep deterministic rules in code. If every partnership request must reach a person, express that as a rule rather than asking the model to infer your policy.

## 2. Get access through TypeSafe

Visit the [official website](https://typesafe.ai/) for current access information and the [TypeSafe console](https://console.typesafe.ai/) to manage credentials. Access availability can change; there is no guaranteed approval time.

Use the [official documentation](https://docs.typesafe.ai/) for the current SDK and API contract. A coding-agent skill can help with implementation, but the skill is separate from model access and usage charges.

Keep API credentials on the server or in your local secret environment. Do not place a key in a public page, repository or browser bundle.

## 3. Describe context and questions

The supplied guide uses a request with `state` and `questions`. Here is an illustrative billing-routing question; confirm the current request contract in the official documentation before integrating it.

```json
{
  "model": "jev-latest",
  "state": {
    "ticket": "My order was charged twice. Please refund the duplicate payment."
  },
  "questions": {
    "department": {
      "type": "choice",
      "instructions": "Which team should handle this ticket?",
      "criteria": {
        "billing": "Payments, refunds and invoices",
        "technical": "Application errors and access problems",
        "sales": "Purchasing and partnerships",
        "other": "No suitable category or not enough information"
      }
    }
  }
}
```

The returned decision is input to your program. It does not itself issue a refund or create an authorization.

## 4. Test before changing behavior

Assemble representative examples, including ambiguous inputs, cases with no match and failures. Decide what the correct result should be before inspecting model output.

Pin a model version when comparing runs. Record the questions, candidate definitions, outputs, latency and usage so that results can be reproduced. Set review thresholds using this evidence, not a universal confidence number.

## 5. Start in observation mode

Keep the existing workflow in charge. Run the new judgment alongside it and compare predictions with actual outcomes. Enable automatic action gradually for low-risk cases that meet your tested criteria.

Handle timeouts, invalid responses and unavailable services explicitly. An error should lead to a safe fallback, not a fabricated answer or a silent success.

## Use a project as a starting point

The [46-project directory](/) groups existing approaches by task. A repository may require a local runtime, credentials and additional services; a listing is not a hosted tool.

For skill routing, separately validate which skills are installed and allowed. For model routing, filter by availability, capability and budget before asking a model to choose.

Continue with the [complete field guide](/guide/) for the source article’s detailed examples and limitations, or open the [TypeSafe resource page](/typesafe/).
