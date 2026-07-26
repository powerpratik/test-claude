# Module 2 — Language Modeling Before Transformers

The Transformer didn't come from nowhere. This module covers the 70-year arc that
led to it — and defines the **language modeling** objective that everything since
still optimizes.

## 2.1 The objective: predict the next word

A **language model (LM)** assigns probability to text. By the chain rule of
probability, any sequence factorizes as:

```
P(w1, w2, …, wn) = P(w1) · P(w2|w1) · P(w3|w1,w2) · … · P(wn|w1…wn-1)
```

So modeling language reduces to one repeated question: **given the context so far,
what's the distribution over the next word?** Every model in this module — and
GPT-5 — answers exactly that question. The differences are only in *how well* and
*with how much context*.

Standard quality metric: **perplexity** = exp(average cross-entropy per token).
Intuition: a perplexity of 20 means the model is, on average, as uncertain as if it
were choosing uniformly among 20 words. Lower is better.

## 2.2 N-gram models (1950s–2000s)

Count and divide: estimate `P(word | previous k-1 words)` from corpus counts.

- **Strength**: simple, fast, was the backbone of speech recognition and Google
  autocomplete for decades.
- **Fatal flaws**: no generalization (counts for "red car" tell you nothing about
  "crimson automobile") and combinatorial sparsity — most 5-word sequences never
  occur even in huge corpora. Smoothing (Kneser-Ney) helps but can't fix it.

The lesson that stuck: **you cannot scale symbolic counting; you need
generalization**, which means representations.

## 2.3 Word embeddings: word2vec and friends (2013)

**word2vec** (Mikolov et al.) trained shallow networks on a simple task — predict a
word from its neighbors (CBOW) or neighbors from a word (skip-gram) — and the
byproduct was word vectors with stunning structure:

- Similar words cluster (`cat` near `dog`, `kitten`).
- Directions encode relations: `vec(king) - vec(man) + vec(woman) ≈ vec(queen)`;
  `vec(Paris) - vec(France) + vec(Italy) ≈ vec(Rome)`.

This validated the **distributional hypothesis** ("you shall know a word by the
company it keeps") at scale and made embeddings (module 1.5) the universal input
representation for NLP. GloVe (2014) got similar results from global co-occurrence
statistics.

Limitation: **one vector per word, regardless of context**. "Bank" in "river bank"
and "bank account" got the same vector. Fixing that required contextual models.

## 2.4 Recurrent networks: RNNs and LSTMs (2014–2017 era)

An **RNN** reads a sequence one token at a time, maintaining a hidden state — a
running summary — updated at each step:

```
h_t = tanh(W_h · h_{t-1} + W_x · x_t)
```

In principle it can carry information forever. In practice, gradients flowing
backward through many steps repeatedly multiply by the same weight matrix and either
**vanish** or **explode** — long-range dependencies are nearly unlearnable.

The **LSTM** (Long Short-Term Memory, Hochreiter & Schmidhuber 1997, dominant
2014–2017) fixed this with a *gated cell state*: learned gates decide what to
remember, forget, and output, giving gradients a protected highway through time.
LSTMs powered the first genuinely impressive neural text generation (Karpathy's 2015
*"Unreasonable Effectiveness of RNNs"* post is a fun time capsule) and Google
Translate's 2016 neural rewrite.

Remaining problems:
1. **Sequential bottleneck** — you must process token 1 before token 2. No
   parallelism across the sequence during training; GPUs sit idle.
2. **Information bottleneck** — everything about the past must squeeze through one
   fixed-size hidden state vector.

## 2.5 Seq2seq and the birth of attention (2014–2015)

**Sequence-to-sequence** (Sutskever et al. 2014): one RNN (the *encoder*) reads the
source sentence into a final hidden state; another (the *decoder*) generates the
translation from it. It worked — but the entire source sentence had to fit into one
vector. Translation quality visibly degraded on long sentences.

**Attention** (Bahdanau et al. 2015) was the fix: instead of one summary vector, let
the decoder, at every output step, compute a **weighted average over all encoder
states**, with weights determined by relevance to what it's generating right now.

```
attention(query, keys, values) = Σ_i softmax(score(query, key_i)) · value_i
```

The decoder generating the French word for "bank" can look directly at the English
word "bank" *and its neighbors* to disambiguate. Attention weights were even
interpretable — you could visualize soft word alignments.

This was the crucial conceptual leap: **content-based, learned, differentiable
lookup**. The 2017 insight (next module) was simply: if attention is this good,
*delete the RNN and keep only attention*.

## 2.6 Timeline at a glance

| Year | Milestone | Lasting idea |
|------|-----------|--------------|
| ~1950s–2000s | N-grams | LM objective; perplexity |
| 1997 | LSTM invented | Gating; protected gradient flow |
| 2013 | word2vec | Embeddings; semantic geometry |
| 2014 | seq2seq | Encoder–decoder framing |
| 2015 | Bahdanau attention | Differentiable content-based lookup |
| 2017 | **Transformer** | Attention is all you need → module 3 |

## Mental models to carry forward

1. **Next-token prediction is the eternal objective** — models changed, the task
   didn't.
2. **Representations beat counting** — generalization comes from geometry.
3. **Attention = soft lookup** — query against keys, retrieve values. Internalize
   this before module 3; self-attention is just this applied within one sequence.
4. Architectures win partly on **hardware efficiency**: the Transformer's real
   killer feature over LSTMs was training parallelism.

## Exercises

1. Build a character-level bigram model (counting, no neural net) on Shakespeare;
   sample from it. Then compare with a neural bigram model — same data, same
   perplexity question. (This is Karpathy's *makemore* part 1.)
2. Load pretrained word2vec/GloVe vectors (gensim) and test analogies. Find one that
   works and two that embarrassingly don't.
3. Train a small LSTM character LM on Shakespeare. Generate 500 characters. Note
   how coherence degrades with length — you're feeling the bottleneck of 2.4.

## Further reading

- Karpathy, *The Unreasonable Effectiveness of Recurrent Neural Networks* (2015).
- Mikolov et al., *Efficient Estimation of Word Representations* (2013).
- Bahdanau, Cho, Bengio, *Neural Machine Translation by Jointly Learning to Align
  and Translate* (2015).
- Olah, *Understanding LSTM Networks* (colah.github.io).
