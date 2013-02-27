#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include "yaffsfs.h"

#define REFPATH "/dev/shm"

int simulate_power_failure;
int random_seed;

#define BUF_SIZE 2048*3
#define MAX_HANDLES 1000

int h[MAX_HANDLES];
int fd[MAX_HANDLES];

#define NUM_BUFFERS 4
char rw[NUM_BUFFERS][BUF_SIZE];
char rwRef[NUM_BUFFERS][BUF_SIZE];
int s = 0;

int last_yaffs_return = 0;
int last_yaffs_error = 0;

int last_errno = 0;

void fail() {
  printf("TEST FAILED\n");
  exit(255);
}

int test(int val, char* msg) {
  last_yaffs_return = val;
  last_yaffs_error = yaffs_get_error();
  if (VERBOSE) {
    printf("%d: %s = %d ", s++, msg, val);
    if (val == -1) {
      printf(" error: %s(%d)", yaffs_error_to_str(last_yaffs_error), last_yaffs_error);
    }
    printf ("\n");
  }
  return val;
}

int ref(int val, char* msg) {
  int failed = 0;
  int terminate = 0;
  last_errno = -errno;
  if (val != last_yaffs_return) {
    if (((val < 0) && (last_yaffs_return > 0)) ||
	((val > 0) && (last_yaffs_return < 0))) {
      failed = 1;
      terminate = 1;
    } else{
      if (strstr("h[", msg) == 0) {
	failed = 1;
	terminate = 1;
      }
    }
  }
  if ((val == -1) && (last_yaffs_return == -1) && (last_yaffs_error != last_errno)) {
    failed = 1;
  }
  if (failed) {
    if (VERBOSE) {
      printf("DIFFERENTIAL MISMATCH\n");
      printf("  RETURN VALUES:  yaffs = %d\n", last_yaffs_return);
      printf("                  ref =   %d\n", val);
      printf("  ERROR VALUES:   yaffs = %s (%d)\n", 
	     yaffs_error_to_str(last_yaffs_error), last_yaffs_error);
      printf("                  ref =   %s (%d)\n",
	     yaffs_error_to_str(last_errno), last_errno);
    }
  }
  if (terminate)
    fail();
  return val;
}

int main () {
  int i, j;
  for (i = 0; i < NUM_BUFFERS; i++) {
    for (j = 0; j < BUF_SIZE; j++) {
      rw[i][j] = i;
      rwRef[i][j] = i;
    }
  }
  int r;
  r = test(yaffs_start_up(), "yaffs_start_up()");
  assert (r == 0);
  r = test(yaffs_mount("/yaffs2"), "yaffs_mount(\"/yaffs2\")");
  assert (r == 0);

