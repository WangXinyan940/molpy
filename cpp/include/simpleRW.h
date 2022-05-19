#ifndef SIMPLERW_H
#define SIMPLERW_H

#include <random>
#include <iostream>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include "vec.h"
#include "array.h"

namespace py = pybind11;
using Positions = Array<double>;
using Vec = Vec3<double>;

class SimpleRW {

    public:
        SimpleRW(double box_lo, double box_hi);
        ~SimpleRW();
        void reset();
        Positions getPositions();
        Vec findStart();
        Positions walkOnce(int lchain, double stepsize);
        Positions walkOnceFrom(Vec start, int lchain, double stepsize);

    private:

        std::default_random_engine generator;
        std::uniform_real_distribution<double> theta_gen;
        std::uniform_real_distribution<double> phi_gen;
        std::uniform_real_distribution<double> pos_gen;
        Vec walkOneStep(Vec now, double stepsize);

};

#endif