Math Conventions
================

A Clothoid for the purposes of this software is any curve for which the curvature is a linear function of arc length.  Put another way, the derivative of curvature with respect to arc length must be a constant value.  Any such curve can be expressed parametrically in the following form:

.. math::
	:nowrap:
	
	\begin{eqnarray*}
	x(s) &= x_0 + \int_0^s \cos\left(\frac{\dot{\kappa}}{2}s^2 + \kappa_0 s + t_0\right) ds\\
	y(s) &= y_0 + \int_0^s \sin\left(\frac{\dot{\kappa}}{2}s^2 + \kappa_0 s + t_0\right) ds\\
	\end{eqnarray*}
	
With curvature and tangent angle described by:

.. math::
	:nowrap:
	
	\begin{eqnarray*}
	\kappa(s) &=& \dot{\kappa}s + \kappa_0\\
	t(s) &=& \frac{\dot{\kappa}}{2}s^2 + \kappa_0 s + t_0\\
	\end{eqnarray*}
	
Where each math symbol is mapped to a name in the software and a description according to the following table:

.. table:: Nomenclature for Clothoid Properties
	:widths: auto
	:align: center
   
	======================  ================   ======================
	Math Symbol              Code Symbol       Description
	======================  ================   ======================
	:math:`x_0`                x0                initial X coordinate
	:math:`y_0`                y0                initial Y coordinate
	:math:`s`                  s                 arc length
	:math:`\dot{\kappa}`       kd                derivative of curvature
	:math:`\kappa_0`           k0                initial curvature
	:math:`t_0`                t0                initial tangent angle
	======================  ================   ======================