title: Markov processes and the second law
slug: second-law-markov
category: math
tags: statistics, math, information-theory, physics, quick-post
date: 2018-09-13

*Note:* This is another one of those "quick" posts about a topic I've found to be fascinating, but which is almost never discussed.

Physics has this nice little law called the [second law of thermodynamics](https://en.wikipedia.org/wiki/Second_law_of_thermodynamics), which governs every physical thermodynamical system in question. The second law is usually phrased as the nice quote "everything tends to disorder," or some other variation thereof which sounds intuitive but is as opaque as a concrete wall when applied in practice.

As usual, I won't really touch this or other similar discussions with a 10 foot pole (though [here](https://plato.stanford.edu/entries/time-thermo/) is a good place to start), but I'll be giving some thoughts on a similar mathematical principle which arises from statistical systems.

## Markov chains

Since this is a short post, I won't be describing [Markov chains](https://en.wikipedia.org/wiki/Markov_chain) in detail, but as a refresher, a Markov chain (or Markov process) is a process in which the next state of the process depends only on the current state. In other words, it's a little like the game [Snakes and Ladders](https://en.wikipedia.org/wiki/Snakes_and_Ladders), where your next position depends only on where you are in the current square and your next dice throw (independent of it being the 1st or 5th time you've landed on the same square).

In particular, we know probability of being at a new square, $x_{t+1}$ at time $t+1$, given that we were in square $x_t$ at time $t$. In other words, we know $p(X_{t+1}=x~|~X_{t}=x')$. Similarly, if we weren't sure of our position at time $t$, but rather we have a probability distribution over positions, say $p(X_t = x)$ (which I will call $p_t(x)$, for convenience), then the probability of being at position $x$ at time $t+1$ given our belief about possible positions, $x'$ at time $t$ is
$$
p_{t+1}(x) = \sum_{x'} p(X_{t+1}=x~|~X_{t}=x')p_t(x').\tag{1}
$$

In other words, we just multiply these two probabilities and sum over all possible states $x'$ at time $t$. The defining trait of (stationary) Markov processes is that $p(X_{t+1}=x~|~X_{t}=x')$, which I will call $K(x, x')$ from now on, is the *same* for all $t$, and equation (1), now written as
$$
p_{t+1}(x) = \sum_{x'} K(x, x')p_t(x),
$$
holds for any $t$.

It's probably not hard to believe that Markov chains are used [absolutely](https://www.cs.cmu.edu/~katef/DeepRLControlCourse/lectures/lecture2_mdps.pdf) [everywhere](https://twitter.com/captain_markov?lang=en), since they make for mathematically simple, but surprisingly powerful models of,  well, everything.

This is all I will mention about Markov chains, in general. If you'd like a bit of a deeper dive, [this blog post](http://setosa.io/ev/markov-chains/) is a beautiful (and interactive!) reference. I highly recommend it.

## A variation on a theme

Let $p_t$ be the distribution of a process at time $t$, then the second law says that (and I will use statistics notation, rather than physics notation, from here on out!),
$$
H(p_t) \equiv -\sum_x p_t(x) \log p_t(x),
$$
is non-decreasing as time, $t$, increases. Note that I'll be dealing with discrete time and space here, but all of these statements with some modifications hold for continuous processes. Anyways, more generally, we can write
$$
H(p_{t+1}) \ge H(p_t),
$$
but it turns out this law, as stated, doesn't quite hold for many Markov processes. It does, on the other hand, hold for a set of processes where the transition probabilities are symmetric (more generally, this holds iff the transitions are doubly-stochastic. [Cover](https://pdfs.semanticscholar.org/332c/1c7bab1a9a7a43d34d5a1784cf2454e0a7f1.pdf) has a slick, few-line proof of this which relies on some properties of the KL-divergence).

In this case, the probability of going from state $A$ to state $B$ is the same as the probability of going from state $B$ to state $A$. Writing this out mathematically, it says:

$$
K(x, x') = K(x', x).
$$

I should note that this is a *very* strong condition, but it can be quite useful in giving a simple proof of the above law. To prove this, first note that the KL-divergence is nonnegative, since the negative log is convex, thus by [Jensen's inequality](https://en.wikipedia.org/wiki/Jensen's_inequality) (this is the same proof as the [previous post](/ml-information-bounds.html)):

$$
\begin{aligned}
D(p_t\lVert p_{t'})&=-\sum_x p_t(x) \log \frac{p_{t'}(x)}{p_t(x)} \\
&\ge -\log\left(\sum_x p_t(x)\frac{p_{t'}(x)}{p_t(x)}\right) \\
&= -\log\left(\sum_x p_{t'}(x)\right) \\
& = -\log 1 \\
&= 0,
\end{aligned}
$$

since $p_{t'}, p_t$ are probability distributions (i.e., nonnegative and sum to one).

Here is the magical trick to proving the above. Note that
$$
D(p_t \lVert p_{t+2}) \ge 0,
$$
so
$$
-\sum_x p_t(x) \log \frac{p_{t+2}(x)}{p_t(x)} \ge 0,
$$
which means
$$
-\sum_x p_t(x) \log p_{t+2}(x) \ge -\sum_x p_t(x) \log p_t(x).
$$
But, by definition, we have that
$$
p_{t+2}(x) = \sum_{x'}K(x, x')p_{t+1}(x'),
$$
so
$$
-\sum_x p_t(x) \log \left(\sum_{x'} K(x, x')p_{t+1}(x')\right) \ge -\sum_x p_t(x) \log p_t(x),
$$
but, by Jensen's inequality (again!) on the left hand side we get,
$$
-\sum_x p_t(x) \log \left(\sum_{x'} K(x, x')p_{t+1}(x')\right) \le -\sum_{x, x'} p_t(x)K(x, x') \log p_{t+1}(x').
$$

Since we know $K(x, x') = K(x', x)$, then we immediately have that
$$
\sum_x p_t(x)K(x, x') = p_{t+1}(x'),
$$
so, putting it all together
$$
\begin{aligned}
H(p_{t+1}) &= -\sum_{x'} p_{t+1}(x') \log p_{t+1}(x') \\
&= -\sum_{x, x'} p_t(x)K(x, x') \log p_{t+1}(x')\\
&\ge -\sum_x p_t(x) \log p_t(x) \\
&= H(p_t),
\end{aligned}
$$
which is what we wished to prove.

## More general Markov processes

So, while it turns out this law doesn't hold for general Markov processes, a very similar law *does* hold. If a Markov process has a stationary distribution, $p$, then:
$$
D(p_{t+1}\lVert p) \le D(p_t \lVert p),
$$
so, as the Markov chain continues evolving, the KL divergence between the current distribution and the equilibrium distribution *never decreases*.

In fact, more generally, for *any* two initial probability distributions $p_0, q_0$, we have that
$$
D(p_{t+1} \lVert q_{t+1}) \le D(p_{t} \lVert q_{t}),
$$
so any two distributions undergoing the same (Markovian) dynamics never decrease in KL-divergence! Even if the Markov process does *not* have a unique stationary distribution, there is still a type of second law which holds, in a very general sense.

As before, [Cover](https://pdfs.semanticscholar.org/332c/1c7bab1a9a7a43d34d5a1784cf2454e0a7f1.pdf) has a fantastic, slick proof of the above, which I highly recommend you read!