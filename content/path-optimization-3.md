title: Comparing continuous optimization heuristics vs. reinforcement learning (Part 3/?)
slug: path-optimization-thoughts3
category: auvsi-competition
tags: control-theory, math, non-convex, path-planning, reinforcement-learning, dnn, auvsi
date: 2017-12-25
status: draft

This is the third post in a series of posts describing an approach to doing path-planning in real-time on a small, embedded compute board. Though this one is more of a standalone post (e.g. doesn't really require much reading of the previous), it compares the performance of the algorithms described in the [second](/path-optimization-thoughts2.html) and [first](/path-optimization-thoughts.html) posts to a standard approach using reinforcement learning (RL) with linear global approximations and RL with a neural-net approximator (e.g. deep RL).

## Introduction and thank yous

The results presented in this post are those found in [Delgeris, Kulgod, Scheinfeld, 2017](https://github.com/ischeinfeld/navigation229/blob/master/paper/methods-drone-obstacle.pdf). Before this, though, I want to give a huge thank you to [Isaach Scheinfeld](https://github.com/ischeinfeld) and Raja Ramesh for their work implementing all of the ideas presented previously into a complete (and usable!) framework—which they did using only the relatively poorly-written (even by my standards) iPython notebook I gave in the second post. Additionally, I note that many of the images used below are from the paper above; so, for further reference, it's worth reading the above paper.

I'm sure you can guess which of DQN, Q-learning, or classical optimization wins (hint: it's none of the ones containing any buzzwords). And the question here, which I will attempt to answer is, why?

First—and I'll just get this out of the way, right now—is that this is a class project and there is no expectation of peer review (i.e. much like everything in this blog). So, don't take anything I say here (or, really, anything I say in general) as gospel. There could've been some bugs in the implementation or things that can be improved. That being said, I'll cover why the overall results aren't so surprising in the first place and why it might take some pretty hard work to really beat a classical implementation in the tasks we're interested in.[^andanotherreminder]

Okay, enough with the disclaimers. Let's take a look at the results!

## Results

As mentioned in the [first post](/path-optimization-thoughts.html) of the series, an important step of the algorithms is a discretization of the plane into a graph problem, from which we receive a feasible point for our optimization problem (assuming, say, that the wall constraints are hard rather than the relaxed constraints we use for optimization). The figure below (taken from the paper) shows a really nice image of the process:

<img src="/images/path-optimization-3/steps.png" class="insert" style="width: 100%">
*Steps to construction of solution, from left to right: (1) graph discretization, (2) continuous problem, (3) local optimization. This latter step is a relaxation of the feasible path to a locally-optimal solution. From [Delgeris, et al. 2017](https://github.com/ischeinfeld/navigation229/blob/master/paper/methods-drone-obstacle.pdf).*

This algorithm is compared to two other cases: one, a linear global approximator which uses some user-defined basis functions. The main one used is (using slightly different terminology than the paper, such that hi)



[^andanotherreminder]: I've been proven wrong before and would love to be proved wrong here as well!
