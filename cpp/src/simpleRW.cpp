
#include "simpleRW.h"
#include <iostream>

SimpleRW::SimpleRW() {

    bondLength = 1.0;
    double xlo = 0;
    double xhi = 10;
    std::random_device rand_seed;
    generator = std::default_random_engine(rand_seed());
    theta_gen = std::uniform_real_distribution<double>(0.0, 2.0 * M_PI);  //azimuth
    phi_gen = std::uniform_real_distribution<double>(0.0, M_PI);  //zenith
    pos_gen = std::uniform_real_distribution<double>(xlo, xhi);  //x,y,z
    positions = Positions();
    nsteps = 0;
    nlinks = 0;

}

void SimpleRW::reset() {
    positions.clear();
}

SimpleRW::~SimpleRW() { }

Vec SimpleRW::findStart() {
    double x = pos_gen(generator);
    double y = pos_gen(generator);
    double z = pos_gen(generator);
    Vec start = {x, y, z};
    return start;
}

void SimpleRW::walk(int lchain, int nchain) {
    for (int i = 0; i < nchain; i++) {
        walkOnce(lchain);
    }
}

Positions SimpleRW::walkOnce(int lchain) {

    Vec next = findStart();
    return walkOnceFrom(next, lchain);

}

Positions SimpleRW::walkOnceFrom(Vec next, int lchain) {

    Positions thisWalkPositions = Positions();

    for (int i = 0; i < lchain; i++) {

        positions.append({next.x, next.y, next.z});
        thisWalkPositions.append({next.x, next.y, next.z});
        if (i != 0) {
            nlinks++;
        }
        nsteps++;
        next = walkOneStep(next);
    }

    thisWalkPositions.shape = {lchain, 3};

    return thisWalkPositions;    

}

Vec SimpleRW::walkOneStep(Vec now) {

    double theta = theta_gen(generator);
    double phi = phi_gen(generator);

    Vec delta = {bondLength*sin(phi)*cos(theta), bondLength*sin(phi)*sin(theta), bondLength*cos(phi)};
    return now + delta;

}

Positions SimpleRW::getPositions() {

    positions.shape = {nsteps, 3};

    return positions;
}
