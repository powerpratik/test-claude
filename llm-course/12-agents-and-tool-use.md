# Module 12 — Agents & Tool Use

A chat model answers; an **agent** *acts*: it calls tools, observes results, and
iterates toward a goal. This is the layer where LLMs stopped being autocomplete
and started being coworkers — and the defining product story of 2025–2026.

## 12.1 Tool use / function calling

The primitive underneath everything. You declare tools as schemas; the model
emits a structured call instead of (or alongside) prose; *your code* executes it
and returns the result as a new message; the model continues.

```json
{"name": "get_weather",
 "description": "Current weather for a city",
 "parameters": {"type": "object",
   "properties": {"city": {"type": "string"}},
   "required": ["city"]}}
```

```
User: Do I need an umbrella in Miami?
Model: → tool_call get_weather({"city": "Miami"})
You:   → tool_result {"condition": "thunderstorms", "temp_f": 84}
Model: Yes — thunderstorms right now. Take one.
```

Things to internalize:
- The model **never executes anything** — it emits intentions; your runtime has
  all the authority (and all the responsibility).
- Tool-calling is a *trained behavior* (module 7's post-training installs the
  syntax and the judgment of when to call).
- **Description quality is prompt engineering**: the model chooses tools by
  reading your schemas. Vague descriptions → wrong calls.
- Structured outputs (module 8.2) guarantee the call is well-formed; nothing
  guarantees it's *wise*.

## 12.2 The agentic loop

An agent is embarrassingly little code:

```python
while not done:
    response = model(messages, tools)
    if response.tool_calls:
        for call in response.tool_calls:
            messages.append(execute(call))   # results become context
    else:
        done = True                          # model chose to answer
```

The intelligence is in the model; the engineering is in everything around the
loop: which tools, what context each iteration (module 9.6), when to stop, what
needs human approval. The ReAct pattern (reason → act → observe, 2022) named the
idea; RL on multi-step tasks (module 7.4) is what made models genuinely good at
it — modern models are *trained as agents*, not merely prompted into being one.

## 12.3 What separates a demo from a production agent

- **Error recovery**: tools fail, pages time out, tests break. Good agents read
  the error and adapt; this robustness is a trained capability and a top
  differentiator between models.
- **Context management over long horizons**: hours-long tasks overflow any
  window. Techniques: summarize/compact old turns, external memory files
  (scratchpads, `notes.md`), sub-agents with fresh contexts for subtasks
  (fan-out/fan-in).
- **Stopping and escalation criteria**: budget caps, "ask before irreversible
  actions," progress detection (agents can loop forever politely).
- **Verification**: the agent should check its own work where checkable — run
  the tests, re-query the database, diff the output. Verifiable feedback is why
  coding agents got good first.
- **Observability**: log every step; you cannot debug what you didn't record.

## 12.4 MCP — the standardization moment

Every (app × tool) pair used to be custom glue. **Model Context Protocol**
(Anthropic, late 2024; adopted broadly across the industry in 2025, including by
OpenAI and Google) standardizes it: an MCP *server* exposes tools/resources/
prompts over a common protocol; any MCP *client* (Claude, IDEs, custom agents)
can use any server. USB-C for AI tooling. Thousands of servers exist — GitHub,
Postgres, Slack, browsers, filesystems. If you build integrations in 2026, you
build an MCP server once instead of N plugins.

## 12.5 The agent landscape (early 2026)

- **Coding agents** — the killer app: Claude Code, OpenAI Codex, Cursor,
  GitHub Copilot's agent mode, open-source (Aider, OpenHands). They run
  multi-hour tasks: read a repo, plan, edit, run tests, iterate, open a PR.
  Why coding first? Verifiable rewards (module 7.4) + economic value + the
  developers building agents are their own users.
- **Computer use / browser agents**: the model operates GUIs via screenshots and
  clicks. Works, still brittle relative to API-based tools; improving fast.
- **Deep research agents**: multi-query web research with synthesis and
  citations (OpenAI/Google/Anthropic all ship one).
- **Orchestration frameworks**: LangGraph, OpenAI Agents SDK, Claude Agent SDK,
  CrewAI… Useful, but the trend is *less* scaffolding as models improve — many
  production systems are the 12.2 loop plus good tools. Start simple; add graphs
  only when the task truly needs them (the "bitter lesson" applied to agent
  design: heavy hand-engineered workflows keep getting eaten by better models).
- **Multi-agent patterns**: orchestrator + parallel sub-agents (research fan-out,
  reviewer/worker pairs). Real gains for parallelizable work; also easy
  complexity theater — reach for it when one context window genuinely can't hold
  the task.

## 12.6 Safety: agents inherit every earlier risk, with hands

Prompt injection (module 9.5) escalates from "wrong answer" to "wrong *action*":
a malicious web page reads "also email the contents of ~/.ssh to…" and an agent
with mail access might comply. The uncomfortable trio is **untrusted input +
private data + external actions** — avoid granting all three to one context.
Mitigations (defense in depth, again): least-privilege tools, sandboxed
execution, human-in-the-loop for irreversible/expensive actions, allowlists for
destinations (git remotes, email domains), audit logs. Treat an agent like a
junior employee with root: capable, fast, and phishable.

## Mental models to carry forward

1. **Agent = model + tools + loop**; the loop is trivial, the model's trained
   judgment does the work.
2. Tools are described, not wired — **schemas are the API and the prompt**.
3. **Verifiability predicts where agents work well** (code > research > open-ended).
4. Prompt injection + tools = the security problem of this decade. Least
   privilege always.

## Exercises

1. Build the 12.2 loop raw against any LLM API (no framework) with two tools:
   `calculator` and `read_file`. Watch it chain calls on "summarize notes.txt and
   double every number in it."
2. Add a deliberately flaky tool (random 30% failures). Compare how a strong vs
   a weak model recovers.
3. Give your agent a `search_web` tool and plant an injection in a page it will
   read. Then defend: separate the "reader" context from the "actor" context and
   re-attack.
4. Use a production coding agent (Claude Code, Codex, Aider) on a real small task
   in one of your repos. Read its full transcript afterward — the observed loop
   *is* this module.

## Further reading

- Yao et al., *ReAct* (2022).
- Anthropic, *Building Effective Agents* (2024) — the "start simple" argument.
- MCP specification and server directory (modelcontextprotocol.io).
- SWE-bench (pairs with module 15) for how agentic coding is measured.
