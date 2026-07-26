# Module 17 — The Current Landscape (as of early–mid 2026)

This is the perishable module: a snapshot of who's who and which trends matter,
written with information current to early 2026 (with light mid-2026 notes).
Verify specifics against today's leaderboards; the *structure* of the landscape
changes slower than the names.

## 17.1 The frontier labs

- **OpenAI** — GPT-5 era (launched Aug 2025, unifying chat and reasoning behind
  a router, after the 4o/o-series split); Codex coding agent; deep consumer
  reach via ChatGPT; Microsoft partnership (loosened but central); Stargate-scale
  compute buildout.
- **Anthropic** — the Claude 4.x line through 2025 (Opus/Sonnet/Haiku tiers;
  extended thinking; computer use), with the Claude 5 generation arriving
  mid-2026; strongest reputation in coding/agentic work (Claude Code) and
  safety research (interpretability, RSP — module 16); enterprise-heavy
  business.
- **Google DeepMind** — Gemini 2.x → Gemini 3 (Nov 2025): 1M+ context,
  strong multimodality (Veo video, native image gen), TPU vertical integration,
  distribution via Search/Android/Workspace. Regained clear co-frontier status
  in 2025.
- **Meta** — the open-weights bet: Llama 3.x widely deployed; Llama 4's rocky
  2025 reception and the Superintelligence Labs reorg (massive talent spend)
  left its next act in flux; still the reason "free frontier-ish weights"
  exist in the West.
- **xAI** — Grok 3/4 on the huge Colossus cluster; fast follower pace,
  moderation controversies; tight X integration.
- **Chinese labs** — the 2025 story: **DeepSeek** (V3/R1: frontier-class at
  claimed ~$6M training cost, open weights, triggered a global repricing of
  AI economics in Jan 2025), **Alibaba Qwen** (the most-finetuned open family
  on HuggingFace), **Moonshot Kimi K2** (open trillion-param MoE), Zhipu,
  MiniMax. Consistently ~3–9 months behind the closed frontier at a fraction
  of the price, and *leading* the open-weights frontier much of the time —
  under tightening US export controls on compute.
- **Mistral** (EU champion, efficient open models) and a long tail of
  specialists (Cohere enterprise, AI21, etc.).

## 17.2 The open-vs-closed dynamic

- Open weights (note: weights ≠ full open source — data/recipes usually stay
  private) trail the closed frontier by months, not years; for most
  *applications* the gap is already immaterial, which keeps API pricing honest.
- The open frontier's center of gravity moved decisively to China in 2025
  (DeepSeek, Qwen, Kimi); Western opens (Llama, Mistral, Gemma, gpt-oss) compete
  tier-by-tier.
- Why give weights away: commoditize your complement, set standards, recruit,
  and (for China) route around distribution disadvantages. Why not: safety
  irreversibility (module 16 — you can't patch released weights) and business
  model.
- Practical builder takeaway: design model-agnostic (module 15.5's evals make
  swaps cheap); the "which model" decision is now a quarterly procurement
  question, not an architecture decision.

## 17.3 The economics

- **Training** frontier models: $100M+ per run and rising; clusters are
  gigawatt-scale, capex in the hundreds of billions industry-wide; power and
  chips (NVIDIA's dominance, TPU/Trainium alternatives, export controls) are
  the strategic bottlenecks.
- **Inference** prices meanwhile fell 100–1000× for equivalent capability since
  2022 (module 8's efficiency stack + competition + small-model quality). Both
  are true at once: frontier scarcity above, commodity abundance below.
- **Revenue is real now** — tens of billions annually across labs, dominated
  by coding, enterprise assistants/copilots, and consumer subscriptions;
  whether it justifies the capex is the live "bubble vs buildout" debate.
  Coding agents are the clearest product-market fit of the era (module 12.5).

## 17.4 The technical trends that define "now"

1. **Test-time compute & hybrid reasoning** (module 13) — the active scaling
   axis; effort routing is a product feature.
2. **Agents over chat** (module 12) — long-horizon autonomy (METR's doubling
   time-horizon curve, module 15.2), MCP as the integration standard,
   computer use maturing.
3. **Efficiency as a frontier** (modules 6, 8) — MoE everywhere, distillation
   tiers, small-on-device models; DeepSeek proved cleverness partially
   substitutes for compute.
4. **Multimodality converging into single models** (module 14) — realtime
   voice, native image gen, video generation commercializing.
5. **Synthetic + verifiable data** (modules 5.6, 7.4) — the data wall answered
   with RLVR and generated curricula.
6. **Safety/regulation becoming operational** (module 16) — EU AI Act phasing
   in, US policy oscillating, state-level fights; lab safety frameworks now
   binding-ish constraints on releases.

## 17.5 Capability reality check (calibrate your intuitions)

Where frontier models genuinely are (early 2026): gold-medal IMO math,
top-tier competitive programming, PhD-level science Q&A, multi-hour autonomous
coding tasks with real success rates (and real failure rates), expert-level
document/data work at scale. Where they still stumble: novel research-grade
problem solving without verification, long-horizon reliability (error
compounding), genuine spatial/physical reasoning, knowing what they don't
know (calibration under pressure), and anything adversarial (modules 9.5,
16.2). "Jagged frontier" (module 15.2) remains the single best two-word
summary — superhuman and silly, simultaneously, in the same afternoon.

## 17.6 How to stay current (the durable skill)

- **Primary sources beat commentary**: model/system cards, lab tech reports
  and blogs (OpenAI/Anthropic/DeepMind/DeepSeek/Qwen), the actual papers
  (arXiv cs.CL/cs.LG).
- **Leaderboards, plural, with module-15 skepticism**: LMArena, SWE-bench,
  LiveBench, ARC-AGI, HuggingFace open-LLM boards.
- **High-signal aggregators**: Karpathy (whatever he ships next), Simon
  Willison's blog (practical, honest), Interconnects (Nathan Lambert, for
  post-training), Zvi's newsletter (exhaustive), Latent Space (engineering).
- **Hands on the models weekly** — nothing recalibrates like usage; the vibes
  gap between model generations is felt before it's benchmarked.

## Exercises

1. Today, whenever you read this: pull current LMArena + SWE-bench standings
   and diff them against 17.1. What changed? Which 17.4 trend explains each
   change?
2. Price the same workload (1M input + 100k output tokens/day, mid-tier
   quality) across three providers and one self-hosted open model (module 8
   math). Where's the break-even?
3. Read one full frontier tech report (DeepSeek's are the most open) and map
   each section to a module of this course — a fun proof of how much you now
   understand.

## Further reading

- Whatever this quarter's model cards are — seriously, they're the syllabus
  now. The concepts to interpret them are in modules 1–16.
