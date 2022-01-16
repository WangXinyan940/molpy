
#include"randomWalk.h"
#include<stdio.h>
#include<stdlib.h>

// RandomWalk::RandomWalk() : MAX_X(100), MAX_Y(100), MAX_Z(100) {}
RandomWalk::RandomWalk(int MAX_X, int MAX_Y, int MAX_Z) : MAX_X(MAX_X), MAX_Y(MAX_Y), MAX_Z(MAX_Z) {
  create(site, MAX_X, MAX_Y, MAX_Z, 4);
}

std::array<int, 4> RandomWalk::findStart() {
  // [0, n) := rand()%n
  // [a, b) := (rand() % (b-a)) + a
  // [a, b] := (rand() % (b-a+1)) + a
  // (a, b] := (rand() % (b-a)) + a + 1
  // to sum up: a + rand() % n, where a is start and n in the range

  // for float, a + int(b) * rand() / (RAND_MAX + 1)
  // (0, 1) := rand() / double(RAND_MAX)

  int i, j, k, l;
  do {
    i = (rand() % (MAX_X));
    j = (rand() % (MAX_Y));
    k = (rand() % (MAX_Z));
    l = (rand() % 4);
  }
  while (site[i][j][k][l] != 0);
  site[i][j][k][l] = 1;
  std::array<int, 4> start {{i,j,k,l}};
  atom_list.push_back(start);
  return start;
}

std::array<int, 4> RandomWalk::walkOnce(std::array<int, 4> start) {

}

std::array<int, 4> RandomWalk::linear() {
  std::array<int, 4> start = find_start();
  std::array<int, 4> end = walk_once(start);
}

RandomWalk::lookForNeighbor() {
  
}

RandomWalk::wrap() {

}

int main() {
  // // RandomWalk rw(10, 20, 30);
  // RandomWalk* rw = new RandomWalk(10, 20, 30);
  RandomWalk rw = RandomWalk();

  // vec3<float> v0 = vec3<float>(0, 1, 2);
  // std::cout << v0.z << std::endl;

}