## 1. Get access to TypeSafe

Visit [typesafe.ai](https://typesafe.ai/) and follow the current access or waitlist process. Approval timing is controlled by TypeSafe.

## 2. Ask your coding agent to install the skill

For Codex or another supported agent, ask it to install the TypeSafe skill with:

```sh
npx skills add typesafe-ai/skills --skill typesafe-ai
```

For Claude Code, use the plugin installation instead:

```sh
claude plugin marketplace add typesafe-ai/skills
claude plugin install typesafe@typesafe-ai
```

Choose one installation method. These commands are documented in the [official TypeSafe skills repository](https://github.com/typesafe-ai/skills).

## 3. Create an API key

Sign in to the [TypeSafe console](https://console.typesafe.ai/) and create a key under API Keys. Configure it in your local environment as `TYPESAFE_API_KEY`; keep it out of browser code and GitHub commits.

<figure><img src="/assets/typesafe-console-home.png" alt="TypeSafe console home with API Keys navigation and an agent Quickstart panel" width="2052" height="1284" loading="lazy"><figcaption>TypeSafe console and agent Quickstart. Screenshot supplied with the source article, credited there to Flavio Copes.</figcaption></figure>

## 4. Describe the job in plain language

Start your instruction with **“use the TypeSafe skill”**. Explain the data, the categories and what should happen when the answer is uncertain.

> Use the TypeSafe skill. Read my support tickets, route each one to billing, technical support, sales or other, and flag uncertain decisions for review. Write the integration and test it on my sample data. The API key is available in TYPESAFE_API_KEY.

Your coding agent can write and run the integration. You still check that the results match your business rules before using it on live work.

[See the complete comment-triage example](/examples/) or [plan a gradual rollout](/integration/).
