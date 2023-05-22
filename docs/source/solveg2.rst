SolveG2
=======

.. autofunction:: pyclothoids.SolveG2


The problem of interpolating these two points in general has multiple solutions, so this function provides
two additional parameters 'Dmax' and 'dmax'.  'Dmax' represents the allowed deviation between the start and
end angle of the first and last segment, meaning that a smaller Dmax will enforce a stricter penalty on large 
angle deviations to prevent loops.  'dmax' is similar, but instead of limiting the angular difference between
the start and endpoint of the end segments, this parameter limits the difference in angle between the 
endpoints of the first and last segments and the corresponding points on a reliably fair solution to a G1
relaxation of the G2 problem at hand.

If not provided, these are set to sensible defaults to ensure the solution is fair and doesn't include 
unneccesary loops.  These defaults have been tested extensively to ensure reliable existence and fairness
of the default solution.

For an in depth look at how these parameters function and how they are set by default, please see [1]

.. [1] Bertolazzi, E., & Frego, M. (2018). On the G2 Hermite interpolation problem with clothoids. Journal of Computational and Applied Mathematics, 341, 99-116.
