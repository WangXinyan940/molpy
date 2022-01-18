
#include "randomWalk.h"

#define PI 3.14159265

// RandomWalk::RandomWalk() : MAX_X(100), MAX_Y(100), MAX_Z(100) {}
RandomWalk::RandomWalk(int MAX_X, int MAX_Y, int MAX_Z) : MAX_X(MAX_X), MAX_Y(MAX_Y), MAX_Z(MAX_Z)
{
  create(site, MAX_X, MAX_Y, MAX_Z, 4);
  create(loc_dens, MAX_X, MAX_Y, MAX_Z, 4);
  sqrt_2_2 = sqrt(2) / 2.0;
}

vec4 RandomWalk::findStart()
{
  // [0, n) := rand()%n
  // [a, b) := (rand() % (b-a)) + a
  // [a, b] := (rand() % (b-a+1)) + a
  // (a, b] := (rand() % (b-a)) + a + 1
  // to sum up: a + rand() % n, where a is start and n in the range

  // for float, a + int(b) * rand() / (RAND_MAX + 1)
  // (0, 1) := rand() / double(RAND_MAX)

  int i, j, k, l;
  do
  {
    i = (rand() % (MAX_X));
    j = (rand() % (MAX_Y));
    k = (rand() % (MAX_Z));
    l = (rand() % 4);
  } while (site[i][j][k][l] != 0);
  site[i][j][k][l] = 1;
  vec4 start{{i, j, k, l}};
  atom_list.push_back(start);
  return start;
}

std::array<float, 3> RandomWalk::mapSiteToCoord(int l)
{
  std::array<float, 3> a;
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

void RandomWalk::linear(int lchain)
{
  vec4 start = findStart();
  vec4 end = walkOnce(start, lchain);
}

vec4 RandomWalk::walkOnce(vec4 start, int length)
{
  vec4 nextStep;
  vec4 currentStep = start;
  for (int v = 1; v < length; v++)
  {
    // looking for neighbor
    findNeighbors(currentStep, v, length);
    chooseNextStep(currentStep, v, length);
  }
  return currentStep;
}

void RandomWalk::findNeighbors(vec4 center, int n_in_chain, int length)
{
  int v = n_in_chain;
  int i, j, k, l;
  int ii, jj, kk, mm;
  int nn_count, nn;
  int dx[3], dy[3], dz[3];
  float angle = 0, d_prod;
  std::array<float, 3> a, aa;
  vec4 atom;

  i = center[0];
  j = center[1];
  k = center[2];
  l = center[3];

  dx[1] = i;
  dy[1] = j;
  dz[1] = k;
  dx[2] = i + 1;
  dy[2] = j + 1;
  dz[2] = k + 1;
  dx[0] = i - 1;
  dy[0] = j - 1;
  dz[0] = k - 1;

  // wrap
  if (dx[2] == MAX_X)
    dx[2] = 0;
  if (dy[2] == MAX_Y)
    dy[2] = 0;
  if (dz[2] == MAX_Z)
    dz[2] = 0;
  if (dx[0] < 0)
    dx[0] = MAX_X - 1;
  if (dy[0] < 0)
    dy[0] = MAX_Y - 1;
  if (dz[0] < 0)
    dz[0] = MAX_Z - 1;

  a = mapSiteToCoord(l);

  for (ii = 0; ii < 3; ii++)
  {
    for (jj = 0; jj < 3; jj++)
    {
      for (kk = 0; kk < 3; kk++)
      {
        for (mm = 0; mm < 4; mm++)
        {
          aa = mapSiteToCoord(mm);
          aa[0] = aa[0] + ii - 1;
          aa[1] = aa[1] + jj - 1;
          aa[2] = aa[2] + kk - 1;
          va[0] = aa[0] - a[0];
          va[1] = aa[1] - a[1];
          va[2] = aa[2] - a[2];
          va_mag = sqrt(va[0] * va[0] + va[1] * va[1] + va[2] * va[2]);

          // check isOccupied
          if (site[dx[ii]][dy[jj]][dz[kk]][mm] == 0||(v==length-1&&site[dx[ii]][dy[jj]][dz[kk]][mm]==2))
          {
            if (va_mag <= sqrt_2_2 + 0.01)  // if va_mag == sqrt_2_2
            {
              loc_dens[dx[ii]][dy[jj]][dz[kk]][mm]++;
              st_ld[nn_count][0] = dx[ii];
              st_ld[nn_count][1] = dy[jj];
              st_ld[nn_count][2] = dz[kk];
              st_ld[nn_count][3] = mm;
              nn_count++; 

              if (v != 1)  // if not the first atom in the chain
              {
                d_prod = va[0] * vb[0] + va[1] * vb[1] + va[2] * vb[2];
                angle = acos(d_prod / (va_mag * vb_mag)) * 180.0 / PI;
              }
              if ((angle < -60.0 && angle > -150.0) || (angle > 60.0 && angle < 150.0) || v == 1)
              {
                neigh[nn][0] = dx[ii];
                neigh[nn][1] = dy[jj];
                neigh[nn][2] = dz[kk];
                neigh[nn][3] = mm;
                v_store[nn][0] = va[0];
                v_store[nn][1] = va[1];
                v_store[nn][2] = va[2];
                mag_store[nn] = va_mag;
                nn++;
              }

            }

            /*
            else if(va_mag<=1.01)
              {
                snd_dens[dx[ii]][dy[jj]][dz[kk]][mm]++;
                snd_ld[snd_count][0]=dx[ii];
                snd_ld[snd_count][1]=dy[jj];
                snd_ld[snd_count][2]=dz[kk];
                snd_ld[snd_count][3]=mm;
                snd_count++;
              }
*/

            if (va_mag < 0.707)
            {
              printf("creating atoms too close to each other\n");
              exit(1);
            }

          }
        }
      }
    }
  }
}

void RandomWalk::chooseNextStep(vec4 currentStep, int& n_in_chain, int length) {

                int total_dens;
                int prob_low,prob_high;
                int point;

                int i = currentStep[0];
                int j = currentStep[1];
                int k = currentStep[2];
                int m = currentStep[3];
        
                if(n_in_chain==0)
                {
                  if(reset==1)
                    {
                      printf("has already been reset and still can not find a neighbor\n");
                      // printf("chain %d atom %d \n",u,v);
                      exit(1);
                    } 
                  printf("there is not a free neighbor site and must reset\n");
                  reset=1;
                  site[i][j][k][m]=2;
                  atom = atom_list.back();
                  i = atom[0];
                  j = atom[1];
                  k = atom[2];
                  m = atom[3];

                  for(int ii=0;ii<12;ii++)
                    {
                      loc_dens[st_ld[ii][0]][st_ld[ii][1]][st_ld[ii][2]][st_ld[ii][3]]--;
                    }
/*
                  for(ii=0;ii<6;ii++)
                    {
                      snd_dens[snd_ld[ii][0]][snd_ld[ii][1]][snd_ld[ii][2]][snd_ld[ii][3]]--;
                    }
*/
                  vb[0]=vc[0];
                  vb[1]=vc[1];
                  vb[2]=vc[2];
                  n_in_chain=n_in_chain-2;
                }
              else
                {
                  total_dens=0;
                  for(int ii=0;ii<n_in_chain;ii++)
                    {
                      total_dens=total_dens+(12-loc_dens[st_ld[ii][0]][st_ld[ii][1]][st_ld[ii][2]][st_ld[ii][3]]);
/*
                      total_dens=total_dens+(6-snd_dens[st_ld[ii][0]][st_ld[ii][1]][st_ld[ii][2]][st_ld[ii][3]]);
*/
                    }
                  point=total_dens*((double)rand()/(double)RAND_MAX);
                  prob_low=0;
                  prob_high=(12-loc_dens[st_ld[0][0]][st_ld[0][1]][st_ld[0][2]][st_ld[0][3]]);
/*
                  prob_high=prob_high+(6-snd_dens[st_ld[0][0]][st_ld[0][1]][st_ld[0][2]][st_ld[0][3]]);
*/
                  printf("span %d prob_high %d prob_low %d point %d\n",prob_high-prob_low,prob_high,prob_low,point);
                  printf("0 %d 1 %d 2 %d 3 %d \n",st_ld[0][0],st_ld[0][1],st_ld[0][2],st_ld[0][3]);
                  printf("site %d\n",site[st_ld[0][0]][st_ld[0][1]][st_ld[0][2]][st_ld[0][3]]);
                  for(int ii=0;ii<n_in_chain;ii++)
                    {
                      if(point>=prob_low&&point<prob_high)
                        {
                          i=neigh[ii][0];
                          j=neigh[ii][1];
                          k=neigh[ii][2];
                          m=neigh[ii][3];
                          atom[0] = i;
                          atom[1] = j;
                          atom[2] = k;
                          atom[3] = m;
                          site[i][j][k][m]=1;
                          n_in_chain++;             

                      /*store the previous vector*/
                          vc[0]=vb[0];
                          vc[1]=vb[1];
                          vc[2]=vb[2];
                          vb[0]=-v_store[ii][0];
                          vb[1]=-v_store[ii][1];
                          vb[2]=-v_store[ii][2];
                          vb_mag=mag_store[ii];
                          ii=n_in_chain;
                          reset=0;
                        }
                      else
                        {
                          if(ii==n_in_chain-1)
                            {
                              if(reset==1)
                                {
                                   printf("there is not a free neighbor site and must reset\n");
                                   printf("has already been reset and still can not find a neighbor\n");
                                   // printf("chain %d atom %d \n",u,v);
                                   exit(1);
                                 } 
                               printf("resetting\n");           
                               reset=1;
                               site[i][j][k][m]=2;
                               atom = atom_list.back();
                  i = atom[0];
                  j = atom[1];
                  k = atom[2];
                  m = atom[3];
                               for(ii=0;ii<12;ii++)
                                 {
                                   loc_dens[st_ld[ii][0]][st_ld[ii][1]][st_ld[ii][2]][st_ld[ii][3]]--;
                                 }
/*
                               for(ii=0;ii<6;ii++)
                                 {
                                   snd_dens[snd_ld[ii][0]][snd_ld[ii][1]][snd_ld[ii][2]][snd_ld[ii][3]]--;
                                 }
*/
                               vb[0]=vc[0];
                               vb[1]=vc[1];
                               vb[2]=vc[2];
                               ii=n_in_chain;
                               n_in_chain=n_in_chain-2;
                            }
                          else
                            {
                              prob_low=prob_high;
                              prob_high=prob_high+(12-loc_dens[st_ld[ii+1][0]][st_ld[ii+1][1]][st_ld[ii+1][2]][st_ld[ii+1][3]]);
/*
                              prob_high=prob_high+(6-snd_dens[st_ld[ii+1][0]][st_ld[ii+1][1]][st_ld[ii+1][2]][st_ld[ii+1][3]]);
*/
                            }
                        }
                    }
                }
            }

int main()
{
  // // RandomWalk rw(10, 20, 30);
  // RandomWalk* rw = new RandomWalk(10, 20, 30);
  RandomWalk rw = RandomWalk();
  rw.linear(10);
}