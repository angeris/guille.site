title: Fast shortest paths for time-varying graphs (Part 4/?)
slug: path-optimization-thoughts4
category: auvsi-competition
tags: control-theory, math, non-convex, path-planning, graph-theory, auvsi
date: 2018-03-17

This is the fourth post in a series of posts describing an approach to doing path-planning in real-time on a small, embedded compute board. This is yet another relatively standalone post which mostly describes how to generate a (starting) path used in the [second](/path-optimization-thoughts2.html) and [first](/path-optimization-thoughts.html) posts to generate a feasible, smooth path that can be followed by a fixed-wing UAV.

For more background on the general optimization case, check out the posts above. In general, I won't be using much content from the previous three posts, so they're not necessary reading other than for context.

## Time-dependent shortest path search

First, as before, it's reasonable to ask for a fast heuristic to discover paths on a graph which are 'feasible' in a weak sense (i.e. a path where the UAV does not crash against an obstacle whose trajectory is known). This solution is then relaxed into a continuous problem inro $\mathbb{R}^2$ space and then optimized over. This latter trajectory is the one actually fed directly to the UAV controller and which is executed by the UAV. It should be noted that performing this weird relaxation is useful since it often takes quite a while for the algorithm to begin to converge to a feasible solution (and often can run into numerical stability problems while trying to do so). Anyways, for more of the details, check out the first [first](/path-optimization-thoughts.html) and [second](/path-optimization-thoughts2.html) posts (and the videos at the bottom, to observe the qualitative behavior).


I should mention that, unlike the previous problems, there already exist some fun [results](https://www.cs.ucsb.edu/~suri/psdir/soda11.pdf) on this notion of the shortest path (including a poly-time $(1+\varepsilon)OPT$ approximation!), but it's interesting enough to describe in a quick post anyways. In general, I assume no constraints on the possible curvature of a trajectory for this approximation, though it's straightforward include them in the general problem if the hit on run time performance isn't an issue.

### Definition

The problem set up is the following: let's say we have a family of graphs $G_t\subseteq G$ parametrized by some time parameter $t\in \mathbb{R}^{\ge 0}$, where $G$ is the 'universal graph'; in other words, every graph at every point in time is a subset of both edges and vertices of that graph. One idea for constructing this $G$ is to set $G = \bigcup_{t\in \mathbb{R}^{\ge 0}} G_t$ and insist that $G$ be a finite graph.[^union-graphs]

$G_t$ at each point encodes some constraints on the current position of the drone, which is indicated by some vertex $v\in V(G)$ (where $V(G)$ is the vertex set of $G$) and this position is *valid* at time $t$ if the vertex exists in $G_t$. In other words, position $v$ is valid at $t$ if $v\in V(G_t)$.

Now, the question becomes: given some cost function $c: V(G)\times V(G) \to \mathbb{R}^{\ge 0}$ and some start and end nodes, construct a shortest valid path[^valid-path] from the start to the end nodes (where the start node is assumed to be at time $t=0$), if it exists.

### A simple algorithm
With this definition and knowledge of the $A^*$ algorithm (hint, hint!), I encourage working out what the solution to this problem is, assuming we have a [consistent heuristic](https://en.wikipedia.org/wiki/Consistent_heuristic) for the path.

As a side note: a simple heuristic, which usually works quite well, is to take the $\ell^2$ distance between two nodes and divide it by the maximum velocity of the UAV—this is consistent since the UAV cannot travel between two points faster than being at its maximum velocity along the shortest possible line. In cases where many of the obstacles are small relative to the size of the graph and are sparse, this idea works extremely well because the approximation is fairly tight.

With that in mind, here's the algorithm, which is really just a (slightly) modified version of $A^*$. (The code below is like quasi-Python pseudocode, but implementing directly shouldn't require too many changes. Additionally, some things can be easily stored instead of recomputed by exploiting the structure of the cost function.)

```
:::python
q <- priority queue
start_node <- start node
end_node <- end node

c <- edge-cost function
h <- heuristic cost function

G <- graph at time t

# Algorithm begins here
add ([start_node], cost=0) to q

while True:
    curr_path, curr_cost = q.pop_smallest()
    last_node = curr_path[end]

    if last_node is end_node:
        return curr_path
    
    for neighbor in last_node.neighbors:
        new_path = curr_path.append(neighbor)
        new_cost = c(new_path)
        if neighbor not in G(new_cost):
            continue
        add (new_path, cost=(new_cost + h(neighbor, end_node))) to q
    

return None
```


This algorithm returns one of the optimal paths, since a path will only be returned if the total cost of the found path is at most as large as the next possible valid path to some point $v_t$ plus the heuristic cost $h(v_t, e)$. By assumption, the heuristic function is a global underestimator, which immediately implies that this return path must have had a minimum possible original cost. I should also point out that there's nothing preventing an exponential time solution (and it's certainly exponential in the worst case... if there doesn't exist a path between $s, e$, for example)! This is not great, but (as usual) this algorithm works much better than exponential time, in practice.

Another thing to be careful of is that the above algorithm can also return paths which double back on themselves (e.g. if the UAV needs to 'wait' for an obstacle to pass). This may not be desired behavior (at least, definitely not in our case), so specific checks can be added to prevent this, depending on the application. Additionally, there is nothing restricting the cost function to be time-independent, so even this constraint can be relaxed while still maintaining optimality.

Anyways, that's all for today. I wanted to keep this post (relatively) short and sweet since there's another one coming up quite soon on how to perform the optimization found in the previous posts: given a functional form for the position of the obstacles at some point in time—e.g., the next step after finding the approximation. Hopefully there will be some more time next week to write that out, but I make no major promises.

[^union-graphs]: By the 'union' of graphs, I mean that the new graph should be
$$
\bigcup_{t} G_t = \left(\bigcup_{t} V(G_t), ~ \bigcup_t E(G_t)\right)
$$
where $V(G)$ is the set of vertices of $G$ and $E(G)$ is the set of edges of $G$.

[^valid-path]: A path $v = (v_t)$ is valid if it is a path from the start node to the end node and each $v_t \in G_t$ for every possible $t$. We also have that $t_{i+1} - t_i = c(v_{t}, v_{t+1})$. In other words, the time at action number $i$ is the sum of the times of all of the previous actions (this just gives a definition of 'time' in this problem).
