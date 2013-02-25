YAFFS_FLAGS = -DCONFIG_YAFFS_DIRECT -DCONFIG_YAFFS_YAFFS2 -DCONFIG_YAFFS_PROVIDE_DEFS -DCONFIG_YAFFSFS_PROVIDE_VALUES -I inc -I yaffs2
CFLAGS = -g -coverage -O2

yaffs2.o: yaffs2.c
	gcc yaffs2.c -c $(YAFFS_FLAGS) $(CFLAGS)

testv1: testgenv1.py yaffs2.o
	python testgenv1.py testv1.c 50
	gcc -o testv1 testv1.c yaffs2.o $(YAFFS_FLAGS) $(CFLAGS) -DVERBOSE=1
	./testv1

clean:
	rm -rf *.o *.gcda *.gcno
