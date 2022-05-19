#include "vec.h"
#include "simpleRW.h"
#include <funcobject.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
namespace py = pybind11;

namespace pybind11 { namespace detail {
    template <typename T> struct type_caster<Vec3<T>> {
    public:
        /**
         * This macro establishes the name 'Vec3' in
         * function signatures and declares a local variable
         * 'value' of type Vec3
         */
        PYBIND11_TYPE_CASTER(Vec3<T>, _("Vec3<T>"));

        /**
         * Conversion part 1 (Python->C++): convert a PyObject into a Vec3
         * instance or return false upon failure. The second argument
         * indicates whether implicit conversions should be applied.
         */
        bool load(handle src, bool convert) {

            if (!convert && !py::array_t<T>::check_(src))
                return false;

            auto buf = py::array_t<T, py::array::c_style | py::array::forcecast>::ensure(src);
            if (!buf)
                return false;

            auto ndim = buf.ndim();
            if (ndim != 1)
                return false;
            
            std::vector<size_t> shape(buf.ndim());

            for (int i=0; i<buf.ndim(); i++)
                shape[i] = buf.shape()[i];

            value = Vec3<T>();
            value.x = buf.data()[0];
            value.y = buf.data()[1];
            value.z = buf.data()[2];

            return true;
        }

        /**
         * Conversion part 2 (C++ -> Python): convert a Vec3 instance into
         * a Python object. The second and third arguments are used to
         * indicate the return value policy and parent object (for
         * ``return_value_policy::reference_internal``) and are generally
         * ignored by implicit casters.
         */
        static py::handle cast(const Vec3<T>& src, py::return_value_policy policy /* policy */, py::handle parent /* parent */) {
            // return src.to_numpy().release();
            return py::array(3, &src.x).release();
        }
    };
}} // Vec3

namespace pybind11 { namespace detail {
    template <typename T> struct type_caster<Array<T>> {
    public:
        /**
         * This macro establishes the name 'Array' in
         * function signatures and declares a local variable
         * 'value' of type Array
         */
        PYBIND11_TYPE_CASTER(Array<T>, _("Array<T>"));

        /**
         * Conversion part 1 (Python->C++): convert a PyObject into an Array
         * instance or return false upon failure. The second argument
         * indicates whether implicit conversions should be applied.
         */
        bool load(handle src, bool convert) {

            if (!convert && !py::array_t<T>::check_(src))
                return false;

            auto buf = py::array_t<T, py::array::c_style | py::array::forcecast>::ensure(src);
            if (!buf)
                return false;

            auto ndim = buf.ndim();
            if (ndim != 1)
                return false;
            
            std::vector<size_t> shape(buf.ndim());

            for (int i=0; i<buf.ndim(); i++)
                shape[i] = buf.shape()[i];

            value = Array<T>();
            value.data = std::vector<T>(buf.data(), buf.data() + buf.size());

            return true;
        }

        /**
         * Conversion part 2 (C++ -> Python): convert an Array instance into
         * a Python object. The second and third arguments are used to
         * indicate the return value policy and parent object (for
         * ``return_value_policy::reference_internal``) and are generally
         * ignored by implicit casters.
         */
        static py::handle cast(const Array<T>& src, py::return_value_policy policy /* policy */, py::handle parent /* parent */) {

            py::array arr;

            if (src.getNdim()) {  // shape is not set
            std::cout << "strides.size() == 0" << std::endl;
                arr = py::array(src.getSize(), src.getPtr());
            }
            else if (src.getNdim()) {  // shape is set
            std::cout << "strides.size() != 0" << std::endl; 
                arr = py::array(src.shape, src.getPtr());
            }

            return arr.release();
        }
    };
}} // Array

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
        .def("walk", &SimpleRW::walk, "walk func", py::arg("lchain"), py::arg("nchain"))
        .def("reset", &SimpleRW::reset, "reset")
        .def("getPositions", &SimpleRW::getPositions, "get positions")
        .def("walkOnce", &SimpleRW::walkOnce, 
             "walk once from random start", 
             py::arg("lchain"))
        .def("walkOnceFrom", &SimpleRW::walkOnceFrom, 
             "walk once from specific start", 
             py::arg("start"), py::arg("lchain"))
        .def("findStart", &SimpleRW::findStart, 
            "find a random walk start"
            );


    // Math
    py::module m_math = m.def_submodule("math");
        m_math.doc() = "math";
        bind_vec3<int>(m_math, "i");
        bind_vec3<float>(m_math, "f");

}
