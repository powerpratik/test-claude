# Module 4 — Tokenization

Tokenization is the unglamorous layer where text becomes integers. It's also the
root cause of a shocking fraction of LLM weirdness — worth one focused module.

## 4.1 The problem

Neural nets need a **finite vocabulary** of symbols to embed (module 1.5). Options:

- **Characters**: tiny vocab, but sequences get very long (T² attention cost!) and
  the model wastes capacity re-learning that s-t-r-a-w spells part of a word.
- **Words**: short sequences, but the vocab is unbounded (typos, names, code,
  German compounds) and rare words get no training signal.
- **Subwords** — the compromise everyone uses: common words are single tokens,
  rare words split into meaningful chunks (`tokenization` → `token` + `ization`).

## 4.2 Byte-Pair Encoding (BPE)

The dominant algorithm. Training the tokenizer (before any neural net training):

1. Start with a base vocabulary (usually the 256 bytes).
2. Count all adjacent symbol pairs in the corpus; **merge the most frequent pair**
   into a new symbol; add it to the vocab.
3. Repeat until you hit the target vocab size (typically 32k–256k merges).

Encoding new text just replays the learned merges in order. Byte-level BPE (GPT-2
onward) starts from raw bytes, so **any** string — any language, emoji, binary — is
representable with zero "unknown token" failures.

Variants you'll see named: **WordPiece** (BERT — merge by likelihood, not
frequency), **SentencePiece/Unigram** (Llama, T5 — probabilistic pruning of a large
candidate vocab; language-agnostic since it treats input as a raw stream, marking
spaces with `▁`).

## 4.3 Practical realities

- **Rules of thumb (English)**: 1 token ≈ 4 characters ≈ 0.75 words. 100 tokens ≈ 75
  words. This is what API pricing and context limits are counting.
- **Whitespace is part of the token**: ` the` (with leading space) and `the` are
  different tokens. Trailing whitespace in a prompt can visibly degrade completions.
- **Case matters**: `hello`, `Hello`, `HELLO` — different tokens, different vectors.
- **Non-English costs more**: text in Thai or Hindi can cost 3–10× the tokens of
  equivalent English, because merges were learned mostly from English-heavy data.
  Same document, higher price, less effective context. Modern tokenizers (larger,
  more multilingual vocabs) have narrowed but not closed this gap.
- **Numbers fragment arbitrarily**: `2023` might be one token, `2027` two. Part of
  why raw LLMs are unreliable at arithmetic — and why they use code tools instead.
- **Chat special tokens**: conversations are serialized with reserved tokens like
  `<|im_start|>user … <|im_end|>` (format varies by lab). The "chat" experience is
  a formatting convention over the same next-token engine.

## 4.4 Tokenization explains the famous failures

- **"How many r's in strawberry?"** The model sees `straw`+`berry` as ~2 token IDs,
  not 10 letters. Character-level questions require it to have *memorized* each
  token's spelling.
- **Reversing a string, acrostics, rhyme schemes** — all fight the token boundary.
- **`SolidGoldMagikarp` / glitch tokens**: tokens that appeared in tokenizer
  training data but almost never in model training data have essentially untrained
  embeddings; feeding them in produced bizarre behavior in earlier GPTs.
- Sensitivity to trailing spaces, weird casing, or unusual Unicode — all boundary
  effects.

When an LLM does something inexplicably dumb with *sub-word structure*, suspect the
tokenizer first.

## 4.5 Hands-on

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")   # GPT-4-era tokenizer
ids = enc.encode("Tokenization explains many LLM quirks!")
print(ids)                          # [3404, 2065, 15100, 1690, 445, 11237, 74713, 0]
print([enc.decode([i]) for i in ids])
# ['Token', 'ization', ' explains', ' many', ' L', 'LM', ' qu', 'irks', '!']  (illustrative)
```

Play with the OpenAI tokenizer web demo or `tiktoken` until token boundaries stop
surprising you.

## 4.6 Frontier notes (early 2026)

- Vocab sizes have grown (GPT-2: 50k → recent models: 128k–256k+) — better
  multilingual coverage and shorter sequences, at the cost of a bigger embedding
  table and rarer per-token updates.
- **Byte-level / tokenizer-free models** (e.g. byte latent transformers) are a live
  research direction — learn patches from raw bytes, kill the tokenizer entirely —
  but haven't displaced BPE at the frontier yet.
- Multimodal models tokenize images/audio too: an image becomes a grid of patch
  embeddings (module 14) — "tokens" generalize beyond text.

## Mental models to carry forward

1. The model never sees letters — it sees **integer IDs with learned vectors**.
2. Tokens are the **unit of cost, context, and speed** — budget in tokens.
3. Subword boundaries are learned from data frequency, hence all the sharp edges.

## Exercises

1. Take 5 languages (English, Spanish, Chinese, Hindi, Arabic), tokenize the same
   paragraph (translated), and compare token counts.
2. Find three words that tokenize into surprising pieces. Explain each via BPE merge
   logic.
3. Implement toy BPE from scratch (~50 lines): train on a paragraph until you get a
   vocab of 300, then encode a held-out sentence.
4. Ask a chat model to count letters in `strawberry`, then ask it again but with the
   word spelled out s-p-a-c-e-d. Explain the difference in reliability.

## Further reading

- Karpathy, *Let's build the GPT Tokenizer* (video) — builds byte-level BPE from
  scratch.
- Sennrich et al., *Neural Machine Translation of Rare Words with Subword Units*
  (2016) — the BPE-for-NMT paper.
- The `tiktoken` and HuggingFace `tokenizers` libraries.
