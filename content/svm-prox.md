title: Proximal gradient for SVM
slug: svm-prox
category: optimization-methods
tags: machine-learning, math, optimization-methods
date: 2017-12-22

For a class that's currently being written (*ahem*, EE104), Prof. Boyd posed an interesting problem of writing a (relatively general, but ideally simple) proximal-gradient optimizer. The idea is that would act as a black-box way for students to plug in machine learning models of a specific form and have the optimizer do all of the hard work immediately, while appearing as transparent as possible.

This led to a rabbit hole of asking what loss functions should be included in the optimization package (huber, square, $\ell\_1$, etc.), many of which are relatively straightforward to implement—except, of course, SVM. Almost all of the other cases have few problems in implementation, since computing their proximal gradient is a direct computation (e.g. $\ell\_1$ corresponds immediately to a [shrinkage operator](https://en.wikipedia.org/wiki/Proximal_gradient_methods_for_learning#Solving_for_%7F'"`UNIQ--postMath-0000002A-QINU`"'%7F_proximity_operator) as we'll see below), yet the SVM loss has a set of hard constraints which I haven't found a nice way of stuffing into the prox-gradient step (and I suspect that there are no such nice ways, but I'd love to be proven wrong, here); thus, every step requires finding a projection into a polygon, which is, itself, a second optimization problem that has to be solved.

Prox gradients are (generally) really well-behaved and I've been having some fun trying to really understand how well they work as general optimizers—I write a few of those thoughts below along with an odd solution to the original problem.

## Proximal gradients
Proximal gradients are a nice idea emerging from convex analysis which provide useful ways of dealing with tricky, non-differentiable convex functions. In particular, you can think of the proximal gradient of a given function as an optimization problem that penalizes taking steps "too far" in a given direction. Better yet (and perhaps one of the main useful points) is that most functions we care about have relatively nice proximal gradient operators!

Anyways, for now, let's define the proximal gradient of a function $g$ at some point $x$ (usually denoted $\text{prox}\_g(x)$, though I will simply call it $P\_g(x)$ for shorter notation) to be

$$
P\_g(x) \equiv \mathop{\arg\\!\min}\limits\_y \left(g(y) + \frac{1}{2}\lVert x- y\lVert_2^2\right)
$$

the definition is useful only because, if we allow $\partial g(u)$ to be the subdifferential of $g$ at $u$, then optimality guarantees that, if $y = P_g(x)$, then (by knowing that the subdifferential must be zero at the optimum) we have

$$
x - y \in \partial g(y).
$$

In other words, $0 \in \partial g(y)$ iff $y$ is a fixed point of $P_g$—that is, we have reached a minimizer of $g$ iff

$$
y = P_g(y).
$$

Additionally, there's no weird trickery that has to be done with subdifferentials since the result of $P\_g$ is always unique, which is a nice side-benefit. Using just this, we can already begin to do some optimization. For example, let's consider the (somewhat boring, but enlightening) example of minimization of the $\ell_1$-norm. Using the fact that

$$
u = P_{\lambda |\cdot|}(x) \iff x - u \in \partial |u|
$$

and using the fact that the $\ell_1$-norm is separable, we have, whenever $u>0$ (I'm considering a single term of the sum, here)

$$
x - u = \lambda \implies u = x-\lambda\text{ whenever } x-\lambda > 0
$$

similarly for the $u=0$ case we have (where $\lambda S$ for some set $S$ is just multiplication of every element in the set by $\lambda$)

$$
x - u = x \in \lambda [-1, 1] = [-\lambda, \lambda].
$$

that is

$$
u = 0\text{ whenever } |x|\le \lambda
$$

and similarly for the $u<0$ case, we have $u = x + \lambda$ if $x < -\lambda$. Since this is done for each component, the final operator has action

$$
u_i = \begin{cases}
x_i - \lambda, & x_i > \lambda\\\\
0, & |x_i| \le \lambda \\\\
x_i + \lambda, & x_i < -\lambda.
\end{cases}
$$

This operator is called the 'shrinkage' operator because of its action on its input: if $x_i$ is greater than our given $\lambda$, then we shrink it by that amount. Note then, that successively applying (in the same manner as SGD) the update rule

$$
u^{i+1} = P_{|\cdot|}(u^i)
$$

correctly yields the minimum of the given convex function, i.e. 0. Of course, this isn't particularly surprising since we already know how to optimize the $\ell\_1$-norm function, $\lVert x \lVert\_1$ (just set it to zero!), but it will help out quite a bit when considering more complicated functions.

## Proximal gradient update
Now, given a problem of the form
$$
\min_x f(x) + g(x)
$$

where $f$ is differentiable, and $g$ is convex, we can write down a possible update in the same vein as the above, except that we now also update our objective for $f$ *and* $g$ at the same time
$$
u^{i+1} = P\_{\gamma^{i+1} g}(u^i - \gamma^{i+1}\nabla f(u^i)).
$$

Here, $\gamma^i$ is defined to be the step size for step $i$. It turns out we can prove several things about this update, but, perhaps most importantly, we can show that it works.

Anyways, this is all I'll say about the proximal gradient step as there are several good resources on the proximal gradient method around which will do a much better job of explaining it than I probably ever will: see [this](https://web.stanford.edu/~boyd/papers/pdf/prox_algs.pdf) for example.

## Optimizing SVM using proximal gradient

### Initial problem
I assume some familiarity with SVMs, but the program given might require a bit of explanation. The idea of an SVM is as a soft-margin classifier (there are hard-magin SVMs, but we'll consider the former variety for now): we penalize the error of being on the wrong side of the decision boundary in a linear form (with zero penalty for being on the correct side of the decision boundary). The only additional thing is that we also require that the margin's size also be penalized such that it doesn't depend overly on a particular variable (e.g. as a form of regularization).

The usual quadratic program for an SVM is, where $\xi^\pm\_i$ are the slack variables indicating how much the given margin is violated, $\varepsilon > 0$ is some arbitrary positive constant, and $\mu$ is the hyperplane and constant offset found by the SVM (e.g. by allowing the first feature of a positive/negative sample to be $(x^\pm\_i)\_0 = 1$):

$$
\begin{aligned}
& \underset{\xi, \mu}{\text{minimize}}
& & \sum_i \xi^+\_i + \sum\_i \xi^-\_i + C\lVert \mu \lVert\_2 \\\\
& \text{subject to}
& & \mu^Tx^+\_i - \varepsilon \ge -\xi^+\_i,\,\,\text{ for all } i \\\\
&&& \mu^Tx^-\_i + \varepsilon \le \xi^-\_i,\,\,\text{ for all } i\\\\
&&& \xi^\pm_i \ge 0,\,\,\text{ for all } i
\end{aligned}
$$

we can rerwite this immediately, given that the class that our data point $i$ corresponds to is $y^{i}\in \\{-1, +1\\}$ to a much nicer form

$$
\begin{aligned}
& \underset{\xi, \mu}{\text{minimize}}
& & 1^T \xi + C\lVert \mu \lVert\_2 \\\\
& \text{subject to}
& & -y^i \mu^Tx\_i - \varepsilon \ge -\xi\_i,\,\,\text{ for all } i \\\\
&&& \xi\_i \ge 0,\,\,\text{ for all } i
\end{aligned}
$$

and noting that the objective is homogeneous of degree one, we can just multiply the constraints and all variables by $\frac{1}{\varepsilon}$ which yields the immediate result (after flipping some signs and inequalities)

$$
\begin{aligned}
& \underset{\xi, \mu}{\text{minimize}}
& & 1^T\xi + C\lVert \mu \lVert\_2 \\\\
& \text{subject to}
& & \xi\_i\ge y^i \mu^Tx\_i +1,\,\,\text{ for all } i \\\\
&&& \xi\_i \ge 0,\,\,\text{ for all } i
\end{aligned}
$$

which, after changing the $\ell\_2$ regularizer to an $\ell\_2^2$-norm regularizer (which is equivalent for approriate regularization hyperparameter, say $\eta$[^hyperparameter]) yields

$$
\begin{aligned}
& \underset{\xi, \mu}{\text{minimize}}
& & 1^T \xi + C\lVert \mu \lVert\_2^2 \\\\
& \text{subject to}
& & \xi\_i\ge y^i \mu^Tx\_i +1,\,\,\text{ for all } i \\\\
&&& \xi\_i \ge 0,\,\,\text{ for all } i.
\end{aligned}
$$

This is the final program we care about and the one we have to solve using our proximal gradient operator. In general, it's not obvious how to fit the inequalities into a step, so we have to define a few more things.

### Set indicators
For now, let's define the set indicator function
$$
g_S(x) = \begin{cases}
0 & x\in S\\\\
+\infty & x\not\in S
\end{cases}
$$
which is convex whenever $S$ is convex; we can use this to encode the above constraints (I drop the $S$ for convenience in what follows) such that a program equivalent to be above is

$$
\underset{\xi, \mu}{\text{minimize}} \,\, 1^T \xi + C\lVert \mu \lVert\_2^2 + g(\mu, \xi)
$$

which is exactly what we wanted! Why? Well:

$$
\underset{\xi, \mu}{\text{minimize}}\,\, \underbrace{1^T \xi + C\lVert \mu \lVert\_2^2}\_\text{differentiable} + \underbrace{g(\mu, \xi)}\_\text{convex}
$$

so now, we just need to find the proximal gradient operator for $g(x)$ (which is not as nice as one would immediately think, but it's not bad!).

### Proximal gradient of the linear inequality indicator
Now, let's generalize the problem a bit: we're tasked with the question of finding the prox-gradient of $g_S(x)$ such that $S$ is given by some set of inequalities $S = \\{x\,|\, Ax\le b\\}$ for some given $A, b$.[^equivalence] That is, we require

$$
\mathop{\arg\\!\min}\limits\_y \frac{1}{2\lambda}\lVert x- y\lVert\_2^2 + g\_S(y)
$$

which can be rewritten as the equivalent program (where the $1/2\lambda$ is dropped since it's just a proportionality constant)

$$
\begin{aligned}
& \underset{y}{\text{minimize}}
& & \lVert x- y\lVert\_2^2 \\\\
& \text{subject to}
& & Ay\le b
\end{aligned}
$$

it turns out this program isn't nicely solvable using the prox-gradient operator (since there's no obvious way of projecting onto $Ax\le b$ and *also* minimizing the quadratic objective). But, of course, I wouldn't be writing this if there wasn't a cute trick or two we could do: note that this program has a strong dual (i.e. the values of the [dual program](https://en.wikipedia.org/wiki/Duality_(optimization)) and the primal are equal) by [Slater's condition](https://en.wikipedia.org/wiki/Slater%27s_condition), so how about trying to solve the dual program? The lagrangian is

$$
\mathcal{L} = \lVert x- y\lVert\_2^2 + \gamma^T(Ay - b)
$$

from which we can derive the dual by taking derivatives over $y$:

$$
\nabla\mathcal{L} = y-x + A^T\gamma = 0 \implies y = x - A^T\gamma
$$

and plugging in the above (and simplifying) yields the program

$$
\begin{aligned}
& \underset{y}{\text{maximize}}
& & \eta^T(Ax-b) - \frac{1}{2}\lVert A^T\eta\lVert_2^2 \\\\
& \text{subject to}
& & \eta \ge 0
\end{aligned}
$$

from which we can reconstruct the original solution by the above, given:

$$
y = x - A^T\eta.
$$

This program now has a nice prox step, since $\left(P\_{\eta \ge 0}(\eta)\right)\_i = \max\\{0, \eta\_i\\}$ (the 'positive' part of $\eta_i$, in other words). This latter case is left as an exercise for the reader.

## Final Thoughts

Putting the above together yields a complete way of optimizing the SVM program: first, take a single step of the above objective, then find the minimum projection on the polygon over the given inequality constraints by using the second method, and then take a new step on the original, first program presented.

Of course, this serves as little more than an academic exercise (I'm not sure how thrilled either Boyd nor Lall would be at using dual programs in 104, even in a quasi-black-box optimizer), but it may be of interest to people who take interest in relatively uninteresting things (i.e. me) or to people who happen to have *really freaking fast* proximal gradient optimizers (not sure these exist, but we can pretend).

[^hyperparameter]: We're also finding this by using cross-validation, rather than a-priori, so it doesn't matter too much.

[^equivalence]: Note that this is equivalent to the original problem, actually. The forwards direction is an immediate generalization. The backwards direction is a little more difficult, but can be made simple by considering, say, only positive examples.