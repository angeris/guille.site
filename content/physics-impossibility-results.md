title: Physics, optimization, and impossibility
slug: physics-impossibility-results
category: physics
tags: statistics, math, physics
date: 2018-12-15

*Note:* this post is based on the results of [this arXiv paper](https://arxiv.org/abs/1811.12936) which I've been working on with Stephen Boyd and Jelena Vuckovic.

The main result of the above paper is kind of weird: essentially, it turns out that you can say what devices are physically *impossible* by phrasing certain problems as optimization problems and then using some basic tools of optimization to derive lower bounds.

To illustrate: imagine you want to generate an engine which is as efficient as possible, then we know the best you could possibly hope to do is given by the [Second law of thermodynamics](). Now, what if (and bear with me here) we want something a little weirder? Say, what if we want a heat sink that has a particular dissipation pattern? Or what if you want a photonic crystal that traps light of a given wavelength in some region? Or a horn which has specific resonances?

We can write down the optimization problems corresponding to each of these circumstances: in general, these problems are very hard to solve in ways that aren't just "try all possible designs and pick the best one." (And there are a *lot* of possible designs.) By using some simple heuristics—gradient descent, for example—we appear to do quite well relative to what almost anyone can do by hand. This approach brings up a few questions with no obvious answers.

1. Maybe there is some design that is really complicated that these heuristics almost always miss.
2. It is possible that the objective we are requesting is physically impossible to achieve.
3. Many heuristics depend heavily on the initial design we provide. Physical intuition sometimes appears to provide good initializations, but often the final design is unintuitive, so perhaps there are better approaches.

The paper provides (some) answers to these questions. In particular, it answers point (2) as its main goal, which gives a partial answer to (1) (namely that the heuristics we use appear to be often close to the global optimum, at least for the problems we tested), and an answer to (3), since the impossibility result suggests an initial design as a byproduct of computing the certificate of impossibility.

I'll explain the interesting parts of this paper in more detail below, since the paper (for the sake of brevity) simply references the reader to derivations of the results (and leaves some as exercises).

## Lagrange duality
In optimization theory, there is a beautiful idea called *Lagrange duality*, which gives lower bounds to any optimization problem you can write down (at least theoretically speaking).

Let's say we have the following optimization problem,
$$
\begin{array}{ll}
\text{minimize} & f(x)\\\\
\text{subject to} & h(x) \le 0,
\end{array}
$$
(this encompasses essentially every optimization problem ever) with objective function $f: \mathbb{R}^n \to \mathbb{R}$ and constraint function $h: \mathbb{R}^n \to \mathbb{R}^m$, and the inequality is taken elementwise. Call the optimal value of the objective of the optimization problem $p^\star$, which we will see again soon.

Continuing, we can then formulate the *Lagrangian* of the problem,
$$
\mathcal{L}(x, \lambda) = f(x) + \lambda^Th(x),
$$
with $\lambda \ge 0$. Finally, we formulate the dual *function*
$$
g(\lambda) = \inf_x \left(f(x) + \lambda^Th(x)\right).
$$
Now, and here's the magic, this dual function $g(\lambda)$ at any $\lambda \ge 0$ is always a lower bound for the optimal objective $p^\star$. Why? Well,
$$
g(\lambda) = \inf_x \mathcal{L}(x, \lambda),
$$
and, by definition of $\inf$,
$$
\inf_x \mathcal{L}(x, \lambda) \le \mathcal{L}(x, \lambda),
$$
for every $x$. Now, every feasible point $x^\mathrm{feas}$ of the optimization problem satisfies $h(x) \le 0$ (this is the definition of 'feasible'), so, since $\lambda \ge 0$,
$$
\mathcal{L}(x^\mathrm{feas}, \lambda) = f(x^\mathrm{feas}) + \underbrace{\lambda^Th(x^\mathrm{feas})}_{\le 0} \le f(x^\mathrm{feas}).
$$
In other words, for any feasible point, $\mathcal{L}(x^\mathrm{feas}, \lambda)$ is always smaller than the objective value at that point. But, since $g(\lambda)$ is smaller than $\mathcal{L}(x, \lambda)$ for *any* $x$, not just the feasible ones, we have
$$
g(\lambda) \le f(x^\mathrm{feas}),
$$
for any feasible point. This means that it is also at most as large as the optimal value (since every optimal point of this optimization problem is feasible). That is,
$$
g(\lambda) \le p^\star.
$$
Therefore, for any $\lambda\ge 0$, we know that $g(\lambda)$ is always a lower bound to the optimal objective value!

Of course, sometimes computing $g(\lambda)$ is at least as difficult as solving the original problem (due to the $\inf$ we have in the definition of $g$). It just so happens that many physical equations and objectives we care about are of a form elegant enough to give an explicit formula for $g$, which is the main point of this paper.

### Best lower bound
Of course, we often want the best (largest) lower bound, not just *a* lower bound (which can often be quite bad). In other words, we want to maximize our lower bound. We can phrase this as the new optimization problem,
$$
\begin{array}{ll}
\text{maximize} & g(\lambda)\\\\
\text{subject to} & \lambda \ge 0.
\end{array}
$$
What is interesting, is that this optimization problem is always convex—e.g., it is almost always easy to compute the optimal value, if we can explicitly write down what $g$ is. (I won't prove this here, but the proof is very straightforward. Take a peek at 5.1.2 in Boyd's [*Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/).)

## Explicit dual function for $g$


