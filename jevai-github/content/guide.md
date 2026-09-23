<p class="article-note">English adaptation of the Chinese guide “Jev 使用指南：只做判断、不写字的 AI 模型怎么用、用在哪,” supplied for this website. The measurements below are reported by that article’s author or by the named project, not independently reproduced by Jev Directory. English translations of Chinese test inputs are for reading; the reported numbers belong to the original tests.</p>

## What Jev does

Most familiar language models spend their time generating: a reply, a few lines of code, a summary. TypeSafe AI’s first model, Jev, focuses on a different job—making a judgment among defined possibilities.

You provide context and focused questions. The response contains typed values and the probabilities or confidence information appropriate to the question type. Your program uses those values to choose its next step.

Think of the difference between an exact rule and a semantic judgment. Code can check whether an order exceeds $100 or whether a status equals “paid.” It needs more help when the question is whether a message sounds angry, whether a comment is advertising, or which visible button best fits a task.

Jev can supply that judgment inside a program. The workflow still belongs to the code. In an agent loop, a larger model may handle planning and writing, tools perform actions, and Jev evaluates small decisions such as selecting a model or identifying a relevant tool result.

The practical building blocks are:

- Bounded semantic judgments for classification, routing and action selection.
- Probabilities and confidence information that code can use to request review.
- Focused decisions that may avoid unnecessary text generation.
- Natural-language criteria for relevance, intent, risk or quality.
- Integration through ordinary code, with coding-agent skills available to help implement the API.

## Why System One, and why Jev?

TypeSafe calls this class a System One model, borrowing from Daniel Kahneman’s distinction between fast, intuitive thinking and slower, deliberate reasoning. Spotting an angry face is a useful illustration of the first; working through a difficult calculation illustrates the second.

This is a way to describe the model’s intended role. It does not make it a replacement for a reasoning model or a calculator.

The name Jev refers to William Stanley Jevons and the idea commonly called the Jevons paradox. As a resource becomes cheaper to use, more uses can emerge and total demand may grow. TypeSafe applies that intuition to intelligence: lower-cost judgments could become practical at many more points inside software.

The naming and model framing are explained in [TypeSafe’s launch announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev).

## Getting access and asking a coding agent

The original guide proposes four steps:

1. Visit [TypeSafe AI](https://typesafe.ai/) for current access information. The article described an early-access waitlist; approval times are not guaranteed.
2. Install the TypeSafe skill in your coding agent using the currently documented instructions.
3. Create an API key in the [TypeSafe console](https://console.typesafe.ai/).
4. Ask the coding agent to use the TypeSafe skill and describe your task in plain language.

The commands below are reproduced from the supplied article. Check the official instructions for changes before using them.

```sh
npx skills add typesafe-ai/skills --skill typesafe-ai
```

The article also gives a Claude Code plugin alternative:

```sh
claude plugin marketplace add typesafe-ai/skills
claude plugin install typesafe@typesafe-ai
```

Credentials should come from an environment variable or a secret store, not a public prompt, repository or client-side script. Installing a skill does not itself grant API access.

## A complete comment-triage example

The article’s author started Claude Code in a directory containing `comments.txt`, with eight synthetic comments written for the demonstration. The translated instruction was:

> Use the TypeSafe skill. Write a Python script named triage.py that reads comments.txt, one comment per line. Use Jev to classify each comment as a question, partnership, advertising, praise, complaint or other. Also judge whether I need to reply personally. Mark classifications below 0.6 confidence for manual review. Run the script on comments.txt and print a table. The API key is already in TYPESAFE_API_KEY. Work only in this directory.

The article reports that the agent wrote a 72-line Python script and ran it. The table below translates the original Chinese inputs and preserves the reported output values.

| Input, translated | Category | Confidence | Personal reply |
| --- | --- | --- | --- |
| Is there a Chinese version? I got an error at step three. | Question | 1.00 | Yes, 0.89 |
| Add me for an AI side-hustle course. Earn thousands daily! | Advertising | 1.00 | No, 0.05 |
| We are an AI education company interested in a sponsored collaboration. | Partnership | 1.00 | No, 0.38 |
| Great article. Bookmarked! | Praise | 1.00 | No, 0.06 |
| Another sponsored post. Boring. | Complaint | 1.00 | No, 0.09 |
| Can the model you mentioned be used commercially? | Question | 1.00 | Yes, 0.82 |
| Such amazing service. Nobody has replied for three days. | Complaint | 1.00 | Yes, 0.58 |
| Could you make a tutorial on automation with Codex? | Question | 1.00 | No, 0.41 |

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

## Three question types

### Noul: evaluate a truth statement

Noul returns a value from 0 to 1 for whether a statement holds. A value near 0.5 indicates uncertainty about the statement, not a medium amount of a quality.

The article illustrates this with a synthetic resume. “Is this person strong at Python?” returned 0.19, but the wording was too vague to support a useful action. Two more concrete questions were more informative:

- Does the resume mention using Python at work? Reported probability: 0.04.
- Does it mention building anything with Python? Reported probability: 0.99, because it described a personal web scraper.

The example is about question design. These signals alone are not a hiring decision, and a missing statement in a resume is not proof that a person lacks a skill.

### Choice: select one candidate

Choice selects from a finite, unordered set. The article describes a limit of 255 candidates for the version it covered. It returns a selected candidate, a probability distribution and confidence information.

Provide a suitable “other,” “no match” or review route. Otherwise an input that fits none of the candidates may still be forced into one of them.

The author also tested Chinese questions. An example about the app crashing on its payment screen was assigned to technical support with reported confidence 1.0. One successful example does not establish multilingual quality; evaluate your own language and domain.

### Score: use an ordered rubric

Score evaluates levels with a meaningful order. The supplied guide describes two to ten levels for the version it covered, with a probability-weighted score and a distribution over levels.

Write concrete criteria rather than vague adjectives. The article’s synthetic bug report said that export failed in Safari, worked in Chrome, and affected a customer base where roughly one third used only Safari.

With “minor / moderate / severe” as the rubric, the reported score was 1.94 with confidence 0.91. With specific definitions—cosmetic only, impaired but with a workaround, or blocked with no workaround—the score was 1.48 and confidence 0.28. Probabilities were split between the middle level, 0.52, and the highest level, 0.48.

That uncertainty is understandable: switching browsers is a workaround for some users but may not be acceptable for others. A clearer rubric made the disagreement visible.

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

Include preprocessing, retries, fallback model calls and human review. Try the [interactive arithmetic example](/why-jev/#where-the-savings-can-come-from) to explore your own assumptions.

## Public demos and community projects

### Wikiracing

The official demonstration chooses links between Wikipedia pages. The article describes a run from “Baseball” to “Sun,” with Jev taking three steps in 0.419 seconds at 0.047 US cents. It reports 3.724 seconds and 3.310 US cents for a compared Claude run, and 9.453 seconds for a GPT run that also selected a nonexistent link.

The vendor’s comparison used non-reasoning modes for the larger models. Enabling reasoning could change outcomes. The demonstration illustrates bounded navigation choices; it does not establish broad superiority.

### Doom

The game state is represented as text—weapon information, enemy distance and direction—rather than supplied directly as images. Jev evaluates decisions such as firing, prioritizing health and choosing a direction, at roughly ten calls per second in the described demo.

The article quotes an estimate of around $7 per hour. It also notes the vendor’s point that a conventional game bot could perform better. This is an illustration of connecting instructions to game decisions.

### Email triage

Ryan Vogel’s [email-triage demonstration](https://x.com/ryanvogel/status/2100042788851101842) evaluates category, priority, spam and whether a reply is needed. The source article describes a test on roughly 1,500 real emails; its video caption shows a queue of 1,701, with 1,534 processed at the captured moment. These are different snapshots, not a consistent benchmark sample size.

The displayed run used eight concurrent calls, with a reported 193 ms average per email and roughly 40 messages per second. These figures describe that demonstration and are not a service guarantee.

### Browser automation

Kyle Jeong’s [Browserbase and Stagehand demonstration](https://x.com/kylejeong/status/2100622054945095934) represents page structure as context and available actions as candidates. Jev chooses the next action; Stagehand performs it.

The task described in the article signs into a test store, adds headlights to a cart, opens the cart and stops before checkout. On uncertain steps, the system observes the page again rather than forcing an action. The post’s reported task cost was $0.001; that is a claim about that run.

The article also mentions early flight-booking and browser-tool demonstrations. Such examples suggest useful experiments, but their timing and social engagement are not substitutes for a reproducible benchmark.

Browse the directory’s [browser and web category](/?category=browser#directory) for the associated repositories, including jev-ultrafast, Jev Browser and public-browser.

### A trading experiment

Jarrod Watts’s [Jev Trader demonstration](https://x.com/jarrodwatts/status/2100356151468585346) explores buy-or-sell judgments at block intervals on Monad. The supplied article notes a distinction between the post’s discussion of real trading and a video interface labeled “dry run.”

The video’s reported average call time was around 100 ms, with occasional missed blocks. This illustrates scheduling and latency. It is not evidence that the strategy earns money, and model speed does not establish financial expertise.

### TypeSafe Typewriter

The [Typewriter demo](https://typesafe-demo.val.run/) evaluates text as it is typed. The article describes 16 questions covering writing patterns, sarcasm, likely reactions, tone, urgency and factual claims, with one shown call taking 318 ms.

The interface is useful for seeing independent judgments update together. Its visible signals should not be treated as objective measurements of writing quality.

### LangChain integration

The article describes `langchain-typesafe` and middleware patterns for model routing and tool-risk checks. The idea is to put a focused judgment inside an agent’s observe–decide–act loop rather than asking a generative model to handle every small decision.

Read [LangChain’s own integration article](https://www.langchain.com/blog/building-a-harness-with-jev) for its current implementation and interfaces.

### The Jev project directory

The directory accompanying this guide organizes source links by use case. These include model and skill routing, guardrails, code review, browser tools, content checks, office workflows, context management, experiments, evaluation and independent model implementations.

It includes repositories, posts and demonstrations—not a collection of hosted applications. Independent models are not official Jev weights. Inclusion does not imply endorsement, tested functionality or a security audit.

[Explore the project directory](/#directory), or begin with [model and skill routing](/?category=route#directory) and [context management](/?category=context#directory).

## More worked examples from the source article

The following examples preserve the source author’s distinction between real article data and synthetic inputs. They have not been rerun for this website.

### Detecting clickbait in real news titles

The author submitted 30 Chinese titles, many translated from English, with two questions per title: a rubric-based clickbait score and whether specific names, numbers or facts were present. The article reports 60 questions in one request, 1.2 seconds and 4,923 input tokens.

A highly charged title about AI, crime and elites scored 1.67, with a concrete-facts probability of 0.13. An introductory AIOps title scored 0.04 with confidence 0.94. A title explaining model-quantization formats scored 0.19, with a concrete-facts probability of 0.95.

A title about a security test was ambiguous: its reported score was 1.21, with almost no confidence. The proposed application was to flag strongly sensational, fact-poor titles while leaving the middle ground for review. The thresholds are examples, not generally validated rules.

### Checking whether a summary is supported

The author used a real news summary as context and wrote four test claims: two supported, one exaggerated and one absent from the source. Each claim had three options: supported, contradicted or not mentioned.

The article reports one 293 ms request. A claim about a one-million-token context window was supported; a claim of more than 50% improvement contradicted the source’s more-than-25% figure; a claim about open weights was not mentioned; and a claim about video input was supported. Reported confidence was 1.0 for each.

The pattern is useful: a generative model drafts, a separate judgment checks support, and uncertain or unsupported statements are reviewed. Checking agreement with a source does not verify that the source itself is true.

### Understanding sarcasm

Three synthetic inputs were assessed for sarcasm, satisfaction and emotional intensity. Translations of the inputs and reported probabilities:

| Input | Sarcasm | Satisfaction |
| --- | --- | --- |
| Amazing service. Nobody has replied for three days. | 0.96 | 0.03 |
| Support solved it in ten minutes. Really great service. | 0.08 | 0.97 |
| Tracking says delivered, but I have not received the parcel. | 0.04 | 0.07 |

The first example shows why a positive keyword alone is insufficient. Three examples remain a small demonstration, not an accuracy study.

### Finding the final agreed meeting time

A synthetic conversation proposed Wednesday, then Thursday, and finally agreed on Friday at 15:00 using Tencent Meeting. Code first collected the candidate times and included a “not agreed” option.

The article reports selecting Friday at 15:00 in 281 ms with confidence 1.0, and selecting the meeting tool with confidence 1.0. Calendar arithmetic, time zones and writing the event remain the responsibility of code and authorized tools.

### Reviewing command risk

The author submitted six example commands for classification as read-only, reversible or irreversible, reporting a 306 ms request. `ls -la` and `git status` were classified as read-only. Removing `node_modules` was treated as reversible; force-pushing a branch, running a remote shell script and dropping a database table were classified as irreversible.

These labels are coarse. Risk depends on actual paths, privileges, environment, backups and what a remote script does. Do not treat this small experiment as a command-authorization system. Use established permission boundaries and review controls independently of the model.

A sensible first integration observes and logs predicted risk before it is allowed to affect execution.

### Scoring editorial choices by dimension

Instead of asking for one overall score, the article’s author separated an editorial decision into whether an item contained an explainable mechanism, whether readers could use it immediately, and whether it was purely fundraising news.

Code applied a rule to exclude pure-funding items, then combined the other two dimensions. Four examples showed why the rule mattered: a data-center financing item had enough technical language to score well on mechanism, but still needed to be removed under the editorial policy.

Separating questions makes the weighting visible. If the underlying scores remain applicable, code can change weights without making another model call.

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

## A gradual integration plan

1. Keep the current rules and workflow in place.
2. Run Jev alongside them and record predictions without changing behavior.
3. Evaluate representative labeled cases, including ambiguities and failures.
4. Select review thresholds based on observed errors and their consequences.
5. Enable automation for a narrow set of low-risk cases.
6. Monitor fallback rates, cost, latency and drift when models or data change.

The source article suggests starting with one small judgment that is currently handled by a brittle rule or regular expression. A week of side-by-side observation can reveal more than a polished demo, but the amount of evidence needed depends on traffic, variety and risk.

A small initial set of labeled examples can help find obvious problems. It is not enough on its own to establish production reliability.

## Continue exploring

- [Find a project in the directory](/).
- [Understand why and when to use Jev](/why-jev/).
- [Follow the getting-started guide](/how-to-use-jev/).
- [Open official documentation and additional sources](/typesafe/).
