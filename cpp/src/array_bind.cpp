#include "array.h"
#include <pybind11/pybind11.h>
namespace py = pybind11;

template<typename T>
void bind_array2(py::module &m, std::string&& typestr) {
    using Array2 = Array2<T>;
    std::string pyclass_name = std::string("Array2") + typestr;
    py::class_<Array2>(m, pyclass_name.c_str(), py::buffer_protocol())
        .def(py::init<int>())
        .def(py::init<int, int>())
        .def_buffer([] (Array2& arr) -> py::buffer_info {
            return py::buffer_info(
                arr.data(),
                sizeof(T),
                py::format_descriptor<T>::format(),
                2,
                {arr.get_nrows(), arr.get_ncols()},
                {sizeof(T) * arr.get_ncols(), sizeof(T)});
        });
}

PYBIND11_MODULE(arrayTest, m) {
    m.doc() = "Array class";

    bind_array2<int>(m, "i");
    bind_array2<float>(m, "f");

}