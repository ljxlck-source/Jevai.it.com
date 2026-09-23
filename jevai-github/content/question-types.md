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


## Related topics

[Quick overview](/what-is-jev/) · [Getting started](/how-to-use-jev/) · [Examples](/examples/) · [Official TypeSafe resources](/typesafe/)
