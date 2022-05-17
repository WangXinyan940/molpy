#include "vec.h"
#include "simpleRW.h"
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
namespace py = pybind11;

template<typename T>
void bind_vec3(py::module &m, std::string&& typestr) {
    using Vec3 = Vec3<T>;
    std::string pyclass_name = std::string("Vec3") + typestr;
    py::class_<Vec3>(m, pyclass_name.c_str(), py::buffer_protocol())
        .def(py::init<>())
        .def(py::init<T, T, T>())
        .def_buffer([] (Vec3& v) -> py::buffer_info {
            return py::buffer_info(
                &v.x,
                sizeof(T),
                py::format_descriptor<T>::format(),
                1,
                {3},
                {sizeof(T)});
        })
        .def_readwrite("x", &Vec3::x)
        .def_readwrite("y", &Vec3::y)
        .def_readwrite("z", &Vec3::z)
        .def("__repr__", [](const Vec3& v) {
            return "<Vec3(" + std::to_string(v.x) + ", " + std::to_string(v.y) + ", " + std::to_string(v.z) + ")>";
        });    
}


PYBIND11_MODULE(molpy_cpp, m) {
    m.doc() = "molpy workload in cpp";

    // RandomWalk
    py::module m_randomWalk = m.def_submodule("randomWalk");

    py::class_<SimpleRW>(m_randomWalk, "SimpleRW", py::buffer_protocol())
        .def(py::init<>())
        .def("walk", &SimpleRW::walk, "walk func")
        .def("reset", &SimpleRW::reset, "reset")
        .def("getPositions", 
            [](SimpleRW &m) -> py::array { 
                Positions positions = m.getPositions();
                return py::array(py::buffer_info(
                    positions.ptr(),
                    sizeof(positions.dtype()),
                    py::format_descriptor<double>::format(),
                    positions.ndim,
                    positions.shape,
                    positions.strides
                )); 
            }, "get positions")
        .def("getLinks",
            [](SimpleRW &m) -> py::array { 
                Links links = m.getLinks();
                return py::array(py::buffer_info(
                    links.ptr(),
                    sizeof(links.dtype()),
                    py::format_descriptor<int>::format(),
                    links.ndim,
                    links.shape,
                    links.strides
                )); 
            }, "get links");


    // Math
    py::module m_math = m.def_submodule("math");
        m.doc() = "math";
        bind_vec3<int>(m, "i");
        bind_vec3<float>(m, "f");

}
