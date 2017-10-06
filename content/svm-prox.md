title: Proximal gradient for SVM
slug: svm-prox
category: optimization-methods
tags: machine-learning, math, optimization-methods
date: 2017-09-21
status: draft

For a class that's currently being written (*ahem*, EE104), Prof. Boyd posed an interesting problem of writing a (relatively general) proximal-gradient optimizer. The idea is that would act as a black-box way for students to plug in machine learning models of a specific form and have the optimizer do all of the hard work immediately, while appearing as transparent as possible.

This led to a rabbit hole of asking what loss functions should be included in the optimization package (huber, square, $\ell_1$, etc.), many of which are relatively straightforward to implement. Except, of course, SVM. Almost none of the other cases have much problems in implementation, since computing their proximal gradient is straightforward (e.g. $\ell_1$ corresponds immediately to a shrinkage operator), except that an SVM loss has a set of hard constraints which I haven't found a nice way of stuffing into the prox-gradient step (and I suspect that there are no such nice ways, but I'd love to be proven wrong, here); thus every step requires finding a projection into a polygon, which is, itself, a second optimization problem that has to be solved.

Prox gradients are (generally) really well-behaved and I've been having some fun trying to really understand how well they work as general optimizers.

## Proximal gradients
Proximal gradients are a nice idea emerging from convex analysis which provide useful ways of dealing with tricky, non-differentiable convex functions. For now, we define the proximal gradient of a function $g$ at some point $x$ (usually denoted $\text{prox}_g(x)$, though I will simply call it $P_g(x)$ for shorter notation) to be

$$
P_g(x) \equiv \mathop{\arg\\!\min}\limits_y \left(g(y) + \frac{1}{2}\lVert x- y\lVert_2^2\right)
$$

the definition is useful only because, if we allow $\partial g(u)$ to be the subdifferential of $g$ at $u$, then optimality guarantees that, if $y = P_g(x)$, then

$$
x - y \in \partial g(y).
$$

In other words, $0 \in \partial g(y)$ iff $y$ is a fixed point of $P_g$—that is, we have reached a minimizer of $g$ iff

$$
y = P_g(y)
$$

additionally, there's no weird trickery that has to be done with subdifferentials since the result of $P_g$ is always unique, which is a nice side-benefit. Using just this, we can already begin to do some optimization. For example, let's consider (the somewhat trivial, but enlightening) example of minimization of the $\ell_1$ norm. Using the fact that

$$
u = P_{\lambda |\cdot|}(x) \iff x - u \in \partial |u|
$$

and using the fact that the $\ell_1$ norm is separable, we have, whenever $u>0$ (I'm considering a single term of the sum, here)

$$
x - u = \lambda \implies u = x-\lambda\text{ whenever } x-\lambda > 0
$$

similarly for the $u=0$ case we have

$$
x - u = u \in \lambda [-1, 1] = [-\lambda, \lambda].
$$

that is

$$
u = 0\text{ whenever } |x|\le \lambda
$$

and similarly for the $u<0$ case, we have $u = x + \lambda$ if $x < -\lambda$. Since this is for each component, the final operator has action

$$
u_i = \begin{cases}
x_i - \lambda, & x_i > \lambda\\\\
0, & |x_i| \le \lambda \\\\
x_i + \lambda, & x_i < -\lambda
\end{cases}
$$

This operator is called the 'shrinkage' operator because of its action on its input: if $x_i$ is greater than our given $\lambda$, then we shrink it by that amount. Note then, that successively applying (in the same manner as SGD) the update rule

$$
u^{i+1} = P_{\lambda^{i+1} |\cdot|}(u^i)
$$

and having $\lambda^i$ be a sequence that isn't summable but has $\lambda_i \to 0$ (for example, $\lambda_i = 1/i$) then correctly yields the minimum of the given convex function, i.e. 0. Of course, this isn't particularly surprising since we already know how to optimize the $\ell_1$ norm function (just set it to zero!), but it will help out quite a bit when considering more complicated functions.

## Proximal gradient update
Now, given a problem of the form
$$
\min_x f(x) + g(x)
$$

where $f$ is differentiable, and $g$ is convex, we can write down a possible update in the same vein as the above, except that we now also update our objective for $f$ *and* $g$ at the same time
$$
u^{i+1} = P\_{\gamma^{i+1} g}(u^i - \gamma^{i+1}\nabla f(u^i)).
$$

It turns out we can prove several things about this update, but, perhaps most importantly, we can show that it works. Anyways, this is all I'll say about the proximal gradient step, here, since there are some good resources on the proximal gradient method around which will do a much better job of explaining it than I probably ever will: see [here](https://web.stanford.edu/~boyd/papers/pdf/prox_algs.pdf) for example.

## Optimizing SVM using proximal gradient
The usual quadratic program for an SVM is, where $\xi^\pm_i$ are the slack variables, $\varepsilon > 0$ is some arbitrary positive constant, and $\mu$ is the hyperplane and constant offset found by the SVM (e.g. by allowing the first feature of a positive/negative sample to be $(x^\pm_i)\_0 = 1$):

$$
\begin{aligned}
& \underset{\xi, \mu}{\text{minimize}}
& & \sum_i \xi^+\_i + \sum\_i \xi^-\_i + C\lVert \mu \lVert\_2^2 \\\\
& \text{subject to}
& & \mu^Tx^+\_i - \varepsilon \ge -\xi^+\_i,\,\,\text{ for all } i \\\\
&&& \mu^Tx^-\_i + \varepsilon \le \xi^-\_i,\,\,\text{ for all } i\\\\
&&& \xi^\pm_i \ge 0,\,\,\text{ for all } i
\end{aligned}
$$
