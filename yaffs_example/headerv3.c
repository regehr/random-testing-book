#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <limits.h>
#include <dirent.h>
#include "yaffsfs.h"

#define REFPATH "/dev/shm"

int simulate_power_failure;
int random_seed;

#define BUF_SIZE 2048*3
#define MAX_HANDLES 10000

int h[MAX_HANDLES];
int fd[MAX_HANDLES];

#define NUM_BUFFERS 4
char rw[NUM_BUFFERS][BUF_SIZE];
char rwRef[NUM_BUFFERS][BUF_SIZE];
int s = 0;

int last_yaffs_return = 0;
int last_yaffs_error = 0;

int last_ref_return = 0;
int last_ref_error = 0;

void cleanup_ref(const char* path) {
  char newPath[PATH_MAX];
  DIR* d = opendir(path);
  if (d == 0)
    return;
  struct dirent* e;
  while (e = readdir(d)) {
    if ((e->d_type == DT_DIR) && (strncmp(e->d_name, ".", PATH_MAX) != 0) &&
	(strncmp(e->d_name, "..", PATH_MAX) != 0)) {
      strncpy(newPath, path, PATH_MAX);
      strncat(newPath, "/", PATH_MAX);
      strncat(newPath, e->d_name, PATH_MAX);
      cleanup_ref(newPath);
      rmdir(newPath);
    } else if (e->d_type == DT_REG) {
      strncpy(newPath, path, PATH_MAX);
      strncat(newPath, "/", PATH_MAX);
      strncat(newPath, e->d_name, PATH_MAX);
      unlink(newPath);
    }
  }
}

int check_buffers() {
#ifdef NO_BUFFER_CHECK
  return 0;
#endif
  int i, j;
  for (i = 0; i < NUM_BUFFERS; i++) {
    for (j = 0; j  < BUF_SIZE; j++) {
      if (rw[i][j] != rwRef[i][j]) {
#ifdef FAIL_VERBOSE
	printf("MISMATCH: Buffer contents differ at buffer %d, location %d:\n", i, j);
	printf("          %d for yaffs vs. %d for ref\n", rw[i][j], rwRef[i][j]); 
#endif
	return  1;
      }
    }
  }
  return 0;
}

void dump_returns() {
  printf("  RETURN VALUES:  yaffs = %d\n", last_yaffs_return);
  printf("                  ref =   %d\n", last_ref_return);
  printf("  ERROR VALUES:   yaffs = %s (%d)\n", 
	 yaffs_error_to_str(last_yaffs_error), last_yaffs_error);
  printf("                  ref =   %s (%d)\n",
	 yaffs_error_to_str(last_ref_error), last_ref_error);

}

int check_return(const char* msg) {
#ifdef NO_RETURN_CHECK
  return 0;
#endif
  int fail_yaffs = (last_yaffs_return < 0);
  int fail_ref = (last_ref_return < 0);

  if (fail_yaffs != fail_ref) {
#ifdef FAIL_VERBOSE
    printf("RETURN SIGN MISMATCH\n");
    dump_returns();
#endif
    return 1;
  }

#ifdef NO_VALUE_CHECK
  return 0;
#endif
  
  if ((last_yaffs_return != last_ref_return) && (strstr(msg, "fd[") == 0)) {
#ifdef FAIL_VERBOSE
    printf("RETURN VALUE MISMATCH\n");
    dump_returns();
#endif
    return 1;
  }

  return 0;
}

int check_error() {
#ifdef NO_ERROR_CHECK
  return 0;
#endif
  int fail_yaffs = (last_yaffs_return < 0);
  int fail_ref = (last_ref_return < 0);

  if (!fail_yaffs || !fail_ref)
    return 0;

  if (last_yaffs_error != last_ref_error) {
#ifdef FAIL_VERBOSE
    printf("ERROR MISMATCH\n");
    dump_returns();
#endif
    return 1;
  }

  return 0;
}

void fail() {
#ifdef FAIL_VERBOSE
  printf("TEST FAILED\n");
#endif
  exit(255);
}

int test(const int val, const char* msg) {
  last_yaffs_return = val;
  last_yaffs_error = yaffs_get_error();
#ifdef VERBOSE
  printf("%d: %s = %d ", ++s, msg, val);
  if (val == -1) {
    printf(" error: %s(%d)", yaffs_error_to_str(last_yaffs_error), last_yaffs_error);
  }
  printf ("\n");
#endif
  return val;
}

int ref(const int val, const char* msg) {
  int failed = 0;
  last_ref_return = val;
  last_ref_error = -errno;

#ifdef REF_VERBOSE
  printf("%d: %s = %d ", s, msg, val);
  if (val == -1) {
    printf(" error: %s(%d)", yaffs_error_to_str(last_ref_error), last_ref_error);
  }
  printf ("\n");
#endif

  failed = check_buffers() || failed;

  failed = check_return(msg) || failed;

  failed = check_error() || failed;

  if (failed) {
    fail();
  }

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
  for (i = 0; i < MAX_HANDLES; i++) {
    h[i] = -1;
    fd[i] = -1;
  }
  cleanup_ref(REFPATH);
  assert(test(yaffs_start_up(), "yaffs_start_up()") == 0);
  assert(test(yaffs_mount("/yaffs2"), "yaffs_mount(\"/yaffs2\")") == 0);

