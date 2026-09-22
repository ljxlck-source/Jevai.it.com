## A model for decisions inside software

Jev is TypeSafe AI’s first System One model. It evaluates supplied context against focused questions and returns typed decisions: a choice, a score or a probability. The surrounding program decides what happens next.

A useful example is a support ticket. Your application supplies the ticket and the possible destinations—billing, technical support, sales or other. Jev evaluates those candidates. Your code routes the ticket, or sends an uncertain result for review.

This directory is an independent guide to that ecosystem. The model and its official services belong to [TypeSafe AI](https://typesafe.ai/).

## Three building blocks

| Primitive | What you define | What you use it for |
| --- | --- | --- |
| Choice | A finite set of candidates | Select a department, model, skill or action |
| Score | An ordered rubric with meaningful levels | Evaluate urgency, relevance or quality |
| Noul | A clear truth statement | Judge whether a condition holds |

These are constrained output shapes. A valid shape does not guarantee a correct judgment. A probability or confidence field needs to be understood in the context of its question type and evaluated on representative tasks.

Read the [worked examples in the full guide](/guide/#three-question-types) for a closer look at each primitive.

## Why the name System One?

TypeSafe’s terminology borrows the distinction between fast, intuitive System 1 thinking and deliberate System 2 reasoning from Daniel Kahneman’s *Thinking, Fast and Slow*. It is a product framing for fast judgments, not proof that the model reproduces human cognition.

Jev is named after the economist William Stanley Jevons. The idea behind the name is that lower-cost intelligence could make new kinds of software automation practical. See the [original announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev).

## Where a generative model still belongs

Use a generative model to write explanations, draft text, produce code or carry out open-ended reasoning. Use ordinary code for exact arithmetic, dates, permissions and deterministic business rules. Consider Jev for the semantic judgments between those steps.

An agent might use a larger model to plan a task, Jev to choose among known tools, and code to check permissions and execute the selected action. The choice itself is not permission to act.

## Explore a real use case

- [Model and skill routing](/?category=route#directory): select an appropriate candidate for a task.
- [Context management](/?category=context#directory): decide which tool results remain useful.
- [Browser automation](/?category=browser#directory): choose among actions available on a page.
- [Evaluation](/?category=eval#directory): test assumptions and fit thresholds to your own data.

Next: [Why use Jev?](/why-jev/) or [How to get started](/how-to-use-jev/).
