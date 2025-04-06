from ._clothoids_cpp import ClothoidCurve, G2solve3arc

from math import cos, sin, atan2
from functools import lru_cache

CLOTHOID_FUNCTION_WINDOW = frozenset(
    (
        "X",
        "XD",
        "XDD",
        "XDDD",
        "Y",
        "YD",
        "YDD",
        "YDDD",
        "Theta",
        "ThetaD",
        "ThetaDD",
        "ThetaDDD",
    )
)

CLOTHOID_PROPERTY_WINDOW = frozenset(
    (
        "length",
        "dk",
        "ThetaStart",
        "ThetaEnd",
        "XStart",
        "XEnd",
        "YStart",
        "YEnd",
        "KappaStart",
        "KappaEnd",
    )
)

PROJECTION_CACHE_SIZE = 32


class Clothoid(object):
    """
    An object representing a single clothoid curve. Pickling and unpickling is supported. The class
    constructor is meant for internal use for interfacing with the C++ layer.  To initialize a Clothoid, use
    one of the classmethods instead.
    """

    def __init__(self, clothoid_curve):
        if type(clothoid_curve) == type(self):
            # Create a copy of the underlying C++ clothoid when constructor is called with a Python Clothoid
            self._ClothoidCurve = ClothoidCurve(clothoid_curve._ClothoidCurve)
        else:
            # No need to create a copy when a C++ clothoid is passed directly by the classmethods or G2solver
            self._ClothoidCurve = clothoid_curve
        self.SetupProjectionCache(PROJECTION_CACHE_SIZE)

    @classmethod
    def StandardParams(cls, x0, y0, t0, k0, kd, s_f):
        """
        A method to initialize a Clothoid given a starting point, starting tangent, starting curvature,
        curvature rate, and final length.
        """
        temp_clothoid = ClothoidCurve()
        temp_clothoid.build(x0, y0, t0, k0, kd, s_f)
        return cls(temp_clothoid)

    @classmethod
    def G1Hermite(cls, x0, y0, t0, x1, y1, t1, tol=1e-10):
        """
        A method to numerically compute the solution to the G1 Hermite interpolation problem and initialize a
        Clothoid object with the solution parameters.
        """
        temp_clothoid = ClothoidCurve()
        temp_clothoid.build_G1(x0, y0, t0, x1, y1, t1, tol)
        return cls(temp_clothoid)

    @classmethod
    def Forward(cls, x0, y0, t0, k0, x1, y1, tol=1e-10):
        """
        A method to numerically compute the solution to the forward problem given a starting point, starting
        tangent, starting curvature, and final point and initialize a Clothoid object with the solution
        parameters.
        """
        temp_clothoid = ClothoidCurve()
        temp_clothoid.build_forward(x0, y0, t0, k0, x1, y1, tol)
        return cls(temp_clothoid)

    def __getattr__(self, name):
        if name in CLOTHOID_FUNCTION_WINDOW:
            return getattr(self._ClothoidCurve, name)
        if name in CLOTHOID_PROPERTY_WINDOW:
            return getattr(self._ClothoidCurve, name)()  # mimic property getter syntax
        return super().__getattribute__(name)()

    def __str__(self):
        return "Clothoid: " + "".join(
            map(
                lambda m, n: m + ":" + str(getattr(self, n)) + " ",
                ("x0", "y0", "t0", "k0", "kd", "s"),
                ("XStart", "YStart", "ThetaStart", "KappaStart", "dk", "length"),
            )
        )

    def __repr__(self):
        return str(self)

    def __getstate__(self):
        return self.Parameters

    def __setstate__(self, state):
        temp_clothoid = ClothoidCurve()
        temp_clothoid.build(*state)
        self._ClothoidCurve = temp_clothoid

    def SetupProjectionCache(self, cachesize):
        """
        By default, each instance of the Clothoid object maintains an lru cache of the results from projecting
        any point onto the clothoid.  This is because the projection operation calculates several potentially
        useful quantities all at once, such as projection distance and the coordinates of the projected point.
        Caching the results means that users can call `ClosestPoint` and `Distance` separately and sequentially
        without recomputing the projection.  The default cachesize is set to 32 but this method allows
        configuring the cache with a custom size.  Pass `cachesize = None` to disable caching entirely.
        """
        if cachesize is not None:
            self.ProjectPointOntoClothoid = lru_cache(maxsize=cachesize)(
                self._ProjectPointOntoClothoid
            )
        else:
            self.ProjectPointOntoClothoid = self._ProjectPointOntoClothoid

    @property
    def Parameters(self):
        """
        Complete data describing the calling Clothoid

        :getter: Returns the initialization parameters of a clothoid, fit to be used as args to StandardParams
        :setter: Parameters cannot be modified
        :type: tuple
        """
        return (
            self.XStart,
            self.YStart,
            self.ThetaStart,
            self.KappaStart,
            self.dk,
            self.length,
        )

    def SampleXY(self, npts):
        """
        A method to return a vector of X coordinates and Y coordinates generated by evaluating the Clothoid at
        npts equally spaced points along its length.

        Roughly shorthand for:

        ::

            def SampleXY(self,npts):
                sample_points = [self.length * m/(npts-1) for m in range(0,npts)]
                X = [self.X(i) for i in sample_points]
                Y = [self.Y(i) for i in sample_points]
                return [X,Y]
        """
        return [
            [j(i * self.length / max(npts - 1, 1)) for i in range(0, npts)]
            for j in (self.X, self.Y)
        ]  # TODO: move sampling to c++ layer for loop efficiency?

    def Scale(self, sfactor, center=(0, 0)):
        """
        Returns a copy of the calling clothoid subjected to a scaling transform with a scale of sfactor and a
        stationary point at center
        """
        if sfactor == 0:
            return self.__class__.StandardParams(0, 0, 0, 0, 0, 0)
        temp_clothoid = self.__class__(self)
        temp_clothoid._ClothoidCurve._scale(
            sfactor
        )  ##DANGER WILL ROBINSON : MUTATING STATE DIRECTLY##
        if center == "start":
            return temp_clothoid
        s = [temp_clothoid.XStart, temp_clothoid.YStart]
        c = center
        dxy = [(sfactor - 1) * (i - j) for i, j in zip(s, c)]
        temp_clothoid._ClothoidCurve._translate(
            *dxy
        )  ##DANGER WILL ROBINSON : MUTATING STATE DIRECTLY##
        return temp_clothoid

    def Translate(self, xoff, yoff):
        """
        Returns a copy of the calling clothoid subjected to a pure translation transform described by a vector
        (xoff,yoff)
        """
        temp_clothoid = self.__class__(self)
        temp_clothoid._ClothoidCurve._translate(
            xoff, yoff
        )  ##DANGER WILL ROBINSON : MUTATING STATE DIRECTLY##
        return temp_clothoid

    def Rotate(self, angle, center=(0, 0)):
        """
        Returns a copy of the calling clothoid subjected to a pure rotation transform of angle and a
        stationary point at center
        """
        cx, cy = center
        temp_clothoid = self.__class__(self)
        temp_clothoid._ClothoidCurve._rotate(
            angle, cx, cy
        )  ##DANGER WILL ROBINSON : MUTATING STATE DIRECTLY##
        return temp_clothoid

    def Reverse(self):
        """
        Returns a copy of the calling clothoid with the direction of the arc length parameter reversed
        """
        temp_clothoid = self.__class__(self)
        temp_clothoid._ClothoidCurve._reverse()  ##DANGER WILL ROBINSON : MUTATING STATE DIRECTLY##
        return temp_clothoid

    def Trim(self, s_begin, s_end):
        """
        Returns a copy of the subsection of the calling clothoid that lies between s_begin and s_end
        """
        temp_clothoid = self.__class__(self)
        temp_clothoid._ClothoidCurve._trim(
            s_begin, s_end
        )  ##DANGER WILL ROBINSON : MUTATING STATE DIRECTLY##
        return temp_clothoid

    def Flip(self, axis="y"):
        """
        Returns a copy of the calling clothoid that has been flipped symmetrically along a specified axis

        currently supported options are:

        * 'y'
        * 'x'
        * 'start'

        Where 'start' represents a line tangent to the clothoid at its starting point.
        """
        xp = self.XStart
        yp = self.YStart
        th = self.ThetaStart
        dx = cos(th)
        dy = sin(th)
        if axis == "y":
            return self.__class__.StandardParams(
                -xp, yp, atan2(dy, -dx), -self.KappaStart, -self.dk, self.length
            )
        if axis == "x":
            return self.__class__.StandardParams(
                xp, -yp, atan2(-dy, dx), -self.KappaStart, -self.dk, self.length
            )
        if axis == "start":
            return self.__class__.StandardParams(
                xp, yp, th, -self.KappaStart, -self.dk, self.length
            )

    def ClosestPoint(self, X, Y):
        """
        Returns a tuple containing the cartesian coordinates of the point on the clothoid which is closest to
        the point defined by the X and Y input arguments.

        This method calls the `ProjectPointOntoClothoid` method and returns only the coordinate return values
        """
        ProjectedPoint, _, _ = self.ProjectPointOntoClothoid(X, Y)
        return ProjectedPoint

    def ClosestPointArcLength(self, X, Y):
        """
        Returns the arc length along the clothoid associated with the point on the clothoid which is closest
        to the point defined by the X and Y input arguments.

        This method calls the `ProjectPointOntoClothoid` method and returns only the arc length return value
        """
        _, ProjectedArclength, _ = self.ProjectPointOntoClothoid(X, Y)
        return ProjectedArclength

    def Distance(self, X, Y):
        """
        Returns the minimum distance between a given point and the clothoid.

        This method calls the `ProjectPointOntoClothoid` method and returns only the distance return value
        """
        _, _, ProjectionDistance = self.ProjectPointOntoClothoid(X, Y)
        return ProjectionDistance

    def _ProjectPointOntoClothoid(self, X, Y):
        ProjectedX, ProjectedY, ProjectedArclength, ProjectionDistance = (
            self._ClothoidCurve._project_point_to_clothoid(X, Y)
        )
        return ((ProjectedX, ProjectedY), ProjectedArclength, ProjectionDistance)

    def IntersectionArcLengths(self, other):
        """
        Returns a list of tuples.  Each tuple contains a pair of clothoid arc length parameters near which an
        intersection occurs.  The first parameter is the distance along the calling clothoid (self) at which
        the intersection occurs, and the second parameter is the distance along the argument clothoid (other).

        Note that due to the numerical methods and iterative approximation methods involved, the floating point
        coordinates of the intersection point on the first clothoid will not exactly coincide with the coordinates
        of the intersection point on the second clothoid.  However we expect this error be extremely small.
        """
        return self._ClothoidCurve._intersections(other._ClothoidCurve)

    def IntersectionPoints(self, other):
        """
        Returns a list of tuples.  Each tuple contains the X and Y cartesian coordinates near which the two clothoids
        intersect.  Approximations are computed using the calling clothoid and will likely differ slightly if computed
        using the other clothoid.
        """
        return [
            (self.X(i), self.Y(i))
            for i, _ in self._ClothoidCurve._intersections(other._ClothoidCurve)
        ]


def SolveG2(x0, y0, t0, k0, x1, y1, t1, k1, Dmax=0, dmax=0):
    """
    Returns a tuple of three Clothoids that form a G2 continuous path that interpolates two cartesian
    endpoints, two tangents, and two curvatures.  Exposes two additional parameters for fine tuning
    the properties of the desired solution.
    """
    solver = G2solve3arc()
    solver.build(x0, y0, t0, k0, x1, y1, t1, k1, Dmax, dmax)
    return tuple(map(Clothoid, (solver.getS0(), solver.getSM(), solver.getS1())))
