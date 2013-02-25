#include <stdlib.h>
#include <stdio.h>
#include "yaffsfs.h"

int simulate_power_failure;
int random_seed;

#define FILE_SIZE 10000

char rwbuf[FILE_SIZE];
int s = 0;

int callFunc(int val, char* msg) {
  if (VERBOSE) 
    printf ("%d: %s = %d\n", s++, msg, val);
  return val;
}

int main () {
  int r;
  r = callFunc(yaffs_start_up(), "yaffs_start_up()");
  assert (r == 0);
  r = callFunc(yaffs_mount("/yaffs2"), "yaffs_mount(\"/yaffs2\")");
  assert (r == 0);

