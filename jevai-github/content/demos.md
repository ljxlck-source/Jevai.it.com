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


## Related topics

[Quick overview](/what-is-jev/) · [Getting started](/how-to-use-jev/) · [Examples](/examples/) · [Official TypeSafe resources](/typesafe/)
