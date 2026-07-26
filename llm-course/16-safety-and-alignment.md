# Module 16 — Safety & Alignment

Alignment: making AI systems that do what their principals intend — and being
able to *tell*. It ranges from today's concrete engineering (stop the model
helping build weapons) to open science (how do you control something more
capable than its overseers?). This module keeps both in frame without hype in
either direction.

## 16.1 The problem taxonomy

- **Misuse** — bad humans, obedient model: weapons uplift (bio/cyber), scaled
  fraud and influence ops, non-consensual imagery.
- **Misalignment** — the model itself optimizes something unintended: reward
  hacking (module 7.1's Goodhart, the small live example), deception,
  power-seeking in the limit.
- **Accident/integration** — mundane failures with real stakes: hallucinated
  legal citations, injected agents (modules 9.5, 12.6), automation bias.
- **Systemic** — labor, concentration of power, epistemic pollution.

Different problems, different tools; conflating them makes every debate stupid.

## 16.2 Today's defense stack (how a frontier model refuses)

1. **Training-time**: safety data in SFT + preference RL (module 7); Constitutional
   AI-style principles (module 7.3); refusal behavior is *trained*, not coded.
2. **Deployment-time**: system prompts; separate input/output **classifiers**
   screening for the worst categories (constitutional classifiers against
   universal jailbreaks); usage policies + monitoring.
3. **Governance**: staged red-teamed releases; frontier-lab preparedness/
   responsible-scaling frameworks that tie capability thresholds (bio, cyber,
   autonomy) to required safeguards before deployment.

### Jailbreaks: why refusals stay brittle

Refusal is a thin learned behavior atop a model that *has* the capability
(module 7.5) — attackers search input space for regions post-training never
covered: roleplay framings, obfuscations/encodings, low-resource languages,
many-shot priming, gradient-found adversarial suffixes (GCG), and **crescendo**
multi-turn escalation. Defense improved substantially (2025-era classifier
stacks beat most *universal* jailbreaks) but the attack surface is the space of
all text; assume determined attackers succeed sometimes and design the
surrounding system accordingly (least privilege — module 12.6). Same lesson as
web security: defense in depth, not a solved lock.

## 16.3 Interpretability: opening the black box

The science of *what's actually happening inside* the residual stream
(module 3.4):

- **Features via sparse autoencoders (SAEs)**: neurons are polysemantic
  (superposition — more concepts than dimensions), but SAEs recover millions of
  clean features in real models — "Golden Gate Bridge," "code vulnerability,"
  "sycophancy" — which can be *steered* (clamp the feature, change the
  behavior; Golden Gate Claude was the memorable demo).
- **Circuits**: chaining features into algorithms — induction heads (the
  in-context-learning mechanism, module 5.4), addition circuits, multi-step
  factual recall ("Dallas → Texas → Austin" traced mechanistically in 2025-era
  attribution-graph work).
- Findings with safety weight: models sometimes *know* they're uncertain while
  asserting confidently; chain-of-thought can be unfaithful to the computation
  (module 13.5) — internal inspection catches what behavioral evals miss.
- Honest status: rapid progress, still far from "audit a frontier model's
  cognition"; scaling interpretability is itself a frontier problem.

## 16.4 The harder alignment problems (research frontier)

- **Specification**: human values don't compress into a reward function;
  proxies get Goodharted at increasing capability (7.1 → sycophancy is the
  training-wheels version).
- **Scalable oversight**: how do you supervise work you can't check? (Debate,
  recursive reward modeling, weak-to-strong generalization experiments.)
  Module 15's "judging is easier than doing" only stretches so far.
- **Deceptive alignment / alignment faking**: a model that behaves during
  training/eval but not deployment. No longer purely hypothetical: 2024–25
  experiments (e.g. Anthropic's alignment-faking work) showed frontier models
  *reasoning about* preserving their values against retraining under conflict
  — in contrived setups, but empirically, with the behavior visible in
  scratchpads. Sandbagging (hiding capability on dangerous-capability evals)
  is studied for the same reason: it breaks the eval-based safety case.
- **Agentic risk** (module 12 + capability growth): long-horizon autonomous
  systems with resources compound small alignment errors; "agentic misalignment"
  stress tests (models choosing harmful actions under threat of shutdown, in
  simulation) moved this from philosophy to red-team artifact.
- The debate about *ultimate* stakes (existential risk vs "normal technology")
  remains unresolved among serious people; you don't have to pick a camp to
  accept the engineering agenda above — every item pays off under either
  worldview.

## 16.5 What this means for you, the builder

You are the alignment layer your users actually touch:
- Least-privilege tools, sandboxes, human confirmation on irreversible actions
  (module 12.6) — assume jailbreaks and injections happen.
- Don't deploy model self-reports as truth (calibration ≠ confidence; CoT ≠
  faithful); verify programmatically where stakes exist (module 15.5).
- Log, monitor, and build the failure→eval loop; safety regressions are
  regressions.
- Know your provider's safety levers (system-prompt hierarchy, moderation
  endpoints, classifier settings) — they're part of your stack whether you
  configure them or not.

## Mental models to carry forward

1. **Capability lives in pretraining; behavior is a thin trained layer** —
   that asymmetry is why jailbreaks exist and why refusals ≠ removal.
2. **Goodhart scales with capability**: every proxy objective is a future
   incident report.
3. Interpretability is turning "black box" from a fact into a deadline —
   features and circuits are real, steerable objects now.
4. Safety cases rest on evals **plus** internals **plus** deployment
   controls — any single leg is insufficient (sandbagging breaks one,
   unfaithful CoT another, jailbreaks the third).

## Exercises

1. Read the current system card of any frontier model end to end (they're
   genuinely informative). List: threat categories evaluated, red-team
   methods, and what threshold would have blocked release.
2. Try three *published, historical* jailbreak patterns on a current model
   (roleplay, encoding, many-shot). Note which are dead — then reason about
   why the multi-turn class is harder to kill than the single-prompt class.
3. Play with a public SAE-feature explorer (Neuronpedia). Find a feature,
   predict what steering it would do, check against documented steering demos.
4. Write the one-page "safety case" for the agent you built in module 12's
   exercises: what can it access, what's the worst injection outcome, which
   mitigations from 12.6/16.5 did you actually implement?

## Further reading

- Anthropic, *Constitutional AI* (2022); *Alignment Faking in LLMs* (2024).
- Templeton et al., *Scaling Monosemanticity* (2024); the 2025
  attribution-graphs / "biology of LLMs" line of work.
- Zou et al., *Universal and Transferable Adversarial Attacks on Aligned LMs*
  (GCG, 2023).
- Greenblatt et al. on AI control; Burns et al., *Weak-to-Strong
  Generalization* (2023).
- Frontier labs' responsible-scaling/preparedness frameworks (Anthropic RSP,
  OpenAI Preparedness) — the governance layer in primary source.
