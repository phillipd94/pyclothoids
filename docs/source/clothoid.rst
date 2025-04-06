Clothoid
========

.. autoclass:: pyclothoids.Clothoid
	
	.. automethod:: StandardParams
	.. automethod:: G1Hermite
	.. automethod:: Forward
	.. autoattribute:: Parameters
	.. attribute:: length

		The total arc length of the Clothoid

		:getter: Returns the arc length of the clothoid
		:setter: Arc length cannot be modified
		:type: float
		
	.. attribute:: dk

		The curvature rate of the Clothoid

		:getter: Returns the curvature rate of the clothoid
		:setter: Curvature rate cannot be modified
		:type: float
	
	.. attribute:: XStart

		The X coordinate of the Clothoid at its starting point

		:getter: Returns the initial X coordinate of the clothoid
		:setter: Initial X coordinate cannot be modified
		:type: float
    
	.. attribute:: XEnd

		The X coordinate of the Clothoid at its end point

		:getter: Returns the final X coordinate of the clothoid
		:setter: Final X coordinate cannot be modified
		:type: float
	
	.. attribute:: YStart

		The Y coordinate of the Clothoid at its starting point

		:getter: Returns the initial Y coordinate of the clothoid
		:setter: Initial Y coordinate cannot be modified
		:type: float
	
	.. attribute:: YEnd

		The Y coordinate of the Clothoid at its end point

		:getter: Returns the final Y coordinate of the clothoid
		:setter: Final Y coordinate cannot be modified
		:type: float
		
			
	.. attribute:: ThetaStart

		The tangent angle of the Clothoid at its starting point

		:getter: Returns the initial tangent angle of the clothoid in radians
		:setter: Initial angle cannot be modified
		:type: float
	
	.. attribute:: ThetaEnd

		The tangent angle of the Clothoid at its end point

		:getter: Returns the final tangent angle of the clothoid in radians
		:setter: Final angle cannot be modified
		:type: float
	
	.. attribute:: KappaStart

		The curvature of the Clothoid at its starting point

		:getter: Returns the initial curvature of the clothoid
		:setter: Initial curvature cannot be modified
		:type: float
	
	.. attribute:: KappaEnd

		The curvature of the Clothoid at its end point

		:getter: Returns the final curvature of the clothoid
		:setter: Final curvature cannot be modified
		:type: float
		
	.. method:: X(s)
	
		Returns the X coordinate of the clothoid at arc length s from the initial point
		
	.. method:: XD(s)
	
		Returns the derivative of the X coordinate of the clothoid at arc length s from the initial point
	
	.. method:: XDD(s)
	
		Returns the second derivative of the X coordinate of the clothoid at arc length s from the initial point
	
	.. method:: XDDD(s)
	
		Returns the third derivative of the X coordinate of the clothoid at arc length s from the initial point
	
	.. method:: Y(s)
	
		Returns the Y coordinate of the clothoid at arc length s from the initial point
	
	.. method:: YD(s)
	
		Returns the derivative of the Y coordinate of the clothoid at arc length s from the initial point
	
	.. method:: YDD(s)
	
		Returns the second derivative of the Y coordinate of the clothoid at arc length s from the initial point
	
	.. method:: YDDD(s)
	
		Returns the third derivative of the Y coordinate of the clothoid at arc length s from the initial point

	.. method:: Theta(s)
	
		Returns the tangent angle of the clothoid at arc length s from the initial point
	
	.. method:: ThetaD(s)
	
		Returns the derivative of the tangent angle of the clothoid at arc length s from the initial point
	
	.. method:: ThetaDD(s)
	
		Returns the second derivative of the tangent angle of the clothoid at arc length s from the initial point
	
	.. method:: ThetaDDD(s)
	
		Returns the third derivative of the tangent angle of the clothoid at arc length s from the initial point
		
	.. automethod:: SampleXY
	.. automethod:: Scale
	.. automethod:: Translate
	.. automethod:: Rotate
	.. automethod:: Flip
	.. automethod:: Reverse
	.. automethod:: Trim

	.. automethod:: ClosestPoint
	.. automethod:: ClosestPointArcLength
	.. automethod:: Distance
	.. method:: ProjectPointOntoClothoid(X, Y)

		Calculates the minimum-distance projection of a given point onto the clothoid.  Returns a tuple containing the closest point coordinates, the arc length along the clothoid where the closest point lies, and the distance between the given point and the projected point on the clothoid.\nThis method is called by the `ClosestPoint`, `ClosestPointArcLength`, and `Distance` methods.  Because the Clothoid object is immutable, we wrap this method in an LRU cache on object construction to save outputs of recently used input points.\nThis allows a user to call `Distance` and `ClosestPoint` separately with the same input point for code readability without recomputing the underlying projection.

	.. automethod:: IntersectionPoints
	.. automethod:: IntersectionArcLengths
	.. automethod:: SetupProjectionCache