title: PCA as a convex optimization problem
slug: pca-convex
category: convex-optimization
tags: math, pca, non-convex, convex
date: 2018-05-16

It's been a while since I last posted (my posting has been less once every two weeks and more like one every two months), but here's a post I've been sitting on for a while that I never got around to finishing. As per [rachelbythebay's advice](https://rachelbythebay.com/w/2018/03/13/write/), I decided to just finish it and post it up. It's likely to be a little rough, but feel free to [tweet](https://twitter.com/GuilleAngeris) any questions or things that you'd like more fleshed out (as usual!).

## Quick introduction to PCA

Most people know [Principal Component Analysis](https://en.wikipedia.org/wiki/Principal_component_analysis) (PCA) as a fast, and easily-scalable dimensionality-reduction technique used quite frequently in machine learning and data exploration—in fact, it's often mentioned that one-layer, linear neural network[^loss-type] applied on some data-set recovers the result from PCA.

It's (also) often mentioned that PCA is one of the [few non-convex problems that we can solve efficiently](https://groups.google.com/forum/#!topic/10725-f12/P9e8BsqaAok), though a (let's say 'non-constructive') answer showing this problem is convex is given in [this Stats.SE thread](https://stats.stackexchange.com/questions/301532/is-pca-optimization-convex), which requires knowing the eigenvectors of $X^TX$, a priori. It turns out it's possible to create a fairly natural semi-definite program which actually constructs the solution in its entirety.

Since I'll only give a short overview of the topic of PCA itself, I won't go too much into depth on methods of solving this. But, the general idea of PCA is to find the best low-rank approximation of a given matrix $A$. In other words, we want, for some given $k$:

$$
\begin{aligned}
& \underset{X}{\text{minimize}}
& & \\| A - X \\|_F^2  \\\\
& \text{subject to}
& & \text{rank}(X) = k,
\end{aligned}
$$

where $\\| B \\|_F^2$ is the square of the Frobenius norm of $B$ (i.e. it is the sum of the squares of each entry of $B$). Why is this useful? Well, in the general formulation, we can write the SVD decomposition of some optimal $X^\* \in \mathbb{R}^{m\times n}$,

$$
X^\* = U^\*\Sigma^\* (V^\*)^T
$$

with orthogonal $U^\* \in \mathbb{R}^{m\times k}, V^*\in \mathbb{R}^{n\times k}$ and diagonal $\Sigma^\* \in \mathbb{R}^{k\times k}$. Then the columns of $V^\*$ represent the $k$ most important features of $A$ (assuming that each row of $A$ ia a point of the dataset). This may seem slightly redundant if you already know the punchline, but we'll get there in a second. 

For now, define the SVD of $A$ in a similar way to the above

$$
A = U\Sigma V^T.
$$

with orthogonal $U, V$ and diagonal $\Sigma$.

For convenience, it's easiest to define the diagonal of $\Sigma$ (the singular values of $A$) to be sorted with the top-left value being the largest and bottom-right value being the smallest. Then let $U_k$ be the matrix which contains only the first $k$ columns of $U$ (and similarly for $V_k$), while $\Sigma_k$ is the $k$ by $k$  diagonal sub-matrix of $\Sigma$ containing only the first $k$ values of the diagonal (as usual, starting from the top left).

Now we can get to the punchline I was talking about earlier: it turns out that the SVD of $X^\*$ is the *truncated* SVD of $A$, in other words, if the SVD of $A$ is $U\Sigma V^T$, then the optimal solution is

$$
X^\* = U_k\Sigma_kV_k^T.
$$

This is the usual way of computing the PCA decomposition of $A$: simply take the SVD and then look at the first $k$ columns of $V$.[^truncated-svd] We'll make use of this fact to show that the optimal values are equal, but it won't be necessary to actually *compute* the result.

## Construction of the SDP

In general, semi-definite programs (i.e. optimization over symmetric, positive-semidefinite matrices with convex objectives and constraints) are convex problems. Here, we'll construct a (relatively) simple reduction of the non-convex problem of PCA, as presented above, to the SDP.

### Quick overview of method

This entire idea was interesting to me, since it was mentioned in [this lecture](http://www.stat.cmu.edu/~ryantibs/convexopt-S15/scribes/26-nonconvex-scribed.pdf) which was a result I didn't know about. There aren't any complete proofs of this online, other than a quick mention in [Vu, et al. (2013)](https://papers.nips.cc/paper/5136-fantope-projection-and-selection-a-near-optimal-convex-relaxation-of-sparse-pca), though it's not hard to show the final result given the general ideas. I highly encourage you to try the proof out after reading only the main ideas, if you're interested!

First, we'll start with the usual program, call it *program Y*:

$$
\begin{aligned}
& \underset{X}{\text{minimize}}
& & \\| A - X \\|_F^2  \\\\
& \text{subject to}
& & \text{rank}(X) = k,
\end{aligned}
$$

and construct the equivalent program (this step can be skipped with a cute trick below), with $F = A^TA$,

$$
\begin{aligned}
& \underset{P}{\text{minimize}}
& & \\| F - P \\|_F^2  \\\\
& \text{subject to}
& & \text{rank}(P) = k,\\\\
&&& P^2 = P,\\\\
&&& P^T = P,
\end{aligned}
$$

in other words, this is a program over projection matrices $P$. This can then be put into the form

$$
\begin{aligned}
& \underset{P}{\text{minimize}}
& & \text{tr}(FP)  \\\\
& \text{subject to}
& & \text{rank}(P) = k,\\\\
&&& P^2 = P,\\\\
&&& P^T = P.
\end{aligned}
$$

for some matrix $F$, and it can be relaxed into the following SDP, let's call it *problem Z*,

$$
\begin{aligned}
& \underset{P}{\text{minimize}}
& & \text{tr}(FP)  \\\\
& \text{subject to}
& & \text{tr}(P) = k,\\\\
&&& 0\preceq P \preceq I,
\end{aligned}
$$

where $A \preceq B$ is an inequality with respect to the semi-definite cone (i.e. $A \preceq B \iff B - A$ is positive semi-definite). You can then show that this SDP has *zero integrality gap* with the above program over the projection matrices. More specifically, any solution to the relaxation can be easily turned into a solution of the original program.

Just a random side-note: if you took or followed Stanford's EE364A course for the previous quarter (Winter 2018), the latter part of this proof idea may seem familiar—it was a problem written for the final exam. My original intent with it was to guide the students through the complete proof, but better judgement prevailed and the question was cut down to only that last part with some hints.

## Complete (if somewhat short!) steps
The two interesting points of the whole proof are (a) to realize that any solution of the original problem (program Y) can be written as a solution $X = AP'$ for some projection matrix $P'$ (which, of course, will turn out to be the projection matrix $P$ which solves program Z, namely $P' = V\_kV\_k^T$), and (b) to note that we can prove that program Z has zero integrality gap since, if we have a solution to the SDP given by $P^* = UDU^T$, then we can 'fix' non-integral eigenvalues via solving the problem

$$
\begin{aligned}
& \underset{x}{\text{minimize}}
& & c^Tx  \\\\
& \text{subject to}
& & 1^Tx = k,\\\\
&&& 0\le x_i \le 1, ~~\forall i,
\end{aligned}
$$

where $c\_i = (U^TAU)\_{ii}$. This LP has an integral solution $x^\*$ (what should this solution be?) which preserves the objective value of the original problem, so $\bar P^\* = U\text{diag}(x^*)U^T$ is a feasible, integral solution to the original problem, with the same objective value as the previous so the SDP relaxation is tight!

Using all of this, then we've converted the PCA problem into a purely convex one, without computing the actual solution beforehand.

[^loss-type]: More specifically, a one-layer, linear NN with $\ell_2$ loss.

[^truncated-svd]: As usual, there are smarter ways of doing this. It turns out one can run a truncated or partial SVD decomposition, which doesn't require constructing all singular values and all the columns of $U, V$. This is far more efficient whenever $k\ll \min\\{m, n\\}$, where $m,n$ are the dimensions of the data. This latter condition is usually the case for practical purposes.