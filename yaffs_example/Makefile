YAFFS_FLAGS = -DCONFIG_YAFFS_DIRECT -DCONFIG_YAFFS_YAFFS2 -DCONFIG_YAFFS_PROVIDE_DEFS -DCONFIG_YAFFSFS_PROVIDE_VALUES -I inc -I yaffs2

CC=gcc
CFLAGS = -g -coverage -O2

#CC=clang
#CFLAGS = -fsanitize=undefined -g -O2 -coverage

all: testv1 testv2 testv3

yaffs2.o: yaffs2.c
	$(CC) yaffs2.c -c $(YAFFS_FLAGS) $(CFLAGS)

testv1.c:
	python testgenv1.py testv1.c 500

testv1: testgenv1.py yaffs2.o headerv1.c testv1.c
	$(CC) -o testv1 testv1.c yaffs2.o $(YAFFS_FLAGS) $(CFLAGS) -DVERBOSE=1

testv2.c:
	python testgenv2.py testv2.c 500

testv2: testgenv2.py yaffs2.o headerv2.c testv2.c
	$(CC) -o testv2 testv2.c yaffs2.o $(YAFFS_FLAGS) $(CFLAGS) -DVERBOSE=1

testv3.c:
	python testgenv3.py testv3.c 500 --ref

testv3: testgenv3.py yaffs2.o headerv3.c testv3.c
	$(CC) -o testv3 testv3.c yaffs2.o $(YAFFS_FLAGS) $(CFLAGS) -DVERBOSE=1

clean:
	rm -rf *.o *.gcda *.gcno testv1.c testv2.c testv3.c testv1 testv2 testv3
