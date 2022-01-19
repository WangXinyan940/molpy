#ifndef RANDOM_WALK_H_
#define RANDOM_WALK_H_

#include<vector>
#include<array>
#include<math.h>
#include<cstdio>

#define PI 3.14159265
#define SQRT22 0.707

using arr4int = std::array<int, 4>;
using arr3int = std::array<int, 3>;
using arr4float = std::array<float, 4>;
using arr3float = std::array<float, 3>;

class RandomWalk {
    public:
        RandomWalk(int nsite_x=100, int nsite_y=100, int nsite_z=100);
        ~RandomWalk();
        arr4int findStart();
        arr3float site2Coord(int);
        arr4int walkOneStep(arr4int, arr4int);
        arr4int walkOnce(arr4int, int);
        arr4int linear(int);
        arr4int wrapOnSite(arr4int);

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
        
    private:
        int nsite_x, nsite_y, nsite_z;
        int**** site;
        int**** unoccupied_neighbors;
        std::vector<arr4int> atom_list;

};
#endif