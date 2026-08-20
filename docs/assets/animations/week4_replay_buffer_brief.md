# Generation Brief: Week 04 Replay Buffer & Target Network Animation

## 1. Pedagogical Intent

Show two practical DQN mechanisms without promising convergence:

1. **Experience replay** stores chronological transitions in a bounded circular
   buffer and samples them in a randomized order. This reduces local temporal
   adjacency and reuses experience; it does not make an evolving finite buffer
   literally i.i.d.
2. **Delayed target parameters** supply next-state values that remain fixed
   between synchronizations. This slows one source of target motion; it does
   not make the full training objective globally stationary.

---

## 2. Visual Architecture
- **Replay Panel (Left)**: LineWorld transitions stored as
  `(state, action, reward, next_state, terminated, truncated)`.
- **Circular Replay Buffer (Center)**: A visual ring of slots showing FIFO insertion and highlighted uniform random batch extraction.
- **Dual Network Panel (Right)**:
  - **Online parameters** receive a real minibatch semi-gradient update.
  - **Delayed parameters** supply Bellman targets and synchronize every four
    optimizer updates.

The visual must compute targets from sampled transitions. It must not animate
fixed arbitrary weight increments while describing them as SGD.

---

## 3. Interaction & Accessibility
- **Controls**: Collect transition, sample/update, synchronize, auto/pause, and
  reset.
- **Design Tokens**: Standard semantic course palette: state blue, action
  orange, reward green, value purple, error red, baseline gray, learned policy
  teal.
- **Accessibility**: Full screen-reader ARIA live region updates, semantic tags, and `@media (prefers-reduced-motion: reduce)` support.
