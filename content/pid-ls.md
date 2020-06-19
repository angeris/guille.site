title: PID as least squares
slug: pid-ls
category: least-squares
tags: control-theory, math, least-squares
date: 2017-09-13

I want to say this is a folk theorem (borrowing terminology from game theory) in that everyone who does optimal control theory knows about this stuff, probably,[^people] but I haven't really seen it stated explicitly anywhere. If anyone does indeed work on optimal control, I'd love to know your thoughts! (even if you don't, I'd still like to know your thoughts on it!)

For context, I'm currently leading a team on path planning for fixed-wing UAVs (I still don't really know who put me in charge of this stuff, or *why* for that matter---overall, it seems pretty terrifying for them, but kinda fun for me), and I wondered why I hadn't actually seen least squares in many papers on fixed-wing control. I still haven't gotten an answer to the question, to be honest, but I did waste some potentially productive time showing that PID $\subset$ LS. Some quick definitions: let $u(t)$ be our control input and allow $\varepsilon(t)$ to be the error of the function (that is, $\varepsilon(t) = x(t) - \hat x(t)$ where $x(t)$ is the desired position and $\hat x(t)$ is the current position), then a PID controller is defined as

$$
u(t) = K_p \varepsilon(t) + K_i \int_0^t d\tau\,\varepsilon(\tau) + K_d\frac{\partial\varepsilon(t)}{\partial t}
$$


where each of the $K_{(\cdot)}$ variables are a gain or proportionality constant. Say $K_p$ is the proportional constant (i.e. how much of $u$ is proportional to the current error), $K_i$ is the integral proportionality constant (i.e. how much of $u$ is proportional to the integral of the error), and $K_d$ is the derivative constant (i.e. ditto). For a more thorough explanation for what each of these means intuitively, see the [PID wikipedia page](https://en.wikipedia.org/wiki/PID_controller).

Anyways, I'll likely make a separate (more introductory) post to least squares but, for now, I define an LS problem to be an optimization problem of the form, for arbitrary but given $A, b, \lambda_j>0, C, d$

$$
\begin{aligned}
& \underset{u}{\text{minimize}}
& & \sum_j \lambda_j \lVert A_j u - b_j\lVert_2^2 \\
& \text{subject to}
& & Cu = d
\end{aligned}
$$

where the $\lVert \cdot \lVert_2^2$ norm is the usual $\ell_2$-norm (i.e. $\lVert x \lVert_2^2 = \sum_i x_i^2$). It's notable that this problem has an analytical solution (not that you'd necessarily *want* the analytical solution for most big-enough scenarios) and is extremely well-behaved for most optimization methods.[^politifact] Now, consider the following objective function with trivial equality constraints (e.g. $0=0$, for convenience, by setting $C = (0,0,…,0)^T,\, d = 0$) and $K$ being some proportionality constant (I'll make the connection to the original $K_{(\cdot)}$ variables above, soon):

$$
E(u, \varepsilon) = \lambda_p \left\lVert u - K\varepsilon (t)\right\lVert_2^2 + \lambda_i \left\lVert u - K\int d\tau\, \varepsilon(t)\right\lVert_2^2 + \lambda_d\left\lVert u - K \frac{\partial\varepsilon(t)}{\partial t}\right\lVert_2^2
$$

Minimizing this function by setting its gradient to zero (this is necessary and sufficient by differentiability, convexity, and coerciveness [that is, $E(u) \to \infty$, whenever $\lVert u\lVert \to \infty$]) gives the solution[^generalization]

$$
\nabla E(u, \varepsilon) = \lambda_p \left(u - K\varepsilon (t)\right) + \lambda_i \left( u - K\int d\tau\, \varepsilon(t)\right) + \lambda_d\left(u - K \frac{\partial\varepsilon(t)}{\partial t}\right) = 0,
$$

or, after rearranging

$$
u = \frac{K}{\lambda_p + \lambda_i + \lambda_d}\left(\lambda_p \varepsilon(t) + \lambda_i\int d\tau\, \varepsilon(t) + \lambda_d \frac{\partial\varepsilon(t)}{\partial t}\right),
$$

which allows the following correspondence between the original PID and the LS problem to be

$$
\begin{align}
K &= K_p + K_i + K_d\\
\lambda_p &= \frac{K_p}{K}\\
\lambda_i &= \frac{K_i}{K}\\
\lambda_d &= \frac{K_d}{K}.
\end{align}
$$

So, now we've given the condition we wanted and we're done!

Anyways, you may ask, why is this useful? I guess it kind of extends the framework to add constraints from your control surface, or secondary objectives. To be completely honest, though? I have no idea.

<!-- [^gametheory]: See, for example, (https://en.wikipedia.org/wiki/Folk_theorem_(game_theory)). -->

[^people]: I mostly know people who do hardware work, etc. on UAVs, so I don't really have a representative sample of control people.

[^politifact]: **PolitiFact**: *Mostly true.* I mean the usual cases (e.g. first-order methods, second-order methods, or conjugate gradient/quasi-newton methods). It's horribly behaved in conic program (SOCP) solvers.

[^generalization]: There's an immediate generalization here: any control of the form $\sum_i \gamma_i\left(u - C_i\right), \gamma_i>0$ can be immediately written as the minimizer to an energy function $E(u) = \sum_i \eta_i\lVert u - \xi C_i\lVert^2_2$. We can actually go further and note there's yet another generalization to any control of the form $\sum_i \left(S_iu - C_i\right)$, where each $S_i$ is symmetric and (strictly) positive definite. This is true as each $S_i$ has an inverse and a 'square root' matrix (e.g. let, $S$ be some positive-definite matrix. We know $SV =  V\Lambda$ for $V^TV = VV^T = I$ and diagonal $\Lambda > 0$, thus $S^{1/2}=V\Lambda^{1/2}V^T$), such that the energy function is written in terms of these. Though it's somewhat enlightening (I guess), I leave the derivation as an exercise for the reader.
