# pyclothoids
A Python library for clothoid curves

[Read the Documentation!](https://pyclothoids.readthedocs.io/en/latest/)

Clothoid curves have some remarkable mathematical properties that make them desirable for use in many areas of physics and engineering.  Not only is a clothoid parameterized by arc length, but it has closed form expressions for its tangent angle and curvature.  These remarkable properties come at a cost.  The cartesian coordinates of a clothoid can only be expressed in closed form in terms of the Fresnel integrals, and cannot in general be evaluated exactly.  

There has been significant research into numerical algorithms to evaluate, construct, and manipulate these curves.  Software packages exist for this purpose but are often difficult to master.  This package takes a different approach, aiming to be easy to pick up and experiment with.  The ultimate goal is to provide a simple, intuitive, and pythonic interface to state of the art numerical software that allows you to leverage the latest research without the learning curve.

If you have a problem that you think could be solved using clothoid curves, this package aims to handle all the complexities of clothoid geometry for you so that you can focus on the top level problem you are trying to solve.  

That said, clothoid curves aren't always well behaved, and there are many other simpler curves that are far easier to understand and manipulate.  Before you use this library for a project, be sure that other simpler geometric constructs such as B-splines will not fulfill your needs.

The main design goals of pyclothoids are minimalism and simplicity.  For that reason, the top level API for this module consists of only one class - Clothoid.  To prevent common errors and further simplify the interface, Clothoid was designed to be immutable from the top level.  This means any methods that transform a Clothoid will return a new Clothoid with the desired modifications while leaving the original Clothoid intact.
