#ifndef RANDOM_WALK_H_
#define RANDOM_WALK_H_

#include <vector>
#include <array>

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

    std::array<int, 4> findStart();
    std::array<int, 4> walkOnce(std::array<int, 4>);

  private:
    int MAX_X, MAX_Y, MAX_Z;
    int**** site, loc_dnes;
    std::vector<std::array<int, 4>> atom_list;
};
#endif