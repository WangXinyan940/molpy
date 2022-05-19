
#include "simpleRW.h"
#include <iostream>

SimpleRW::SimpleRW(double box_lo, double box_hi) {

    std::random_device rand_seed;
    generator = std::default_random_engine(rand_seed());
    theta_gen = std::uniform_real_distribution<double>(0.0, 2.0 * M_PI);  //azimuth
    phi_gen = std::uniform_real_distribution<double>(0.0, M_PI);  //zenith
    pos_gen = std::uniform_real_distribution<double>(box_lo, box_hi);  //x,y,z

}

SimpleRW::~SimpleRW() { }

Vec SimpleRW::findStart() {
    double x = pos_gen(generator);
    double y = pos_gen(generator);
    double z = pos_gen(generator);
    Vec start = {x, y, z};
    return start;
}

Positions SimpleRW::walkOnce(int lchain, double stepsize) {

    Vec next = findStart();
    return walkOnceFrom(next, lchain, stepsize);

}

Positions SimpleRW::walkOnceFrom(Vec next, int lchain, double stepsize) {

    Positions thisWalkPositions = Positions();

    for (int i = 0; i < lchain; i++) {
        thisWalkPositions.append({next.x, next.y, next.z});
        next = walkOneStep(next, stepsize);
    }

    thisWalkPositions.shape = {lchain, 3};

    return thisWalkPositions;    

}

Vec SimpleRW::walkOneStep(Vec now, double stepsize) {

    double theta = theta_gen(generator);
    double phi = phi_gen(generator);

    Vec delta = {stepsize*sin(phi)*cos(theta), stepsize*sin(phi)*sin(theta), stepsize*cos(phi)};
    return now + delta;

}
