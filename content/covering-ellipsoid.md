title: The S-procedure and small covering ellipsoids
slug: covering-ellipsoid
category: convex-optimization
tags: math, control-theory, S-procedure
date: 2019-06-05

*Note:* This post was inspired by [Kunal Shah](https://msl.stanford.edu/people/kunal-shah)'s question that came up at some point during one of our meetings: is there an efficient way of finding an ellipsoid which covers the intersections and unions of a bunch of other ellipsoids?

While this question has been explored [somewhat](https://pdfs.semanticscholar.org/ab38/565f7957f7ee4980663324b5820b0a018de2.pdf) [extensively](http://www.optimization-online.org/DB_FILE/2018/07/6719.pdf), the exposition is often more general than necessary and aimed at a relatively mathematical audience. Either way, if you're interested, both papers are fairly well-written—I highly recommend at least a quick skim!

# The S-procedure

The [S-procedure](https://en.wikipedia.org/wiki/S-procedure) is a well known lemma in control theory that seeks to answer the following question:

Let's say we have a bunch of quadratic functions $f_0, f_1, f_2, \dots, f_n : \mathbb{R}^m \to \mathbb{R}$. When is it true that
$$
    f_i(x) \le 0 ~~ \text{for $i=1, \dots, n$} \implies  f_0(x) \le 0,
$$
for $x \in \mathbb{R}^m$? (Recall that a quadratic is a function of the form $f(x) = x^TPx + 2q^Tx + r$ for symmetric $P \in \mathbb{R}^{m\times m}$, $q \in \mathbb{R}^m$, and $r \in \mathbb{R}$).

There are many reasons to attempt to answer this (surprisingly useful) question. The original motivations were to show [stability of systems](https://stanford.edu/class/ee363/lectures/lmi-s-proc.pdf), though the domain of applications is certainly larger. We can use this to show anything from impossibility results (for example, many of the results of [this paper](https://arxiv.org/abs/1811.12936) can be recast in terms of the S-procedure) to, well, in our case, the construction of a small covering ellipsoid from a bunch of other ellipsoids, which is itself useful for things like filtering (for localizing drones from noisy measurements for example) along with many other applications.

If you're familiar with Lagrange duality, this is mostly an equivalent statement—except that this statement is in the special case of quadratics, where you can say a little more than with general functions.

## The $n=1$ case
We can fully and completely answer this question in the case that $n=1$: there exists a nonnegative number $\tau \ge 0$ such that
$$
    f_0(x) \le \tau f_1(x)
$$
for all $x$ if, and only if, $f_1(x) \le 0 \implies f_0(x) \le 0$.

Why? Well, let say we have a $\tau\ge 0$ that satisfies the above inequality. Then, if we have an $x$ such that $f_1(x) \le 0$, then
$$
f_0(x) \le \tau f_1(x) \le \tau0 = 0.
$$

The converse is slightly trickier, so I will defer to [B&V's *Convex Optimization*](http://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf) which has a very readable presentation of the proof (see B.1 and B.2 in the appendix).

## The general case
The general case is really only a slight change from the $n=1$ case (except that the converse of the statement is not true). In particular, if there exist $\lambda \ge 0$ such that
$$
    f_0(x) \le \sum_i \lambda_i f_i(x) ~~ \text{for all $x \in \mathbb{R}^m$},
$$
then, $f_i(x) \le 0 ~ \text{for} ~ i = 1, \dots, n \implies f_0(x) \le 0$. Showing this is nearly the same as the $n=1$ case,
$$
f_0(x) \le \sum_i \lambda_i f_i(x) \le \sum_i \lambda_i 0 = 0.
$$

So now we have a family of sufficient (but not necessary!) conditions for which we know when $f_i(x) \le 0 ~ \text{for} ~ i = 1, \dots, n$ implies that $f_0(x) \le 0$.

# Covering ellipsoids for unions

## Definitions and connections
Ellipsoids are a particularly nice family to work with since, as you may have guessed, they are the sets defined by
$$
\mathcal{E} = \{x \mid f(x) \le 0\},
$$
where $f: \mathbb{R}^m \to \mathbb{R}$ is a convex quadratic. This definition gives us a way of translating statements about sets (inclusion, etc) into statements about the functions which generate them. In particular, if we have two ellipsoids $\mathcal{E}, \mathcal{E}_0 \subseteq \mathbb{R}^n$ defined by the convex quadratics $f, f_0$, then
$$
\mathcal{E} \subseteq \mathcal{E}_0 \iff (f(x) \le 0 \implies f_0(x) \le 0).
$$
But wait a minute, we know exactly when this happens! By the previous section, we found that
$$
f(x) \le 0 \implies f_0(x) \le 0,
$$
if and only if there is some $\tau \ge 0$ with $f_0(x) \le \tau f(x)$. Also note that if we have a union of a bunch of ellipsoids (say $\mathcal{E}_1, \dots, \mathcal{E}_m$) that we want to cover with an ellipsoid $\mathcal{E}_0$, then this is the same as saying
$$
\mathcal{E}_i \subseteq \mathcal{E}_0, ~\text{for $i=1, \dots, m$},
$$
or, that each ellipsoid is covered by the big one, $\mathcal{E}_0$.

## Back to our goal
Ok, to reiterate, we are looking for a small ellipsoid $\mathcal{E}_0 = \{x \mid f_0(x) \le 0\}$ such that $\mathcal{E}_0$ contains all of the other ellipsoids $\mathcal{E}_i = \{x \mid f_i(x) \le 0\}$, where the $f_i$ and $f_0$ are convex quadratics. In other words, using the results of the previous subsection, we look for a quadratic $f_0$ such that
$$
(f_i(x) \le 0 \implies f_0(x) \le 0) ~~ \text{for each $i$}
$$
which we know happens only when there exists some $\tau_i \ge 0$ with
$$
f_0(x) \le \tau f_i(x) ~~ \text{for each $i$ and all $x$}.
$$
Now remains the final question: given two quadratics, $f_i$ and $f_0$ and some number $\tau \ge 0$, how can we check if $f_0(x) \le \tau f_i(x)$ for all $x$? I won't prove this (though I have written a quick proof of this statement in my notes, found [here](/notes/lmi-iff-quadratic-inequality.pdf)), but, if we let $f_i(x) = x^TP_ix + 2q_i^Tx + r_i$ and $f_0(x) = x^TP'x + 2(q')^Tx + r'$ then $f_0(x) \le f_i(x)$ for all $x$ if, *and only if*,
$$
\begin{bmatrix}
P' & q\\
(q')^T & r'
\end{bmatrix} \le \tau\begin{bmatrix}
P_i & q_i\\
q_i^T & r_i
\end{bmatrix},
$$
where we say two symmetric matrices $A, B$ satisfy $A \le B$ whenever $x^TAx \le x^TBx$ for all $x$. A straightforward exercise it to verify that the set of matrices $A \ge 0$ is a convex cone (almost universally called the positive semidefinite or PSD cone).

This rewriting is extremely useful, since we've turned a problem over a potentially difficult-to-handle space (the space of quadratics greater than or equal to another) into a problem that is easy to handle (the PSD cone). The best news, though, is that we have efficient algorithms to solve optimization problems whose constraints are PSD constraints.[^lmi-book]

## Corresponding optimization problem
Finally, after enough background, we can get to the final goal: writing an efficiently-solvable optimization problem to give us a small bounding ellipsoid.

There are several ways of defining "small," in the case of ellipsoids, but one of the most common definitions is to pick the ellipsoid with the smallest volume. In the case that $\mathcal{E}_0 = \{x \mid x^TP'x + 2(q')^Tx + r \le 0\}$, the *volume* of this ellipsoid is given by the determinant, $\mathop{\mathrm{det}} P'$, of the matrix $P'$. So, we can write—using the conditions given above—an optimization problem corresponding to finding the smallest (in volume) ellipsoid $\mathcal{E}_0$ which contains all ellipsoids, $\mathcal{E}_i$ as
$$
\begin{aligned}
& \underset{P', q', r', \tau}{\mathrm{minimize}}
& & \mathop{\mathrm{det}} P'  \\
& \text{subject to}
& & \begin{bmatrix}
P' & q\\
(q')^T & r'
\end{bmatrix} \le \tau_i\begin{bmatrix}
P_i & q_i\\
q_i^T & r_i
\end{bmatrix}, \quad i = 1, \dots, n.
\end{aligned}
$$
The only problem here (which we can easily fix) is that the determinant is not a convex function. On the other hand, the *log* determinant *is* (for a proof, see the [Convex book](https://web.stanford.edu/~boyd/cvxbook/), section 3.1.5), so we can write,
$$
\begin{aligned}
& \underset{P', q', r', \tau}{\mathrm{minimize}}
& & \log \mathop{\mathrm{det}} P'  \\
& \text{subject to}
& & \begin{bmatrix}
P' & q\\
(q')^T & r'
\end{bmatrix} \le \tau_i\begin{bmatrix}
P_i & q_i\\
q_i^T & r_i
\end{bmatrix}, \quad i = 1, \dots, n.
\end{aligned}
$$
This is equivalent to the original problem since $\log(y)$ is an increasing function of $y$. 

Of course, any convex function (such as, for example the trace) would do here as well.

# Covering ellipsoids for intersections and unions
Ok, now we know how to solve the problem where we have a bunch of ellipsoids and we want to find an ellipsoid which covers all of them. How about the problem where we want to find an ellipsoid which also covers the sets $\{N_i\}$ for $i=1, \dots, k$, which are, themselves, intersections of ellipsoids?

In particular, if $N_i$ is defined as
$$
N_i = \bigcap_{j \in I_i} \mathcal{E}_j,
$$
for some index set $I_i \subseteq \{1, \dots, n\}$ and some set of ellipsoids $\{\mathcal{E}_j\}$, each of which are defined as before ($\mathcal{E}_j = \{x \mid f_j(x) \le 0 \}$), we can perform a similar trick to the one above!

More generally, if we have an ellipsoid $\mathcal{E}_0 = \{x \mid f_0(x) \le 0\}$, then
$$
N_i \subseteq \mathcal{E}_0 \iff (f_j(x) \le 0 ~~ \text{for $j \in I_i$} \implies f_0(x) \le 0).
$$
(It's a worthwhile exercise to think about why, but it follows the same idea as before.) In other words, $\mathcal{E}_0$ is a superset of $N_i$ only when *a bunch of quadratic inequalities imply another*. (Where have we seen this before...?)

In other words, we know that (by the first section), if there exist $\lambda \ge 0$ such that
$$
f_0(x) \le \sum_{j \in I_i} \lambda_{j} f_j(x),
$$
then we immediately have that $N_i \subseteq \mathcal{E}_0$. Since the converse is not true, we are sadly not guaranteed to actually find the smallest bounding ellipsoid $\mathcal{E}_0$, but this is usually quite a good approximation (if it's not exact).

Following exactly the same steps as in the previous section and using the same definitions, we now get a new program for minimizing the volume for the union and intersection of ellipsoids:
$$
\begin{aligned}
& \underset{P', q', r', \lambda}{\mathrm{minimize}}
& & \log \mathop{\mathrm{det}} P'  \\
& \text{subject to}
& & \begin{bmatrix}
P' & q\\
(q')^T & r'
\end{bmatrix} \le \sum_{j \in I_i}\lambda_{ij}\begin{bmatrix}
P_i & q_i\\
q_i^T & r_i
\end{bmatrix}, \quad i = 1, \dots, k \\
&&& \lambda_{ij} \ge 0, \quad i=1, \dots, k, ~~ j \in I_i.
\end{aligned}
$$
As before, this program does not guarantee actually finding the minimal volume ellipsoid, but it is likely to be quite close! (That is, if it's not spot on, most of the time.)

[^lmi-book]: For more information, see Boyd's [Linear Matrix Inequalities](https://web.stanford.edu/~boyd/lmibook/) book.
