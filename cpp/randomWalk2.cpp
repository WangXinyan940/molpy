#include "randomWalk2.h"

RandomWalk::RandomWalk(int nsite_x, int nsite_y, int nsite_z) : nsite_x(nsite_x), nsite_y(nsite_y), nsite_z(nsite_z) {
    create(site, nsite_x, nsite_y, nsite_z, 4);
    create(unoccupied_neighbors, nsite_x, nsite_y, nsite_z, 4);
}

RandomWalk::~RandomWalk() {
    destroy(site);
    destroy(unoccupied_neighbors);
}

arr4int RandomWalk::findStart()
{
  // [0, n) := rand()%n
  // [a, b) := (rand() % (b-a)) + a
  // [a, b] := (rand() % (b-a+1)) + a
  // (a, b] := (rand() % (b-a)) + a + 1
  // to sum up: a + rand() % n, where a is start and n in the range

  // for float, a + int(b) * rand() / (RAND_MAX + 1)
  // [0, 1) := rand() / double(RAND_MAX)

  int i, j, k, l;
  do
  {
    i = (rand() % (nsite_x));
    j = (rand() % (nsite_y));
    k = (rand() % (nsite_z));
    l = (rand() % 4);
  } while (site[i][j][k][l] != 0);
  site[i][j][k][l] = 1;
  arr4int start{{i, j, k, l}};
  atom_list.push_back(start);
  return start;
}

arr3float RandomWalk::site2Coord(int l)
{
  arr3float a;
  // mapping site indicator to coordinate
  if (l == 0)
  {
    a[0] = 0;
    a[1] = 0;
    a[2] = 0;
  }
  else if (l == 1)
  {
    a[0] = 0.5;
    a[1] = 0.5;
    a[2] = 0;
  }
  else if (l == 2)
  {
    a[0] = 0.5;
    a[1] = 0;
    a[2] = 0.5;
  }
  else
  {
    a[0] = 0;
    a[1] = 0.5;
    a[2] = 0.5;
  }
  return a;
}

arr4int RandomWalk::walkOneStep(arr4int current, arr4int previous) {

    int i = current[0];
    int j = current[1];
    int k = current[2];
    int m = current[3];
    
    int dx[3] {i-1, i, i+1};
    int dy[3] {j-1, j, j+1};
    int dz[3] {k-1, k, k+1};

    arr3float a, b, c;
    float va[3], vb[3];
    float va_mag, vb_mag;
    float angle, d_prod;
    float point;
    int first_coords[12][4];
    int fc_counter = 0;
    int alter_counter = 0;
    int prob_low, prob_high;
    int ii, jj;
    int alters[12][4];
    int v_store[12][4];
    int mag_store[12];
    int total_unoccupied, reset;
    arr4int atom;


    // wrap
    if (dx[2] == nsite_x)
        dx[2] = 0;
    if (dy[2] == nsite_y)
        dy[2] = 0;
    if (dz[2] == nsite_z)
        dz[2] = 0;
    if (dx[0] < 0)
        dx[0] = nsite_x - 1;
    if (dy[0] < 0)
        dy[0] = nsite_y - 1;
    if (dz[0] < 0)
        dz[0] = nsite_z - 1;

    b = site2Coord(m);

    // look for neighbors
    for(int ii=0;ii<3;ii++) {
        for(int jj=0;jj<3;jj++) {
            for(int kk=0;kk<3;kk++) {
                for(int mm=0;mm<4;mm++) {
            
                    c = site2Coord(mm);
                    c[0] = c[0] + ii - 1;
                    c[1] = c[1] + jj - 1;
                    c[2] = c[2] + kk - 1;

                    va[0] = c[0] - b[0];
                    va[1] = c[1] - b[1];
                    va[2] = c[2] - b[2];

                    va_mag = va[0]*va[0]+va[1]*va[1]+va[2]*va[2];

                    if (site[dx[ii]][dy[jj]][dz[kk]][mm]==0) {
                        if (va_mag <= 0.51) {
                            unoccupied_neighbors[dx[ii]][dy[jj]][dz[kk]][mm]++; //occupied
                            first_coords[fc_counter][0] = dx[ii];
                            first_coords[fc_counter][1] = dy[jj];
                            first_coords[fc_counter][2] = dz[kk];
                            first_coords[fc_counter][3] = mm;
                            fc_counter++;

                            if (previous==current) {
                                angle = 90;
                            }
                            else {
                                m = previous[3];
                                a = site2Coord(m);
                                previous[0] += a[0];
                                previous[1] += a[1];
                                previous[2] += a[2];
                                vb[0] = i - previous[0];
                                vb[1] = j - previous[1];
                                vb[2] = k - previous[2];

                                d_prod=va[0]*vb[0]+va[1]*vb[1]+va[2]*vb[2];
                                
                                angle=acos(d_prod/(va_mag*vb_mag))*180.0/PI;

                            }
                            if((angle<-60.0&&angle>-150.0)||(angle>60.0&&angle<150.0))
                            {
                                alters[alter_counter][0]=dx[ii];
                                alters[alter_counter][1]=dy[jj];
                                alters[alter_counter][2]=dz[kk];
                                alters[alter_counter][3]=mm;
                                v_store[alter_counter][0]=va[0];
                                v_store[alter_counter][1]=va[1];
                                v_store[alter_counter][2]=va[2];
                                mag_store[alter_counter]=va_mag;
                                alter_counter++;
                            }

                        }
                    }
                }
            }
        }
    }
    // choose next step

    if (alter_counter == 0) {
        if (previous==current) {
            atom = atom_list.back();
            atom_list.pop_back();
            return atom;  // return last one
        }
        else {
            return previous;
        }

    }
    else {
        std::array<int, 12> weight;
        for(ii=0; ii<alter_counter; ii++) {
            if (ii==0) weight[ii] = unoccupied_neighbors[first_coords[ii][0]][first_coords[ii][1]][first_coords[ii][2]][first_coords[ii][3]];
            else weight[ii] = weight[ii-1] + unoccupied_neighbors[first_coords[ii][0]][first_coords[ii][1]][first_coords[ii][2]][first_coords[ii][3]];
        }
        
        prob_low = 0;
        prob_high = weight[ii-1];
        point=rand()%prob_high;

        for (jj=0; jj<ii; jj++) {
            if (point<weight[jj]) break;
        }

        atom[0] = first_coords[jj][0];
        atom[1] = first_coords[jj][1];
        atom[2] = first_coords[jj][2];
        atom[3] = first_coords[jj][3];

        atom_list.push_back(atom);
        return atom;

        }
    
}

arr4int RandomWalk::walkOnce(arr4int current, int length) {
    int i = 0;
    arr4int previous(current), next;
    for (i=0; i<length; i++) {
        next = walkOneStep(current, previous);
        if (next==previous) {
            i--;
        }
        else {
            previous.swap(current);
            current.swap(next);
        }
    }
    return current;
}

arr4int RandomWalk::linear(int length) {
    arr4int start = findStart();
    return walkOnce(start, length);
}

int main() {
    RandomWalk rw = RandomWalk(10, 10, 10);
    arr4int atom = rw.findStart();
    printf("(%d, %d, %d, %d)\n", atom[0], atom[1], atom[2], atom[3]);
    rw.linear(5);
}