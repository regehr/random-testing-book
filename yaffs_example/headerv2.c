#include <stdlib.h>
#include <stdio.h>
#include "yaffsfs.h"

int simulate_power_failure;
int random_seed;

#define BUF_SIZE 10000
#define MAX_HANDLES 1000

int h[MAX_HANDLES];

#define NUM_BUFFERS 4
char rwBuf[NUM_BUFFERS][BUF_SIZE];
int s = 0;

int callFunc(int val, char* msg) {
  if (VERBOSE) 
    printf ("%d: %s = %d\n", s++, msg, val);
  return val;
}

int main () {
  int i, j;
  for (i = 0; i < NUM_BUFFERS; i++) {
    for (j = 0; j < BUF_SIZE; j++) {
      rwBuf[i][j] = i;
    }
  }
  int r;
  r = callFunc(yaffs_start_up(), "yaffs_start_up()");
  assert (r == 0);
  r = callFunc(yaffs_mount("/yaffs2"), "yaffs_mount(\"/yaffs2\")");
  assert (r == 0);

