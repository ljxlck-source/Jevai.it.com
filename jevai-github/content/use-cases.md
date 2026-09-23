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


## Related topics

[Quick overview](/what-is-jev/) · [Getting started](/how-to-use-jev/) · [Examples](/examples/) · [Official TypeSafe resources](/typesafe/)
