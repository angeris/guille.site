title: Some thoughts on global path optimization (Part 1/?)
slug: path-optimization-thoughts
category: auvsi-competition
tags: control-theory, math, non-convex, path-planning, auvsi
date: 2017-10-17

I usually see path planning in some shape or form usually solved as a Bellman update, Dynamic Programming-style problem, where the given control is asymptotically stable and optimal; in general, this seems to work quite well, but when we have so much computational power available now-a-days, I do wonder if a global optimization approach is both feasible and maybe even better. There is some literature on this, but most of it is... I'll just say it's not really as interesting as I thought it would be, at first right.

That being said, if anyone has any papers that I should *definitely* read, please do send them over to my Twitter (below) or email, etc.; whatever floats your boat. I feel like I have a very limited view of the current state of the field, so I'd always love to learn more! That being said, a cursory search through Google Scholar isn't as productive as I would've thought.

Anyways, let's get to something more interesting. I believe I'll be splitting this post up into some small set (say, 3, though this may change) posts explaining individual parts and more prickly details of the algorithm, but for now I'll just share the big idea and dive into the last part (which I argue is the hardest case).

Essentially the problem will be broken down into three basic steps (and a fourth "looping" step):

1. Discretize the space and goals into a graph problem which is guaranteed to be (a) *damn fast to solve* and (b) to always give a feasible result (minus a curvature constraint—that will come in later).

2. Make the resulting path through the graph into an ordered set of points $x_i \in \mathbb{R}^2$ (or $\mathbb{R}^3$, depending on what problem needs to be solved) through actual Euclidean space.

3. Perform continuous optimization starting at this resulting path in order to meet curvature constraints and add some 'finishing touches' (this will be formalized in a second, don't worry).

4. Do $(3)$ for moving objects, for a while, as $(1) \to (2)$ are solved again, simultaneously.

In this post, I'll mostly focus on step $(3)$, which is actually all you need to truly optimize over a path (along with some cute other heuristics), though steps $(1)$ and $(2)$ are also really just fast heuristics so we don't get stuck in crappy minima that would take us through the middle of an obstacle. I'll show how this can happen in non-obvious ways which is kinda fun for the first few times and mostly infuriating for the rest of the time (which is why we end up going through $(1)$ and $(2)$ in the end!).

## Smooth barriers

Perhaps the main idea of this step is that we can optimize over some function (which isn't quite a hard-wall constraint) and then slowly tune a parameter until it becomes a better and better approximation of a hard wall; for this example I've chosen the (reversed) logistic function

$$
\phi(x) = \frac{1}{1+e^{x}}
$$

such that two things happen: one, that $\phi(x) \to 0$ as $x\to \infty$ and $\phi(x) \to 1$ as $x\to -\infty$, and, two, that $\phi(Cx)$ approximates a hard wall as $C\to \infty$. Below is $\phi(Cx)$ plotted for a few different values of $C$:

<img src="/images/path-optimization-1/phi_curvature.png" class="plot">
*Barrier functions for varying curvatures $C$.*

The idea is that the smooth problem should be easy to solve and we can get consistently better approximations by starting at the easy problem and solving a sequence of problems which, in the limit, give the desired path.

More generally speaking, let the obstacles be centered at some set of points $\\{c\_j\\}$, each with some radius $R\_j$, then a single constraint corresponds to the barrier of curvature $C$ given by (where the object is at position $x$)

$$
\phi\left(C\left(\frac{\lVert x - c_j \lVert_2^2}{R_j^2} - 1\right)\right)
$$

which, if we assume that our path is characterized by an ordered set of points $\\{x_i\\}$, gives our complete energy function to be

$$
\mathcal{L}(x; c, R, C) = \sum_{ij}\phi\left(C\left(\frac{\lVert x_i - c_j \lVert_2^2}{R_j^2} - 1\right)\right)
$$

which is really just a fancy way of writing "each discretized point in my path should be outside of an obstacle." This is *close* to what we want, but it's not quite there yet: we aren't penalizing for being arbitrarily far away from other points—that is, if we just put all of our $\\{x_i\\}$ at infinity, we now have zero penalty!

Of course, that's a pretty stupid path that no drone can take (especially if we're constrained to be in some particular region, which, in this case, we are), so we do the next straightforward thing: we also penalize any point being far away from its adjacent points. E.g. we add a penalty term of the form $\eta\lVert x\_i - x\_{i+1}\lVert_2^2$ for $\eta>0$. 

In this case, our complete energy function then looks like

$$
\mathcal{L}(x; c, R, C) = \sum_{i}\left[\sum_j\phi\left(C\left(\frac{\lVert x_i - c_j \lVert_2^2}{R_j^2} - 1\right)\right) + \eta \lVert x\_i - x\_{i+1}\lVert_2^2\right]
$$

with a 'tunable' parameter $\eta$, and constraint wall 'hardness' $C$ which we send to infinity as we solve a sequence of problems. That is, let $\\{C\_k\\}$ be a sequence such that $C_k\to \infty$ then we solve the sequence of problems

$$
x^{(k)} = \min\_x\mathcal{L}(x; c, R, C_k) 
$$

and take the trajectory

$$
x^* = \lim\_{k\to\infty} x^{(k)}
$$

in the limit. Why do we do this? Because the derivative of $\mathcal{L}$ vanishes as $C\to\infty$ for the hard constraints. This can be seen in the picture above, by looking at the left side; as $C$ becomes large, the function becomes essentially flat when $x<0$ and $x>0$. This is generally bad, since, if we were to optimize directly for some very large $C$ which goes through the interior of an obstacle, we would be near a point where the derivative nearly vanishes even though we're inside of an obstacle!

This is totally infeasible for our problem and we cannot sidestep this issue in an obvious way using general optimization tools. So we're forced to do the Next Best Thing™, which is to perform this cooling schedule idea while optimizing over the objective.[^shortestpath]

Anyways, optimizing this function somewhat successfully with some decent cooling schedule (which is the subject of the next post) yields a cute movie that looks like the following

<video controls>
    <source src="/images/path-optimization-1/path_optimization.mp4" type="video/mp4">
</video>

Don't be fooled, though: there's plenty of little experiments that didn't work out while making this. Robustness is a huge reason why optimizing just this objective would take way too long and, hence, why we require the heuristics mentioned above (and which I'll soon discuss!).

A general overview of the code (with more details and implementation) can be found in the [StanfordAIR Github repo](https://github.com/StanfordAIR/optimization-sandbox).

[^shortestpath]: As given before, we can create feasible trajectories which do not have this problem by discretization methods—this helps out quite a bit since, for complicated trajectories where a lot of the initial path intersects obstacles, most of the time is spent on either (a) making a good cooling schedule for $C$ or (b) escaping the minima which include local obstacles. I'll discuss these methods in a later post.