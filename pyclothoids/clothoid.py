from ._clothoids_cpp import ClothoidCurve, G2solve3arc

import numpy as np

CLOTHOID_FUNCTION_WINDOW = frozenset(("X","XD","XDD","XDDD","Y","YD","YDD","YDDD",
                                "Theta","ThetaD","ThetaDD","ThetaDDD"))

CLOTHOID_PROPERTY_WINDOW = frozenset(("length","dk","ThetaStart","ThetaEnd","XStart",
                                "XEnd","YStart","YEnd","KappaStart","KappaEnd"))

class Clothoid(object):
    def __init__(self,clothoid_curve):
        if type(clothoid_curve) == type(self):
            #Create a copy of the underlying C++ clothoid when constructor is called with a Python Clothoid
            self._ClothoidCurve = ClothoidCurve(clothoid_curve._ClothoidCurve)
        else:
            #No need to create a copy when a C++ clothoid is passed directly by the classmethods or G2solver
            self._ClothoidCurve = clothoid_curve
    
    @classmethod
    def StandardParams(cls,x0,y0,t0,k0,kd,s_f):
        temp_clothoid = ClothoidCurve()
        temp_clothoid.build(x0,y0,t0,k0,kd,s_f)
        return cls(temp_clothoid) 
    
    @classmethod
    def G1Hermite(cls,x0,y0,t0,x1,y1,t1):
        temp_clothoid = ClothoidCurve()
        temp_clothoid.build_G1(x0,y0,t0,x1,y1,t1)
        return cls(temp_clothoid)
    
    def __getattr__(self,name):
        if name in CLOTHOID_FUNCTION_WINDOW:
            return getattr(self._ClothoidCurve,name)
        if name in CLOTHOID_PROPERTY_WINDOW:
            return getattr(self._ClothoidCurve,name)() #mimic property getter syntax
        return super().__getattribute__(name)()
    
    def __str__(self):
        return 'Clothoid: ' + ''.join(map(lambda m,n:m + ':' + str(getattr(self,n)) + ' ',
                                             ('x0','y0','y0','k0','kd','s'),('XStart','YStart','ThetaStart','KappaStart','dk','length')))
    
    def __repr__(self):
        return str(self)
    
    def __getstate__(self):
        return self.Parameters
    
    def __setstate__(self,state):
        temp_clothoid = ClothoidCurve()
        self._ClothoidCurve = temp_clothoid.build(*state)
    
    def SampleXY(self,npts):
        return [[j(i) for i in np.linspace(0,self.length,npts)] for j in (self.X,self.Y)] #TODO: move sampling to c++ layer for loop efficiency?

    @property
    def Parameters(self):
        return (self.XStart,self.YStart,self.ThetaStart,self.KappaStart,self.dk,self.length)

    def Scale(self,sfactor,center = (0,0)):
        if sfactor == 0:
            return Clothoid.StandardParams(0,0,0,0,0,0)
        temp_clothoid = Clothoid(self)
        temp_clothoid._ClothoidCurve._scale(sfactor) ##DANGER WILL ROBINSON : MUTATING STATE DIRECTLY##
        if center == 'start':
            return temp_clothoid
        s = np.array([temp_clothoid.XStart,temp_clothoid.YStart])
        c = np.array(center)
        dxy = (sfactor-1)*(s-c)
        temp_clothoid._ClothoidCurve._translate(*dxy) ##DANGER WILL ROBINSON : MUTATING STATE DIRECTLY##
        return temp_clothoid
    
    def Translate(self,xoff,yoff):
        temp_clothoid = Clothoid(self)
        temp_clothoid._ClothoidCurve._translate(xoff,yoff) ##DANGER WILL ROBINSON : MUTATING STATE DIRECTLY##
        return temp_clothoid
    
    def Rotate(self,angle,cx = 0,cy = 0):
        temp_clothoid = Clothoid(self)
        temp_clothoid._ClothoidCurve._rotate(angle,cx,cy) ##DANGER WILL ROBINSON : MUTATING STATE DIRECTLY##
        return temp_clothoid
    
    def Reverse(self):
        temp_clothoid = Clothoid(self)
        temp_clothoid._ClothoidCurve._reverse() ##DANGER WILL ROBINSON : MUTATING STATE DIRECTLY##
        return temp_clothoid
    
    def Trim(self,s_begin,s_end):
        temp_clothoid = Clothoid(self)
        temp_clothoid._ClothoidCurve._trim(s_begin,s_end) ##DANGER WILL ROBINSON : MUTATING STATE DIRECTLY##
        return temp_clothoid
    
    def Flip(self,axis = 'y'):
        xp = self.XStart
        yp = self.YStart
        th = self.ThetaStart
        dx = np.cos(th)
        dy = np.sin(th)
        if axis == 'y':
            return Clothoid.StandardParams(-xp,yp,np.arctan2(dy,-dx),-self.KappaStart,-self.dk,self.length)
        if axis == 'x':
            return Clothoid.StandardParams(xp,-yp,np.arctan2(-dy,dx),-self.KappaStart,-self.dk,self.length)
        if axis == 'start':
            return Clothoid.StandardParams(xp,yp,th,-self.KappaStart,-self.dk,self.length)
        

def SolveG2(x0,y0,t0,k0,x1,y1,t1,k1):
    solver = G2solve3arc()
    solver.build(x0,y0,t0,k0,x1,y1,t1,k1,0,0)
    return tuple(map(Clothoid,(solver.getS0(),solver.getSM(),solver.getS1())))
    
    