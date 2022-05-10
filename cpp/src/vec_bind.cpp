#include "vec.h"
#include <pybind11/pybind11.h>
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

PYBIND11_MODULE(vec, m) {
    m.doc() = "Vector class";

    bind_vec3<int>(m, "i");
    bind_vec3<float>(m, "f");

}