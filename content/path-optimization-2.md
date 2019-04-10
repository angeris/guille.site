title: Optimizers, momentum, and cooling schedules (Part 2/?)
slug: path-optimization-thoughts2
category: auvsi-competition
tags: control-theory, math, non-convex, path-planning, auvsi
date: 2017-10-22

This is the second post in a series of posts describing an initial approach to doing path-planning in real-time on a small, embedded compute board. For the first in the series which describes the energy function used below, see the [first post](/path-optimization-thoughts.html).

## Quick recap

Anyways, we left off on the idea that we now have a function which we wish to optimize, along with a sequence of constants $C$ which tends to a given solution—in particular, and perhaps most importantly, we only care about the solution in the limit $C\to\infty$.

As before, though, we can't just optimize the function
$$
\mathcal{L}(x; c, R, C) = \sum_{i}\left[\sum_j\phi\left(C\left(\frac{\lVert x_i - c_j \lVert_2^2}{R_j^2} - 1\right)\right) + \eta \lVert x_i - x_{i+1}\lVert_2^2\right]
$$

over some large $C$, since we've noted that the objective becomes almost-everywhere flat in the limit[^measure-theory] and thus becomes very difficult to optimize using typical methods. Instead, we optimize over the sequence of functions, for $C_k \to \infty$,

$$
x^{(k)} = \min_x\mathcal{L}(x; c, R, C_k) 
$$

picking only

$$
x^* = \lim_{k\to\infty} x^{(k)}
$$

as our final trajectory. The goal of this post is to explore some methods for optimizing this function in the constrained, embedded environment which we'll be using for the competition.

## Gradient descent

I'll do a quick introduction to gradient descent since there are [plenty](https://medium.com/ai-society/hello-gradient-descent-ef74434bdfa5) of [posts](https://machinelearningmastery.com/gradient-descent-for-machine-learning/) on [this](https://www.quora.com/What-is-an-intuitive-explanation-of-gradient-descent) [method](http://homes.soic.indiana.edu/classes/spring2012/csci/b553-hauserk/gradient_descent.pdf), many of which I suspect are much better than anything I'll ever write.

Anyways, the simple idea (or another perspective on it) is that, if we want to find the minimum of a function $V$, then we can think about the function as a potential for a particle, whose position we call $x$, and then just run Newton's equation forward in time!

$$
m\ddot x = -\nabla V(x)
$$

where $\ddot x = \frac{d^2x}{dt^2}$ (this is just a rewriting of $F=ma=m\ddot x$, where our force is conservative).  You may notice a problem with this idea: well, if we land in a well, we'll continue oscillating... that is, there's literally no friction to stop us from just continuing past the minimum. So, let's add this in as a force proportional to the velocity (but pointing in the opposite direction), with friction coefficient $\mu>0$:

$$
m\ddot x = -\nabla V(x) - \mu \dot x.
$$

Now, here I'll note we can do two things: one, we can keep the former term containing acceleration (i.e. momentum), accepting that we could possibly overshoot our minimum (because, say, we're going 'too fast') but then later 'come back' to it (this is known as gradient descent with momentum),[^momentum] or, if we never want to overshoot it (but allow for the possibility that we may always be too slow in getting there in the first place) we can just send our momentum term to zero by sending $m \to 0$. I'll take the latter approach for now, but we'll consider the former case, soon.

Anyways, sending $m\to 0$ corresponds to having a ball slowly rolling down an extremely sticky hill, stopping only at a local minimum, that is:

$$
\mu\dot x + \nabla V(x) = 0
$$

or, in other words:

$$
\dot x = -\frac{1}{\mu}\nabla V(x).
$$

Discretizing this equation by noting that, by definition of the derivative, we have

$$
\dot x(t_{i+1}) \approx \frac{x_{i+1} - x_i}{h}
$$

then gives us (by plugging this into the above)

$$
\frac{x_{i+1} - x_i}{h} = -\frac{1}{\mu}\nabla V(x),
$$

or, after rearranging (and setting $\mu=1$, since we can control $h$ however we like, say by defining $h := \frac{h}{\mu}$)

$$
x_{i+1} = x_i - h\nabla V(x).
$$

In other words, gradient descent corresponds to the discretization of Newton's equations in the *overdamped* limit (e.g. in the limit of small mass and large friction).

This method is great because (a) we know it converges with probability 1 (as was relatively recently proven [here](https://arxiv.org/abs/1602.04915)) for arbitrary, somewhat nice functions and (b) because it *works*. That being said, it's slow; for example, in the previous post, we saw that it converged after 5000 iterations (which, to be fair, takes about 20 seconds on my machine, but still).

A simple improvement (where we don't throw $m\to 0$) yields a significant speed up! Of course, at the cost of having to deal with more hyperparameters, but that's okay: we're big kids now, and we can deal with more than one hyperparameter in our problems.

## Gradient descent with momentum
The next idea is to, instead of taking $m\to 0$, just write out the full discretization scheme. To make our lives easier, we rewrite $v(t) \equiv \dot x(t)$ to be our velocity, this gives us a simple rewriting of the form:

$$
\begin{align}
m\dot v &= -\nabla V(x) - \mu v\\
\dot x(t) &= v(t)
\end{align}
$$

discretizing the second equation with some step-size $h'$ (as above) we get

$$
x_{t+1} = x_t + h'v_{t+1}
$$

where the former equation is, when discretized with some step size $h$

$$
m\frac{v_{t+1} - v_t}{h} = -\nabla V(x_t) - \mu v_t
$$

or after rearranging, and defining $\gamma \equiv \frac{h}{m}$ (which we can make as small as we'd like)

$$
\begin{align}
v_{t+1} &= -\gamma \nabla V(x_t) + (1-\mu \gamma) v_t\\
x_{t+1} &= x_t + h'v_{t+1}
\end{align}
$$

usually we take $h' = 1$, and, to prevent $v_t$ from having weird behaviour, we require that $1-\mu\gamma > 0$, i.e. that $\gamma < \frac{1}{\mu}$.[^oscillations] If we call $\beta \equiv 1 - \mu\gamma$ and therefore have that $0 < \beta  < 1$ then we obtain the classical momentum for gradient descent

$$
\begin{align}
v_{t+1} &= -\gamma \nabla V(x_t) + \beta v_t\\
x_{t+1} &= x_t + v_{t+1}
\end{align}
$$

which is what we needed! Well... close to what we needed, really.

Anyways, just to give some perspective on the speed up: using momentum, the optimization problem took around 600 iterations to converge, more than 8 times less than the original given above. I'll give a picture of this soon, but I'm missing one more slight detail.

## Cooling schemes

Imagine we want to optimize some function $\ell(\cdot)$ that is, in general, extremely hard to solve. If we're lucky, we may be able to do the next best thing: take a series of functions parametrized by, say, $C$, such that $\ell_C(\cdot) \to \ell(\cdot)$ as $C\to\infty$,[^approaches] *and* where the problem is simple to solve for $C_{k+1}$, given the solution for $C_k$.

Of course, given this and the above we can already solve the problem: we begin with some small $C_0$ and then, after converging for $\ell_{C_0}(\cdot)$ we then continue to $\ell_{C_1}(\cdot)$, after converging to that, we then continue to solve for $\ell_{C_2}(\cdot)$, etc., until we reach some desired tolerance on the given result.

Or... (of course, I'm writing this for a reason), we could do something fancy using the previous scheme:

Every time we update our variable, we also increase $k$ such that both the problem sequence and the final solution converge at the same time. It is, of course, totally not obvious that this works (though with some decent choice of schedule, one could imagine it should); the video below shows this idea in action using both momentum and this particular choice of cooling scheme (note the number of iterations is much lower relative to the previous attempt's 5000, but also note that, while the scheme converged in the norm—that is, the variables were updated very little—it didn't actually converge to an optimal solution, but it was pretty close!).

I'd highly recommend looking at the code in order to get a better understanding of how all this is implemented and the dirty deets.

Anyways, optimizing the original likelihood presented in the first post (and in the first part of *this* post) using momentum and the above cooling schedule yields the following nice little video:


<video controls>
    <source src="/images/path-optimization-2/path_optimization_2.mp4" type="video/mp4">
</video>


As before, this code (with more details and implementation) can be found in the [StanfordAIR Github repo](https://github.com/StanfordAIR/optimization-sandbox).

<!-- Footnotes -->

[^measure-theory]: This is, indeed, a technical term, but it's also quite suggestive of what really happens.

[^momentum]: Of course, there are many reasons why we'll want momentum, but those will come soon.

[^oscillations]: Consider $V(x) = 0$, with some initial condition, $v_0 > 0$, say, then we'll have
$$
v_t = -k v_{t-1}
$$
for some $k = \mu\gamma - 1>0$. Solving this yields $v_{t} = (-1)^tk^t v_{0}$. This is weird, because it means that our velocity will change directions every iteration even though there's no potential! This is definitely not expected (nor desirable) behaviour.

[^approaches]: In some sense. Say: in the square error, or something of the like. This can be made entirely rigorous, but I choose not to do it here since it's not terribly essential.