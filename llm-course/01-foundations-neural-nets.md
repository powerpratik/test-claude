# Module 1 — Neural Networks from Scratch

Everything in this course runs on one substrate: differentiable functions optimized
by gradient descent. This module builds that substrate from zero.

## 1.1 What a neural network actually is

A neural network is just a **function with tunable knobs**:

```
ŷ = f(x; θ)
```

- `x` — input (an image, a sentence encoded as numbers, …)
- `θ` — parameters ("weights"), often billions of floating-point numbers
- `ŷ` — output (a probability distribution, a number, …)

Training = finding values of `θ` that make `f` produce good outputs. That's it.
"Learning" is an optimization problem.

The simplest useful `f` is a **linear layer**: `y = Wx + b`, a matrix multiply plus a
bias. Stack several with a nonlinearity between them and you get a **multi-layer
perceptron (MLP)**:

```python
import torch
import torch.nn as nn

mlp = nn.Sequential(
    nn.Linear(784, 256),  # W1x + b1
    nn.ReLU(),            # nonlinearity: max(0, x)
    nn.Linear(256, 10),   # W2h + b2
)
```

Why the nonlinearity? Two stacked linear layers collapse into one
(`W2(W1x) = (W2W1)x`). The nonlinearity is what lets depth add expressive power.
The **universal approximation theorem** says even one hidden layer can approximate
any continuous function given enough width — but deep networks approximate real-world
functions far more *efficiently*.

## 1.2 Loss: measuring wrongness

We need a number that says how bad the model's output is. For classification (and,
crucially, for next-token prediction) the standard is **cross-entropy loss**:

```
L = -log p_model(correct answer)
```

If the model assigns probability 0.9 to the right answer, loss = 0.105. If it
assigns 0.001, loss = 6.9. Minimizing cross-entropy = maximizing the probability the
model gives to the truth. This exact loss trains every LLM you've ever used.

To turn raw network outputs ("logits") into probabilities, we use **softmax**:

```
p_i = exp(z_i) / Σ_j exp(z_j)
```

Remember this pairing — *logits → softmax → cross-entropy* — it appears in
attention (module 3), in sampling (module 8), and in RLHF (module 7).

## 1.3 Gradient descent: turning the knobs

The gradient `∇θ L` points in the direction that *increases* loss fastest. So we
step the other way:

```
θ ← θ - η · ∇θ L        (η = learning rate)
```

In practice:
- **Stochastic/mini-batch GD** — compute the gradient on a small batch of examples,
  not the whole dataset. Noisier but vastly cheaper, and the noise even helps.
- **Adam / AdamW** — the optimizer used for virtually all LLM training. It adapts
  the step size per-parameter using running averages of the gradient (momentum) and
  its square (scale). AdamW adds decoupled weight decay.
- **Learning-rate schedules** — LLMs typically use *warmup* (start tiny, ramp up)
  then *cosine or linear decay*. Wrong LR is the #1 way training fails.

## 1.4 Backpropagation: computing gradients

Backprop is just the **chain rule**, applied systematically. Every operation in the
network knows its local derivative; the framework chains them backward from the loss
to every parameter.

Key mental model: the forward pass builds a **computation graph**; the backward pass
walks it in reverse, multiplying local derivatives. Frameworks (PyTorch, JAX) do this
automatically ("autograd"):

```python
loss = criterion(mlp(x), y)
loss.backward()        # gradients now sit in each parameter's .grad
optimizer.step()       # θ ← θ - η·grad (Adam-flavored)
optimizer.zero_grad()
```

You should hand-derive backprop for a 2-layer net **once** in your life (exercise 3).
After that, trust autograd — but understanding it explains phenomena like *vanishing
gradients* (deep chains of small derivatives multiply to ~0), which motivated
architectures you'll meet in modules 2–3 (LSTMs, residual connections).

## 1.5 Embeddings: turning symbols into vectors

Neural nets eat numbers, not words. An **embedding** maps a discrete symbol (a word,
a token, a user ID) to a learned dense vector:

```python
emb = nn.Embedding(num_embeddings=50_000, embedding_dim=768)
vec = emb(torch.tensor([1337]))   # → a 768-dim vector, learned like any weight
```

An embedding table is literally a matrix — row `i` is the vector for symbol `i` —
and it's trained by backprop like everything else. The magic is what the geometry
ends up encoding: similar things land near each other, and directions become
meaningful (the famous `king - man + woman ≈ queen`, module 2).

**This is the single most important concept for LLMs**: the entire input to a
Transformer is token embeddings, and its output layer is (often) the same matrix
transposed. Everything in between is manipulation of vectors in embedding space.

## 1.6 Tensors, shapes, and the GPU

- A **tensor** is an n-dimensional array. LLM code is 90% shape bookkeeping:
  `(batch, sequence_length, hidden_dim)` is the shape you'll see everywhere.
- Neural nets are dominated by **matrix multiplications**, which GPUs execute in
  massive parallel. This hardware fit — not any biological insight — is why deep
  learning took off in the 2010s and why NVIDIA became the world's most valuable
  company.
- **Precision**: weights are floats. Training typically uses bf16 (16-bit brain
  float) with fp32 accumulation; inference goes lower still (module 8's
  quantization).

## 1.7 Overfitting, regularization, generalization

- **Overfitting**: the model memorizes training data instead of learning the
  pattern; training loss drops while validation loss rises.
- Classic remedies: more data, weight decay, dropout, early stopping.
- LLM twist: frontier pretraining is often *single-epoch* over enormous data —
  each example is seen roughly once, so classic overfitting matters less than
  **data quality and mixture** (module 5). But memorization of repeated text is
  real and matters for privacy/copyright.

## Mental models to carry forward

1. **Everything is a differentiable function**; training is gradient descent on a
   scalar loss.
2. **Cross-entropy on next-token prediction** is the master objective of this course.
3. **Embeddings turn symbols into geometry**; the network computes in that geometry.
4. **Scale of matmuls on GPUs** is the physical reality underneath all of it.

## Exercises

1. Train an MLP on MNIST in PyTorch (~30 lines). Get >97% test accuracy. Break it:
   set the learning rate 100× too high and watch the loss diverge; 100× too low and
   watch it crawl.
2. Remove the ReLU from a 3-layer net and verify accuracy drops to that of a linear
   model.
3. On paper: derive the gradients of a 2-layer network with a scalar output and MSE
   loss. Check them numerically with finite differences.
4. Watch Karpathy's *"The spelled-out intro to neural networks and backpropagation:
   building micrograd"* and build micrograd yourself.

## Further reading

- Andrej Karpathy, *Neural Networks: Zero to Hero* (video series) — the companion
  to this entire course.
- *Deep Learning* (Goodfellow, Bengio, Courville) — chapters 6–8.
- PyTorch's 60-minute blitz tutorial.
