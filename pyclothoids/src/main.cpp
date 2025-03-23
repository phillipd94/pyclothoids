/*
Author: Phillip Dix
*/

#ifdef _WIN32
#include <pybind11\pybind11.h>
#include <pybind11\stl.h>
#else
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#endif

#include <G2lib.hh>
#include <Clothoid.hh>
#include <ClothoidList.hh>

namespace py = pybind11;


PYBIND11_MODULE(_clothoids_cpp, m) {
    m.doc() = "This module is a partial pybind11 wrapper of Enrico Bertolazzi's C++ library for clothoid curves.  The C++ code can be found on github and is distributed under a BSD License at https://github.com/ebertolazzi/Clothoids.";

    py::class_<G2lib::ClothoidCurve>(m, "ClothoidCurve")
        .def(py::init<G2lib::ClothoidCurve>())
        .def(py::init<>())
        .def("build",(void (G2lib::ClothoidCurve::*)(G2lib::real_type, G2lib::real_type, G2lib::real_type, G2lib::real_type, G2lib::real_type, G2lib::real_type)) &G2lib::ClothoidCurve::build,
            py::arg("x0"), py::arg("y0"), py::arg("t0"), py::arg("k0"), py::arg("dk"), py::arg("L"))
        .def("build_G1", &G2lib::ClothoidCurve::build_G1,
            py::arg("x0"), py::arg("y0"), py::arg("t0"), py::arg("x1"), py::arg("y1"), py::arg("t1"), py::arg("tol"))
        .def("build_forward", &G2lib::ClothoidCurve::build_forward,
            py::arg("x0"), py::arg("y0"), py::arg("t0"), py::arg("k0"), py::arg("x1"), py::arg("y1"), py::arg("tol"))

        .def("Theta", &G2lib::ClothoidCurve::theta, py::arg("s"))
        .def("ThetaD", &G2lib::ClothoidCurve::theta_D, py::arg("s"))
        .def("ThetaDD", &G2lib::ClothoidCurve::theta_DD, py::arg("s"))
        .def("ThetaDDD", &G2lib::ClothoidCurve::theta_DDD, py::arg("s"))

        .def("X", &G2lib::ClothoidCurve::X, py::arg("s"))
        .def("XD", &G2lib::ClothoidCurve::X_D, py::arg("s"))
        .def("XDD", &G2lib::ClothoidCurve::X_DD, py::arg("s"))
        .def("XDDD", &G2lib::ClothoidCurve::X_DDD, py::arg("s"))

        .def("Y", &G2lib::ClothoidCurve::Y, py::arg("s"))
        .def("YD", &G2lib::ClothoidCurve::Y_D, py::arg("s"))
        .def("YDD", &G2lib::ClothoidCurve::Y_DD, py::arg("s"))
        .def("YDDD", &G2lib::ClothoidCurve::Y_DDD, py::arg("s"))

        .def("length", &G2lib::ClothoidCurve::length)
        .def("dk", &G2lib::ClothoidCurve::dkappa)
        .def("ThetaStart", &G2lib::ClothoidCurve::thetaBegin)
        .def("ThetaEnd", &G2lib::ClothoidCurve::thetaEnd)
        .def("XStart", &G2lib::ClothoidCurve::xBegin)
        .def("XEnd", &G2lib::ClothoidCurve::xEnd)
        .def("YStart", &G2lib::ClothoidCurve::yBegin)
        .def("YEnd", &G2lib::ClothoidCurve::yEnd)
        .def("KappaStart", &G2lib::ClothoidCurve::kappaBegin)
        .def("KappaEnd", &G2lib::ClothoidCurve::kappaEnd)

        .def("_translate", &G2lib::ClothoidCurve::translate, py::arg("dx"), py::arg("dy"), "DANGER: EXPOSED MUTABLE STATE!!  This function translates the clothoid curve in cartesian space")
        .def("_rotate", &G2lib::ClothoidCurve::rotate, py::arg("angle"), py::arg("x_center") = 0, py::arg("y_center") = 0, "DANGER: EXPOSED MUTABLE STATE!!  This function rotates the clothoid curve in cartesian space")
        .def("_scale", &G2lib::ClothoidCurve::scale, py::arg("scale_factor"), "DANGER: EXPOSED MUTABLE STATE!!  This function scales the clothoid curve in cartesian space")
        .def("_reverse", &G2lib::ClothoidCurve::reverse, "DANGER: EXPOSED MUTABLE STATE!!  This function reverses the curvature of the clothoid curve in cartesian space")
        .def("_trim", &G2lib::ClothoidCurve::trim, py::arg("s_begin"),py::arg("s_end"), "DANGER: EXPOSED MUTABLE STATE!!  This function removes parts of the curve outside the provided parameter range")
        
        .def("_intersections",
            [](const G2lib::ClothoidCurve& self, const G2lib::ClothoidCurve& OtherClothoid) {
                G2lib::IntersectList ilist;
                self.intersect_ISO(0.0, OtherClothoid, 0.0, ilist, false);
                
                std::vector<std::pair<G2lib::real_type, G2lib::real_type>> result(ilist.begin(), ilist.end());
                return result;
            },
            py::keep_alive<1, 2>(), // make sure python can't garbage collect this while we're running
            py::arg("OtherClothoid")
        )
        .def("_project_point_to_clothoid",
            [](const G2lib::ClothoidCurve& self, G2lib::real_type X, G2lib::real_type Y) {
                G2lib::real_type x, y, s, t, DST;
                G2lib::int_type result = self.closestPoint_ISO(X, Y, 0.0, x, y, s, t, DST);
                return std::make_tuple(x, y, s, DST);
            },
            py::arg("X"),
            py::arg("Y")
        )
        ;


    py::class_<G2lib::G2solve3arc>(m, "G2solve3arc")
        .def(py::init<>())
        .def("build",&G2lib::G2solve3arc::build, py::arg("x0"), py::arg("y0"), py::arg("t0"), py::arg("k0"), py::arg("x1"), py::arg("y1"), py::arg("t1"), py::arg("k1"), py::arg("Dmax") = 0, py::arg("dmax") = 0)
        .def("totalLength",&G2lib::G2solve3arc::totalLength)
        .def("getS0", &G2lib::G2solve3arc::getS0)
        .def("getS1", &G2lib::G2solve3arc::getS1)
        .def("getSM", &G2lib::G2solve3arc::getSM)
        ;
}