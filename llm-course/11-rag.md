# Module 11 — Retrieval-Augmented Generation (RAG)

Models know the internet up to a cutoff; they don't know your wiki, your tickets,
or what happened yesterday. RAG fixes that by **putting the right facts in the
context window at question time** — module 9's "context engineering" made
systematic.

## 11.1 The core loop

```
User question
  → retrieve relevant chunks from your corpus
  → stuff them into the prompt ("answer using these sources; cite them")
  → model generates a grounded answer
```

Why this beats fine-tuning for knowledge (module 10.1): updatable in seconds
(re-index, done), citable (users can verify), access-controllable (filter chunks
by permission *before* the model sees them), and it doesn't teach the model to
confabulate in your domain's voice.

## 11.2 Embeddings and vector search

The retrieval workhorse is **dense retrieval**: an embedding model (a small
encoder-style Transformer — module 3.6's other family, alive and well) maps text
to vectors such that semantic similarity ≈ cosine similarity. Index all chunk
vectors; embed the query; return nearest neighbors (ANN indexes — HNSW — make
this fast at millions of chunks).

- Dense retrieval matches **meaning** ("How do I get my money back?" ↔ "Refund
  policy") where keyword search matches **strings**.
- But keyword/**BM25** still wins on exact identifiers: error codes, SKUs, names,
  API symbols. Hence the standard answer is **hybrid search** (dense + BM25,
  scores fused), which is robustly better than either alone.
- Embedding models are ranked on **MTEB**; strong open options (bge, gte, Qwen
  embeddings) and API options abound. The embedding model is swappable
  infrastructure — benchmark on *your* data.

## 11.3 Chunking

Documents must be split before indexing, and chunking is an unreasonably
important knob:

- Too big → diluted vectors, wasted context; too small → fragments without
  context. Common starting point: 300–800 tokens with 10–15% overlap, splitting
  on structure (headings, paragraphs) rather than fixed character counts.
- Attach **metadata** (title, section path, date, permissions) to every chunk —
  for filtering and for the model's citations.
- **Contextualized chunks** (a 2024-era upgrade that stuck): prepend a short
  LLM-generated line situating the chunk in its document ("From the refunds
  section of the EU customer policy…") before embedding. Cheap, large retrieval
  gains.

## 11.4 The quality ladder

Deploy in this order; stop when your evals pass:

1. **Baseline**: hybrid search → top-k (5–10) chunks → prompt with citations
   required.
2. **Reranking**: retrieve wide (top-50), then a **cross-encoder reranker**
   (Cohere Rerank, bge-reranker) scores each (query, chunk) pair jointly and you
   keep the top-5. Rerankers read the pair together, so they're far more accurate
   than embedding distance; this is the single highest-ROI upgrade in RAG.
3. **Query transformation**: rewrite the user's message into better search
   queries (decompose multi-part questions; resolve pronouns from chat history;
   HyDE — embed a hypothetical answer instead of the question).
4. **Structure-aware tricks**: parent-chunk retrieval (match small, feed the
   model its bigger parent section), multi-hop retrieval for questions that need
   chained lookups.
5. **GraphRAG-style** approaches (entity/relation summaries) for "connect the
   dots across many documents" corpora — heavyweight, situational.

## 11.5 Failure modes and their fixes

| Symptom | Usual cause | Fix |
|---|---|---|
| Right answer exists, wasn't retrieved | embedding mismatch, bad chunking | hybrid search, reranker, contextual chunks |
| Retrieved but ignored | too many/noisy chunks, lost-in-middle | rerank harder, fewer better chunks |
| Fluent answer, wrong facts | retrieval failed and the model free-styled | require citations, instruct "say 'not found'", eval groundedness |
| Stale answers | index lag | incremental re-indexing; recency boosting |
| Users see data they shouldn't | filtering after retrieval or not at all | permission filters at query time, in the index |

The meta-lesson: **most "LLM is hallucinating" complaints in RAG apps are
retrieval failures.** Debug the search engine before blaming the model.

## 11.6 Evaluating RAG (do this before tuning anything)

Build a set of (question → ideal answer + source passages) — even 50 is
transformative. Measure the two stages *separately*:

- **Retrieval**: recall@k / MRR — is the needed passage in what we fetched?
- **Generation**: groundedness/faithfulness (claims supported by the provided
  chunks?) and answer relevance — typically scored by an LLM judge
  (module 15's methods, with their caveats).

Frameworks: RAGAS, or hand-rolled judge prompts. Without this, the 11.4 ladder is
guesswork.

## 11.7 RAG in 2026: not dead, just absorbed

Long context (module 6.4) did *not* kill RAG: million-token windows still cost
money and latency per call, corpora are billions of tokens, and permissions/
freshness still require retrieval. What changed is the interface — increasingly,
retrieval is a **tool an agent calls** (module 12): the model searches, reads,
decides to search again with a refined query, and iterates ("agentic RAG"),
rather than receiving one static stuffed prompt. The components in this module
are unchanged underneath; the orchestration moved into the model's loop.

## Mental models to carry forward

1. **RAG = search engine + reader.** Quality is usually won or lost in search.
2. **Hybrid retrieval + reranking** is the boring, correct default.
3. Chunking and metadata are data engineering, and they dominate outcomes.
4. Evaluate retrieval and generation **separately** or debug blind.

## Exercises

1. Build a minimal RAG over 20–50 real documents (your notes, a project's docs):
   chunk → embed (open model) → FAISS/Chroma or even a flat cosine loop → answer
   with citations. No framework; ~100 lines. Frameworks after fundamentals.
2. Write 20 eval questions. Measure recall@5 for dense-only vs hybrid vs
   hybrid+reranker. (Expect the ladder to show up in your numbers.)
3. Create three questions whose answers are absent from your corpus. Does your
   system say "not found" or confabulate? Fix the prompt until it behaves.
4. Break dense retrieval: find a query where BM25 wins (an exact code/name) and
   one where dense wins (paraphrase). Understand *why* before automating.

## Further reading

- Lewis et al., *Retrieval-Augmented Generation* (2020) — the namesake paper.
- Anthropic, *Contextual Retrieval* post (2024).
- MTEB leaderboard; RAGAS docs.
- Asai et al., *Self-RAG* (2023) and the agentic-RAG literature for where 11.7 is
  heading.
