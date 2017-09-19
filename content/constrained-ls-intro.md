title: Least-squares and image processing
slug: ls-images
category: math
tags: math, least-squares, image-processing
date: 2017-09-16

Least squares is one of those things that seems relatively simple once you first look at it (perhaps also because most linear algebra texts relegate it to nothing more than a page or two on their textbooks), but has surprisingly powerful implications that are quite nice, and, most importantly, that are easily computable.

If you're interested in looking at the results first, I'd recommend skipping the following section and going immediately to the next one, which shows the application.

So, let's dive right in!

## Vanilla least squares
The usual least-squares many of us have heard of is a problem of the form

$$
\min_x \,\,\lVert Ax - b \lVert^2
$$

where I define $\lVert y\lVert^2 \equiv \sum_i y_i^2 = y^Ty$ to be the usual Euclidean norm (and $y^T$ denotes the transpose of $y$). This problem has a unique solution provided that $A$ is full-rank (i.e. has independent columns), and therefore that $A^TA$ is invertible.[^sq-invertible] This is true since the problem above is convex (e.g. any local minimum, if it exists, corresponds to the global minimum[^convex-global-min]), coercive (the function diverges to infinity, and therefore *has* a local minimum) and differentiable such that

$$
\nabla \lVert Ax - b \lVert^2 = \nabla (Ax-b)^T(Ax-b) = 2A^T(Ax-b) = 0,
$$

or that, after rearranging the above equation,

$$
A^TAx = A^Tb.
$$

This equation is called the *normal equation*, which has a unique solution for $x$ since we said $A^TA$ is invertible. In other words, we can write down the (surprisingly, less useful) equation for $x$

$$
x = (A^TA)^{-1}A^Tb.
$$

A simple example of direct least squares can be found on the [previous post](/pid-ls.html), but that's nowhere as interesting as an *actual* example, using some images, presented below. First to show the presented example is possible, I should note that this formalism can be immediately extended to cover a (multi-)objective problem of the form, for $\lambda_i > 0$

$$
\min_x \,\,\lambda_1\lVert A_1x - b_1 \lVert^2 + \lambda_2\lVert A_2x - b_2 \lVert^2 + \dots + \lambda_n\lVert A_nx - b_n \lVert^2
$$

by noting that (say, with two variables, though the idea extends to any number of objectives), we can pull the $\lambda_i$ into the inside of the norm and observing that

$$
\lVert a\lVert^2 + \lVert b \lVert^2 = \left \lVert 
\begin{bmatrix}
a\\\\
b
\end{bmatrix}
\right\lVert^2.
$$

So we can rewrite the above multi-objective problem as

$$
\lambda_1\lVert A_1x - b_1 \lVert^2 + \lambda_2\lVert A_2x - b_2 \lVert^2  = \left\lVert 
\begin{bmatrix}
\sqrt{\lambda_1} A_1\\\\
\sqrt{\lambda_2} A_2
\end{bmatrix}
x
-
\begin{bmatrix}
\sqrt{\lambda_1}b_1\\\\
\sqrt{\lambda_2}b_2
\end{bmatrix}\right\lVert^2.
$$

Where the new matrices above are defined as the 'stacked' (appended) matrix of $A_1, A_2$ and the 'stacked' vector $b_1, b_2$. Or, defining 

$$
\bar A \equiv 
\begin{bmatrix}
\sqrt{\lambda_1} A_1\\\\
\sqrt{\lambda_2} A_2
\end{bmatrix}
$$

and

$$
\bar b \equiv
\begin{bmatrix}
\sqrt{\lambda_1} b_1\\\\
\sqrt{\lambda_2} b_2
\end{bmatrix},
$$

we have the equivalent problem

$$
\min_x \,\, \lVert \bar A x - \bar b\lVert^2
$$

which we can solve by the same means as before.

This 'extension' now allows us to solve a large amount of problems (even equality-constrained ones! For example, say $\lambda_i$ corresponds to an equality constraint, then we can send $\lambda_i \to \infty$, which, if possible, sends that particular term to zero[^eq-constraint]), including the image reconstruction problem that will be presented below. Yes, there are better methods, but I can't think of many that can be written in about 4 lines of Python with only a linear-algebra library (not counting loading and saving, of course 😉).

## Image de-blurring with LS
Let's say we are given a blurred image, represented by some vector $y$ with, say, a gaussian blur operator given by $G$ (which can be represented as a matrix). Usually, we'd want to minimize a problem of the form

$$
\min_x \,\,\lVert Gx - y \lVert^2
$$

where $x$ is the reconstructed image. In other words, we want the image $x$ such that applying a gaussian blur $G$ to $x$ yields the closest possible image to $y$. E.g. we really want something of the form

$$
Gx \approx y.
$$

Writing this out is a bit of a pain, but it's made a bit easier by noting that convolution with a 2D gaussian kernel is separable into two convolutions of 1D (e.g. convolve the image with the up-down filter, and do the same with the left-right) and by use of the Kronecker product to write out the individual matrices.[^kronecker-conv] The final $G$ is therefore the product of each of the convolutions. Just to show the comparison, here's the initial image, taken from [Wikipedia](https://commons.wikimedia.org/wiki/File:Lichtenstein_img_processing_test.png)

<img src="/images/constrained-ls-intro/initial_image.png" class="insert">
*Original greyscale image*

and here's the image, blurred with a 2D gaussian kernel of size 5, with $\sigma = 3$

<img src="/images/constrained-ls-intro/blurred_image.png" class="insert">
*Blurred greyscale image. The vignetting comes from edge effects.*

The kernel, for context looks like:

<img src="/images/constrained-ls-intro/gaussian_kernel.png" class="insert">
*2D Gaussian Kernel with $N=5, \sigma=3$*

Solving the problem, as given before, yields the final (almost identical) image:

<img src="/images/constrained-ls-intro/reconstructed_image.png" class="insert">
*The magical reconstructed image!*

Which was nothing but solving a simple least squares problem (as we saw above)!

Now, you might say, "why are we going through all of this trouble to write this problem as a least-squares problem, when we can just take the FFT of the kernel and the Gaussian and divide the former by the latter? Isn't convolution just multiplication in the Fourier domain?"

And I would usually agree!

Except for one problem: while we may *know* the gaussian blurring operator on artificial images that *we* actively blur, the blurring operator that we provide for real images may not be fully representative of what's really happening! By that I mean, if the real blurring operator is given by $G^\text{real}$, it could be that our guess $G$ is far away from $G^\text{real}$, perhaps because of some non-linear effects, or random noise, or whatever.

That is, we know what photos, in general, look like: they're usually pretty smooth and have relatively few edges. In other words, the variations and displacements aren't large almost everywhere in most images. This is where the multi-objective form of least-squares comes in handy—we can add a secondary (or third, etc) objective that allows us to specify how smooth the actual image should be! 

How do we do this, you ask? Well, let's consider the gradient at every point. If the gradient is large, then we've met an edge since there's a large color variation between one pixel and its neighbour, similarly, if the gradient is small at that point, the image is relatively smooth at that point.

So, how about specifying that the sum of the norms of the gradients at every point be small?[^heat-diffusion] That is, we want the gradients to *all* be relatively small (minus those at edges, of course!), with some parameter that we can tune. In other words, let $D_x$ be the difference matrix between pixel $(i,j)$ and pixel $(i+1,j)$ (e.g. if our image is $X$ then $(D_x X)\_{ij} = X\_{i+1,j} - X\_{ij}$, and, similarly, let $D_y$ be the difference matrix between pixel $(i, j)$ and $(i,j+1)$.[^derivative-mat] Then our final objective is of the form

$$
\min_x \,\,\lVert Gx - y \lVert^2 + \lambda\left(\lVert D\_x x \lVert^2 + \lVert D\_y x \lVert^2\right)
$$

where $\lambda \ge 0$ is our 'smoothness' parameter. Note that, if we sent $\lambda \to \infty$ then we really care that our image is 'infinitely smooth' (what would that look like?[^smooth-image]), while if we send it to zero, we care that the reconstruction from the (possibly not great) approximation of $G^\text{real}$ is really good. Now, let's compare the two methods with a slightly corrupted image:

<img src="/images/constrained-ls-intro/initial_image.png" class="insert">
*Original greyscale image (again)*

<img src="/images/constrained-ls-intro/smoothed_corrupted_reconstructed_image_l=1e-07.png" class="insert">
*Reconstruction with $\lambda = 10^{-7}$*

<img src="/images/constrained-ls-intro/corrupted_reconstructed_image.png" class="insert">
*Reconstruction with original method*

Though the normalized one has slightly larger grains, note that, unlike the original, the contrast isn't as heavily lost and the edges, etc, are quite a bit sharper.

To that end, one could think of many more ways of characterizing a 'natural' image, all of which will yield successively better results, but I'll leave with saying that LS, though simple, is quite a powerful method for many cases. In particular, I'll cover fully-constrained LS (in a more theoretical post) in the future, but with an application to path-planning.

Hopefully this was enough to convince you that even simple optimization methods are pretty useful! But if I didn't do my job, maybe you'll have to read some future posts. ;)

The code for this post can be found [here]().


[^sq-invertible]: If $A^TA x = 0$ then $x^TA^TAx = 0$, but $x^TA^TAx = (Ax)^T(Ax) = \lVert Ax \lVert^2 = 0$ which is zero only when $Ax = 0$. E.g. only if there is an $x$ in the nullspace of $A$.

[^convex-global-min]: A proof is straightforward. Let's say $f$ is differentiable, since this is the case we care about, then we say $f$ is convex if the hyperplane given by $\nabla f(x)$ (at any $x$) bounds $f$ from below. 

    A nice picture usually helps with this:
    ![Convex envelope approximation](/images/constrained-ls-intro/bounding-hyperplanes.png)

    Each of the hyperplanes (which are taken at the open, red circles along the curve; the hyperplanes themselves denoted by gray lines) always lies below the graph of the function (the blue parabola). We can write this as
    $$
    f(y)\ge (y-x)^T(\nabla f(x)) + f(x)
    $$
    for all $x, y$.

    This is usually taken to be the *definition* of a convex function, so we'll take it as such here. Now, if the point $x^0$ is a local minimum, we must have $\nabla f(x^0) = 0$, this means that
    $$
    f(y) \ge (y-x^0)^T(\underbrace{\nabla f(x^0)}_{=0}) + f(x^0) = (y-x^0)^T0 + f(x^0) = f(x^0),
    $$
    for any $y$.

    In other words, that
    $$
    f(y) \ge f(x^0),
    $$
    for any $y$. But this is the definition of a global minimum since the point $f(x^0)$ is less than any other value the function takes on! So we've proved the claim that any local minimum (in fact, more strongly, that any point with vanishing derivative) is immediately a global minimum for a convex function. This is what makes convex functions so nice!
    
[^eq-constraint]: There are, of course, better ways of doing this which I'll present in some later post. For now, though, note that if the constraint is not achievable at equality, e.g. that we have $\lVert Cx - d\lVert^2 \ge \varepsilon > 0$ for any $x$, then the objective $\lambda_i\lVert Cx - d\lVert^2 \ge \lambda_i\varepsilon \to \infty$ whenever we send $\lambda_i \to \infty$. This gives us a way of determining if the constraint is feasible (which happens only if the program converges to a finite value for arbitrarily increasing $\lambda_i$) or infeasible (which happens, as shown before, if the minimization program diverges to infinity).

[^kronecker-conv]: Assuming we write out the image as a row-major order, with dimensions $m\times m$, we can write the [Toeplitz matrix](https://en.wikipedia.org/wiki/Toeplitz_matrix) of the 1D gaussian convolution of length $n$, say $T$. Then the row-convolution of the image's one-dimensional vector representation is given by $I_m \otimes T$, where $\otimes$ denotes the [Kronecker product](https://en.wikipedia.org/wiki/Kronecker_product) of both matrices and $I_m$ is the $m\times m$ identity matrix. Similarly, we can do this for the column convolution by writing it out as $T\otimes I_{m+n}$ (note the additional $n$ which comes from the convolution!), then the final $G$ matrix is

    $$
        G = (T\otimes I_{m+n})(I_m \otimes T)
    $$

    which is much simpler to compute than the horrible initial expression dealing with indices. Additionally, these expressions are sparse (e.g. the first is block-diagonal), so we can exploit that to save on both memory and processing time. For more info, I'd recommend looking at the code for this entry.

[^heat-diffusion]: It turns out this has deep connections to a bunch of beautiful mathematical theories (most notably, the theory of heat diffusion on manifolds), but we won't go into them here since it's relatively out of scope, though I may cover it in a later post.

[^smooth-image]: You probably guessed it: it's just an image that is all the same color.

[^derivative-mat]: These are slightly tricker to form for 2D images, but, as with the previous, we make heavy use of the Kronecker product. The derivative matrix for a 1D $m$-vector is the one formed by (let's call it $L$ with dimensions $(m-1)\times m$)
$$
L=\begin{bmatrix}
1 & -1 & 0 & 0 & \dots\\\\
0 & 1 & -1 & 0 & \dots\\\\
0 & 0 & 1 & -1 & \dots\\\\
\vdots & \vdots & \vdots & \vdots & \ddots
\end{bmatrix}
$$
this is relatively straightforward to form using an off-diagonal matrix. Note also that this matrix is quite sparse, which saves us from very large computation. Now, we want to apply this to each row (column) of the 2D image which is in row-major form. So, we follow the same idea as before and pre (post) multiply by the identity matrix. That is, for an $m\times m$ image
$$
D_x = I_m\otimes L
$$
and
$$
D_y = L\otimes I_m
$$