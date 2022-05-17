#ifndef SIMPLERW_H
#define SIMPLERW_H

#include <random>
#include <iostream>
#include "vec.h"
#include "array.h"

using Positions = Array<double>;
using Links = Array<int>;
using Vec = Vec3<double>;

class SimpleRW {

    public:
        SimpleRW();
            
        ~SimpleRW();
        void walk(int lchain, int nchain);
        void reset();
        Positions getPositions();
        Links getLinks();

    private:
        double bondLength;
        std::default_random_engine generator;
        std::uniform_real_distribution<double> theta_gen;
        std::uniform_real_distribution<double> phi_gen;
        std::uniform_real_distribution<double> pos_gen;
        Vec walkOneStep(Vec now);
        Vec walkOnce(int lchain);
        Vec findStart();
        int nsteps, nlinks;
        Positions positions;
        Links links;
};

#endif