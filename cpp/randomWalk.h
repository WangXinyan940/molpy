#ifndef RANDOM_WALK_H_
#define RANDOM_WALK_H_

#include<vector>
#include<array>
#include<math.h>
#include<stdio.h>
#include<stdlib.h>

using vec4 = std::array<int, 4>;
using vec3 = std::array<int, 3>;

class RandomWalk {
  public:
    // RandomWalk() = default;
    RandomWalk(int site_x=100, int site_y=100, int site_z=100);


    template <typename T> T**** create(T****& arr, T x, T y, T z, T m) {
      arr = new T***[x];
        for (int i=0; i<x; i++) {
          arr[i] = new T**[y];
          for (int j=0; j<y; j++) {
            arr[i][j] = new T*[z];
            for (int k=0; k<z; k++) {
              arr[i][j][k] = new T[4];
              for (int l=0; l<m; l++) arr[i][j][k][l] = 0;
            }
          }
        }
      return arr;
    }

    template <typename T> void destroy(T****& arr) {

      for (int i=0; i<sizeof(arr)/sizeof(arr[0]); i++) {
        for (int j=0; j<sizeof(arr[0])/sizeof(arr[0][0]); j++) {
          for (int k=0; k<sizeof(arr[0][0])/sizeof(arr[0][0][0]); k++) {
            delete [] arr[i][j][k];
          }
          delete [] arr[i][j];
        }
        delete [] arr[i];
      }
      delete [] arr;
      return;
    }

    vec4 findStart();
    std::array<float, 3> mapSiteToCoord(int);
    vec4 walkOnce(vec4, int);
    void findNeighbors(vec4, int, int);
    void chooseNextStep(vec4, int&, int);
    void linear(int);

  private:
    int MAX_X, MAX_Y, MAX_Z;
    int**** site;
    int**** loc_dens;
    int reset;
    std::vector<vec4> atom_list;
    int st_ld[12][4];
    double va[3], vb[3], vc[3];
    double neigh[12][4], v_store[12][3], mag_store[12];
    int nn;
    float sqrt_2_2;
    float va_mag, vb_mag;
    vec4 atom;

};
#endif