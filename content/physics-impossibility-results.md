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
What is interesting is that this optimization problem is always convex—*e.g.*, it is almost always easy to compute the optimal value, *if* we can explicitly write down what $g$ is. (I won't prove this here, but the proof is very straightforward. Take a peek at section 5.1.2 in Boyd's [*Convex Optimization*](https://web.stanford.edu/~boyd/cvxbook/).)

## Explicit dual function for $g$

### Problem formulation
Many of the problems we're interested in (including design in photonics via Maxwell's equations,[^maxwell] acoustics via Helmholtz's equations, quantum mechanics via Schrodinger's equation, and heat engineering via the heat equation) have physics equations of the form (once discretized)
$$
(A + \mathrm{diag}(\theta))z = b,
$$
where $\theta \in \mathbb{R}^n$ are the design parameters (*e.g.* permittivity in the case of photonics, or speed of sound in the material in the case of acoustics) and $z \in \mathbb{R}^n$ is the field (*e.g.* the electric field in photonics, or the amplitude of the wave in acoustics).

More specifically, if you take a peek at Helmholtz's equation:
$$
\nabla^2 a(x) + \left(\frac{\omega^2}{c(x)^2}\right)a(x) = u(x),
$$
where $c: \mathbb{R}^3 \to \mathbb{R}\_{> 0}$ is a function specifying the speed of sound at every point in the material, while $a: \mathbb{R}^3 \to \mathbb{R}$ is a function specifying the amplitude at each point, $u: \mathbb{R}^3 \to \mathbb{R}$ is a function specifying an excitation, and $\omega \in \mathbb{R}\_{\ge 0}$ is the frequency of the wave. We can make some simple correspondences:
$$
\Bigg(\underbrace{\nabla^2}\_{A} + \underbrace{\bigg(\frac{\omega^2}{c(x)^2}\bigg)}\_{\mathrm{diag}(\theta)}\Bigg)\underbrace{a(x)}\_{z} = \underbrace{u(x)}\_{b}.
$$

Now, we usually want the field ($z$) to look similar to a desired field (which we will call $\hat z$), while satisfying the physics equation described above. We can phrase this in several ways, but a [particularly natural one](/ls-images.html) is by attempting to minimize the objective $\left\|z - \hat z\right\|\_2^2$.

Finally, we are only able to choose materials within a specific range: that is, $\theta^\mathrm{min} \le \theta \le \theta^\mathrm{max}$.

Putting all of this together, we can write the optimization problem as
$$
\begin{array}{ll}
\text{minimize} & \frac12\left\|z - \hat z\right\|\_2^2\\\\
\text{subject to} & (A + \mathrm{diag}(\theta))z = b\\\\
& \theta^\mathrm{min} \le \theta \le \theta^\mathrm{max}.
\end{array}
$$
which is exactly problem (1) in the paper, in the special case where $W = I$, the identity matrix.

### Deriving the dual
Here is essentially the only 'magic' part of the paper. First, we can write the Lagrangian of the problem as,
$$
\mathcal{L}(z, \theta, \nu) = \frac12\left\|z - \hat z\right\|\_2^2 + \nu^T((A + \mathrm{diag}(\theta))z - b).
$$
Now, there is something weird here: notice that I sneakily dropped the term containing the lower and upper limits for $\theta$—this idea is, in fact, what saves the entire approach. What we will first do is the usual thing: we'll minimize the Lagrangian over all possible $z$, which we can easily do since the Lagrangian is a convex quadratic over $z$. In particular, taking the gradient over $z$ and setting it to zero (which is necessary and sufficient by convexity and differentiability) gives us that the optimal $z$ is
$$
z = \hat z - (A + \mathrm{diag(\theta)})^T\nu,
$$
which means that
$$
\inf_z \mathcal{L}(z, \theta, \nu) = - \frac12\left\|\hat z - (A + \mathrm{diag(\theta)})^T\nu\right\|\_2^2 - \nu^Tb + \frac12\|\hat z\|\_2^2.
$$
The next step is then finding the infimum of $\mathcal{L}$ over $\theta$. That is, finding
$$
\inf_\theta \left(\inf_z \mathcal{L}(z, \theta, \nu)\right).
$$
Now, of course, minimization over all $\theta$ is a lower bound (but not a very good one), since, unless $\nu = 0$, we can send the whole thing to negative infinity. (Why?)

What we can do instead is minimize over $\theta$, constrained to its feasible range, $\theta^\mathrm{min} \le \theta \le \theta^\mathrm{max}$. I'll leave it as an exercise for the reader as to why this is still a lower bound, but you should ponder this very carefully, because it is the main point of the paper. Take a peek at the proof above for why the Lagrangian is a lower bound in the first place. Of course, a second hint can be found in the paper which gives a somewhat-natural construction (sometimes called the "partial Lagrangian"), but I highly recommend sitting down with a bit of wine (or something stronger) and thinking about it![^wine]

If you've convinced yourself of this (or haven't yet, but want to continue), we now have the following minimization problem:
$$
\begin{aligned}
g(\nu) &= \inf_{\theta^\mathrm{min} \le \theta \le \theta^\mathrm{max}} \left(\inf_z \mathcal{L}(z, \theta, \nu)\right)\\\\
&= \inf_{\theta^\mathrm{min} \le \theta \le \theta^\mathrm{max}} \left(- \frac12\left\|\hat z - (A + \mathrm{diag(\theta)})^T\nu\right\|\_2^2 - \nu^Tb + \frac12\|\hat z\|\_2^2\right)
\end{aligned}
$$
The trick is to notice two things. One, that the objective is concave in $\theta$ and, two, that the objective is *separable* over each component of $\theta$. 

First off, let's say a function $v: \mathbb{R} \to \mathbb{R}$ is concave over the interval $[L, U]$, then it achieves its minimum value at the boundaries of the interval. Why? Well, the definition of concavity says, for every $0 \le \gamma \le 1$,
$$
f(\gamma L + (1- \gamma)U) \ge \gamma f(L) + (1-\gamma)f(U) \ge \min\\{f(L), f(U)\\}.
$$
but any point in the interval $[L, U]$ is a convex combination of $L$ or $U$! So every point inside of the interval is at least as large as the smallest endpoint of the interval, which completes the proof.

This solves our problem: since the objective is separable, then we only need to consider each component of $\theta$, and, because it's concave, then we know that an optimal $\theta_i$ is one of either $\theta^\mathrm{min}_i$ or $\theta^\mathrm{max}_i$. Replacing the complicated $\inf$ with this (much simpler) $\min$ gives the analytic solution for $g$:
$$
\begin{multline}
g(\nu) = \sum_i \min\bigg\\{-\frac12 (\hat z\_i - a\_i^T\nu + \theta\_i^\mathrm{min} \nu_i)^2, - \frac12 (\hat z\_i - a\_i^T\nu + \theta\_i^\mathrm{max} \nu_i)^2\bigg\\} \\\\- \nu^Tb + \frac12|\hat z|\_2^2,
\end{multline}
$$
or, writing it in the same way as the paper, by pulling out the $-1/2$,
$$
g(\nu) = -\frac12 \sum_i \max\bigg\\{ (\hat z\_i - a\_i^T\nu + \theta\_i^\mathrm{min} \nu_i)^2, (\hat z\_i - a\_i^T\nu + \theta\_i^\mathrm{max} \nu_i)^2\bigg\\} - \nu^Tb + \frac12|\hat z|\_2^2.
$$

## Results
The results are, of course, in the paper, but I'll give a quick summary.

For a relatively complex design, we found that a simple, commonly used heuristic finds a design with an objective value lying around 9% above the lower bound, and, therefore has objective value at most 9% above the best possible design. (In general, though, we suspect that the true optimum lies closer to the designs that the heuristics give than the lower bound we come up with.) In other words, it is physically impossible to improve upon the heuristic design more than marginally.



[^maxwell]: This is... almost accurate, but not quite. It turns out a small modification to the problem is needed for Maxwell's equations in two and three dimensions. For specifics, see the appendix in the paper.

[^wine]: Honestly, I *only* recommend reading this blog with wine (or whatever you have at hand). Not sure it's bearable, otherwise.