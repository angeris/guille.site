title: Machine learning, information, and tail bounds
slug: ml-information-bounds
category: machine-learning
tags: statistics, math, information-theory
date: 2018-09-04

Usually, in explaining the connection between information theory and machine learning, I would begin by writing down the definition of entropy and deriving some useful results about it, and then come back to tell you that you can look at ML as an information problem, where nature picks some parameters and 'communicates them' through a noisy channel (e.g. via samples from some distribution or some other stochastic process), which you then have to infer (i.e., decode). While this approach is common, my explanations are likely to be far worse than [the](http://www.cs.cmu.edu/~aarti/Class/10704_Spring15/lecs.html) [many](https://www.princeton.edu/~eabbe/publications/tuto_slides_part1.pdf) [available](http://www.inference.org.uk/itprnn/book.pdf) [texts](https://web.stanford.edu/~montanar/RESEARCH/book.html). So I'll try to do something mildly differently (and perhaps a bit backwards) and hope it's at least somewhat entertaining and, ideally, do it all without assuming much more than some comfort with statistics (e.g. the [weak law](https://en.wikipedia.org/wiki/Law_of_large_numbers#Weak_law) and [Markov's inequality](https://en.wikipedia.org/wiki/Markov%27s_inequality)).

## Maximum-likelihood and KL-divergence
The maximum-likelihood estimator (MLE) is probably the simplest estimator, if you have a probability distribution $p(x|\theta)$ which models your data. In this case we try to pick the hypothesis $\theta$ which makes our observed data the most likely. In other words, we want to solve the optimization problem:
$$
\theta^\mathrm{MLE} = \underset{\theta}{\operatorname{argmax}}~~p(x~|~\theta).
$$
While this framework is quite general, we'll prove that this estimator is [consistent](https://en.wikipedia.org/wiki/Consistent_estimator) in the case where our data points, $x = \\{x^i\\}$, are all independently drawn from $p(\cdot ~|~ \theta^\*)$, where $\theta^\*$ is the "true" hypothesis. In other words, when
$$
p(x~|~\theta) = \prod_i p(x^i~|~\theta)
$$

The proof that this estimator is consistent is relatively simple and assumes only the [weak law of large numbers](https://en.wikipedia.org/wiki/Law_of_large_numbers#Weak_law), which says that the empirical mean of a bunch of i.i.d variables $\{Y_i\}$ converges[^in-probability] to its expectation
$$
\frac{1}{n}\sum_i Y_i \overset{p}{\to} \mathbb{E}[Y_1].
$$
(from here on out, I will write 'converges in probability' just as $\to$, instead of $\overset{p}{\to}$).

First, note that[^trick]

$$
\underset{\theta}{\operatorname{argmax}}\left(\prod_i p(x^i~|~\theta)\right) = \underset{\theta}{\operatorname{argmax}}\left(\log \left(\prod_i p(x^i~|~\theta)\right)\right),
$$
since $0 < x \le y \iff \log(x) \le \log(y)$ (i.e. $\log$ is monotonic[^monotonicity], so it preserves any maximum or minimum). We also have
$$
\log \left(\prod_i p(x^i~|~\theta)\right) = \sum_i \log p(x^i ~|~ \theta),
$$
and now we need some way of comparing the current hypothesis $\theta$, with the true hypothesis $\theta^\*$. The simplest way is to subtract one from the other and show that the difference is less than zero whenever $\theta \ne \theta^\*$, so this is what we will do.[^sneaky] In particular:
$$
\sum_i \log  p(x^i~|~\theta) - \sum_i \log p(x^i~|~\theta^\*) = \sum_i \log\left(\frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)}\right).
$$

If we can prove the quantity above is negative with high probability, then we're set! So divide by $n$ on both sides and note that, by the weak law, we have
$$
\frac{1}{n}\sum_i \log\left(\frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)}\right) \to \mathbb{E}_{X}\left(\log\left(\frac{p(X~|~\theta)}{p(X~|~\theta^\*)}\right)\right).
$$
(the expectation here is taken with respect to the true distribution $p(\cdot ~|~\theta^\*)$). Now, $\log(x)$ is a concave function (proof: take the second derivative and note that it's always negative), so, this means that
$$
\mathbb{E}(\log(Y)) \le \log(\mathbb{E}(Y)),
$$
for any random variable $Y$ (this is [Jensen's inequality](https://en.wikipedia.org/wiki/Jensen%27s_inequality)). In fact, in this case, equality can only happen if $Y$ takes on a single value, so in general, we have
$$
\mathbb{E}(\log(Y)) < \log(\mathbb{E}(Y)).
$$

Applying this inequality to the previous line is the only magical part of the proof, which gives us
$$
\begin{aligned}
\mathbb{E}\_{X}\left(\log\left(\frac{p(X~|~\theta)}{p(X~|~\theta^\*)}\right)\right) &< \log\mathbb{E}\_{X}\left(\frac{p(X~|~\theta)}{p(X~|~\theta^\*)}\right) \\\\
&= \log \int_S p(X~|~\theta^\*)\frac{p(X~|~\theta)}{p(X~|~\theta^\*)}~dX\\\\
&= \log \int_S p(X~|~\theta)~dX\\\\
&= \log 1\\\\
&= 0.
\end{aligned}
$$

So, as $n \uparrow\infty$, we find that
$$
\frac{1}{n}\sum_i \log\left(\frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)}\right) < 0
$$
or, multiplying by $n$ and rearranging,
$$
\sum_i \log p(x^i~|~\theta) < \sum_i \log p(x^i~|~\theta^\*)
$$
with high probability. So, any point which is not $\theta^\*$ will have a lower likelihood than $\theta^\*$.[^immediate-bounds]

## Tail bounds on information
The next question, of course, is how many samples do we need to actually guess the right hypothesis? There are several ways of attacking this question, but let's start with a basic one: what is the probability that a wrong (empirical) likelihood is actually better than the true empirical likelihood? In other words, can we give an upper bound on
$$
P\left(\prod_i p(x^i~|~\theta) \ge \prod_i p(x^i~|~\theta^\*)\right)
$$
that depends on some simple, known quantities? Applying [Markov's inequality](https://en.wikipedia.org/wiki/Markov%27s_inequality) directly yields the trivial result
$$
P\left(\prod_i \frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)} \ge 1\right) \le \mathbb{E}_x\left(\prod_i \frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)}\right) = 1,
$$
that the probability is at most 1. So where do we go from here? Well, as before, we can turn the product into a sum by taking the log of both sides and dividing by $n$ (déjà vu, anyone?),
$$
P\left(\prod_i \frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)} \ge 1\right) = P\left(\frac1n\sum_i \log\left( \frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)}\right) \ge 0\right).
$$
Here, we can weaken the question a little bit by asking: how likely is it that our wrong hypothesis has a higher log-likelihood than the right one *by any amount*, $\varepsilon > 0$. In other words, let's give a bound on
$$
P\left(\frac1n\sum_i \log\left( \frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)}\right) \ge \varepsilon\right).
$$

Here comes a little bit of magic, but this is a general method in what are known as Chernoff bounds. It's a good technique to keep in your toolbox if you haven't quite seen it before!

Anyways, since $\log$ is a monotonic function, note that $\exp$ (its inverse) is also monotonic, so,
$$
P\left(\frac{1}{n}\sum_i \log\left(\frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)}\right) \ge \varepsilon\right) = P\left(\exp\left\\{\sum_i \log\left( \frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)}\right)\right\\} \ge e^{n\varepsilon}\right),
$$
and applying Markov's inequality to the right-hand-side yields
$$
P\left(\exp\left\\{\sum_i \log\left(\frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)}\right)\right\\} \ge e^{n\varepsilon}\right) \le e^{-n\varepsilon},
$$
so as the number of samples increases, our wrong hypothesis becomes exponentially unlikely to exceed the true hypothesis by more than $\varepsilon$.

Of course, at any point in this proof, we could've multiplied both sides of the inequality by $\lambda > 0$ and everything would've remained true, but note that then we would have a bound
$$
P\left(\frac1n\sum_i \log\left( \frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)}\right) \ge \varepsilon\right) \le \mathbb{E}_X\left[\left(\frac{p(X ~|~ \theta)}{p(X~|~\theta^\*)}\right)^\lambda\right]~ e^{-\lambda n\varepsilon},
$$
which looks almost nice, except that we have no control over the tails of 

$$
\left(\frac{p(X ~|~ \theta)}{p(X~|~\theta^\*)}\right)^\lambda,
$$

since at no point have we assumed anything about the dependence of $p$ on $\theta$ or $X$ (apart from it being a correct probability distribution). More generally speaking, given $\lambda \ne 0, 1$, we can find a function such that this quantity blows up (exercise for the reader!), which makes our bound trivial.

It is possible to make some assumptions about how these tails behave, but it's not entirely clear that these assumptions would be natural or useful. If anyone has further thoughts on this, I'd love to hear them!

## On Fisher Information and Lower-Bounds
The second set of lower-bounds that are easy to derive and are surprisingly useful are the Cramér-Rao bounds on estimators. In particular, we can show that, for any estimator $\hat \theta$ whose expectation is $\mathbb{E}(\hat \theta) = \psi(\theta)$, with underlying probability distribution $p(\cdot~|~\theta)$, then[^dimensions]
$$
\operatorname{Var}(\theta) \ge \frac{[\psi ' (\theta)]^2}{I(\theta)},
$$
where $I(\theta) \ge 0$ is the Fisher information of $p(\cdot~|~\theta)$, which is something like the local curvature of $\log p(\cdot~|~\theta)$ around $\theta$. In particular, it is defined as
$$
I(\theta) = -\mathbb{E}_X\left(\frac{\partial^2 \log p(X~|~\theta)}{\partial \theta^2}\right).
$$
In other words, the inequality says that, the more flat $\log p$ is at $\theta$, the harder it is to correctly guess the right parameter. This makes sense, since the flatter the distribution is at this point, the harder it is for us to distinguish it from points around it.

I'll give a simple proof of this statement soon (in another post, since this one has become quite a bit longer than expected), but, to see why this makes sense, let's go back to the original proof of the consistency of the MLE estimator for a given probability distribution. Note that assuming that $\psi(\theta) = \theta$ then gives us bounds on the variance of an unbiased estimator of $\theta$.

At one point we used the fact that
$$
\frac{1}{n}\sum_i \log\left(\frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)}\right) \to \mathbb{E}\_{X}\left(\log\left(\frac{p(X~|~\theta)}{p(X~|~\theta^\*)}\right)\right) \equiv -D(\theta ~\Vert~\theta^\*) \le 0.
$$
This quantity on the right is called the [KL-divergence](https://en.wikipedia.org/wiki/Kullback–Leibler_divergence), and it has some very nice information-theoretic interpretations, which I highly recommend you read about, but which I will not get into here. Anyways, assuming that $\theta$ is close to $\theta^\*$, we can do a Taylor expansion around the true parameter $\theta^\*$ to find

$$
\frac{1}{n}\sum_i \log\left(\frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)}\right) \approx \frac{1}{n}\sum_i \left(\underbrace{\log\left(\frac{p(x^i~|~\theta^\*)}{p(x^i~|~\theta^\*)}\right)}\_{=0} + (\theta - \theta^\*)\frac{\partial\_\theta p(\cdot ~|~\theta^\*)}{p(\cdot ~|~ \theta^\*)} + \dots\right)
$$
and the quantity on the right hand side goes to, as $n\uparrow \infty$,
$$
\begin{aligned}
\frac{1}{n}\sum_i \left((\theta - \theta^\*)\frac{\partial\_\theta p(\cdot ~|~\theta^\*)}{p(\cdot ~|~ \theta^\*)} + O((\theta - \theta^\*)^2)\right) &\to (\theta - \theta^\*)\mathbb{E}\_X\left(\frac{\partial\_\theta p(X ~|~\theta^\*)}{p(X ~|~ \theta^\*)}\right) \\\\
&= (\theta - \theta^\*)\int_S \frac{\partial_\theta p(X~|~\theta^\*)}{p(X~|~\theta^\*)}p(X~|~\theta^\*)~dX\\\\
&=(\theta - \theta^\*)\int_S \partial_\theta p(X~|~\theta^\*)~dX\\\\
&=(\theta - \theta^\*)\partial_\theta\left(\int_S p(X~|~\theta^\*)~dX\right)\\\\
&= (\theta - \theta^\*)\partial_\theta (1)\\\\
&= 0
\end{aligned}
$$
...zero?![^dominated-convergence] Well, the expectation of the first derivative of the log-likelihood vanishes, so taking the second term in the Taylor expansion yields
$$
\frac{1}{2}(\theta - \theta^\*)^2\mathbb{E}\_X\left(\partial_\theta^2 \log(p(X~|~\theta^\*)\right)) = -\frac12(\theta - \theta^\*)^2I(\theta^\*).
$$

Putting it all together, we have that
$$
\frac{1}{n}\sum_i \log\left(\frac{p(x^i~|~\theta)}{p(x^i~|~\theta^\*)}\right) \to -D(\theta \Vert \theta^\*) \approx -\frac12(\theta - \theta^\*)^2I(\theta^\*) + O((\theta - \theta^\*)^3),
$$
or that the curvature of the KL-divergence around $\theta^\*$ is the Fisher information! In this case, it shouldn't be entirely surprising that there is some connection between how well we can measure a parameter's value and the Fisher information of that parameter, since the likelihood's noise around that parameter is given by the Fisher information.

On the other hand, I haven't been able to find a direct proof of the above bound (or, even, any other nice bounds) given *only* the above observation. So, while the connection might make sense, it turns out the proof of the Cramér-Rao bound uses a slightly different technique, which I will present later (along with some other fun results!).


[^in-probability]: In probability. I.e., the probability that the empirical mean differs from the expectation by some amount, $\left|\frac{1}{n}\sum_i Y_i - \mathbb{E}[Y_1]\right| > \varepsilon$, goes to zero as $n\uparrow \infty$. A simple proof in the finite-variance case follows from Chebyshev's inequality (exercise for the reader!).

[^trick]: It's often easier to deal with log-probabilities than it is to deal with probabilities, so this trick is relatively common.

[^monotonicity]: In fact, the logarithm is *strictly* monotonic, so it preserves minima uniquely. In other words, for any function $\phi: S\to \mathbb{R}^{> 0}$, $\phi$ and $\log \circ\, \phi$ have minima and maxima at exactly the same points.

[^sneaky]: I am, of course, being sneaky: the subtraction *happens* to work since this just *happens* to yield the KL-divergence in expectation—but that's how it goes. Additionally, the requirement really is not that $\theta \ne \theta^\*$, but rather that $p(x~|~\theta^\*) \ne p(x~|~\theta)$, just in case there happen to be multiple hypotheses with equivalent distributions. Since you're reading this then just assume throughout that $p(\cdot~|~\theta) \ne p(\cdot~|~\theta^\*)$ on some set with nonzero probability (in the base distribution) whenever $\theta \ne \theta^\*$.

[^immediate-bounds]: While it may seem that there should be easy bounds to give immediately based on this proof, the problem is that we do *not* have good control of the second moment of $\log(p(\cdot~|~\theta^\*)/p(\cdot~|~\theta))$ (this quantity may not even converge in a nice way). This makes giving any kind of convergence rate quite difficult, since the proof of the weak law given only a first-moment guarantee uses the dominated convergence theorem to give non-constructive bounds.

[^dimensions]: This is a derivation of the one-dimensional case, but the $n$-dimensional case is almost identical.

[^dominated-convergence]: All I will say about changing the derivative and integral around is that it is well-justified by dominated convergence.