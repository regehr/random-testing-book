#ifndef __MY_STRING_H
#define __MY_STRING_H

#ifndef __USE_MY_STRING_FUNCTIONS
    #define mymemmove  memmove
    #define mymemcpy   memcpy
    #define mymemcmp   memcmp
    #define mymemset   memset
    #define mystrcmp   strcmp
    #define mystrncmp  strncmp
    #define mystrcpy   strcpy
    #define mystrncpy  strncpy
    #define mystrlen   strlen
    #define mystrnlen  strnlen
    #define mystrcat   strcat

#else

#include "stdlib.h"

void* mymemmove(void *s1, const void *s2, size_t n) 
 {
    /* note: these don't have to point to unsigned chars */
    char *p1 = s1;
    const char *p2 = s2;
    /* test for overlap that prevents an ascending copy */
    if (p2 < p1 && p1 < p2 + n) {
        /* do a descending copy */
        p2 += n;
        p1 += n;
        while (n-- != 0) 
            *--p1 = *--p2;
    } else 
        while (n-- != 0) 
            *p1++ = *p2++;
    return s1; 
 }
 
 void* mymemcpy(void * s1, const void * s2, size_t n)
 {
     char *dst = s1;
     const char *src = s2;
     /* Loop and copy.  */
     while (n-- != 0)
         *dst++ = *src++;
     return s1;
 }
 
int mymemcmp(const void *s1, const void *s2, size_t n)
{
    const unsigned char *us1 = (const unsigned char *) s1;
    const unsigned char *us2 = (const unsigned char *) s2;
    while (n-- != 0) {
        if (*us1 != *us2)
            return (*us1 < *us2) ? -1 : +1;
        us1++;
        us2++;
    }
    return 0;
}
 
void* mymemset(void *s, int c, size_t n)
{
    unsigned char *us = s;
    unsigned char uc = c;
    while (n-- != 0)
        *us++ = uc;
    return s;
}

int mystrcmp(const char *s1, const char *s2)
{
    unsigned char uc1, uc2;
    /* Move s1 and s2 to the first differing characters 
    in each string, or the ends of the strings if they
    are identical.  */
    while (*s1 != '\0' && *s1 == *s2) {
        s1++;
        s2++;
    }
    /* Compare the characters as unsigned char and
    return the difference.  */
    uc1 = (*(unsigned char *) s1);
    uc2 = (*(unsigned char *) s2);
    return ((uc1 < uc2) ? -1 : (uc1 > uc2));
}

int mystrncmp(const char *s1, const char *s2, size_t n)
{
    unsigned char uc1, uc2;
    /* Nothing to compare?  Return zero.  */
    if (n == 0)
        return 0;
    /* Loop, comparing bytes.  */
    while (n-- > 0 && *s1 == *s2) {
        /* If we've run out of bytes or hit a null, return zero
        since we already know *s1 == *s2.  */
        if (n == 0 || *s1 == '\0')
            return 0;
        s1++;
        s2++;
    }
    uc1 = (*(unsigned char *) s1);
    uc2 = (*(unsigned char *) s2);
    return ((uc1 < uc2) ? -1 : (uc1 > uc2));
}

char* mystrcpy(char * s1, const char * s2)
{
    char *dst = s1;
    const char *src = s2;
    /* Do the copying in a loop.  */
    while ((*dst++ = *src++) != '\0')
        ; /* The body of this loop is left empty. */
    /* Return the destination string.  */
    return s1;
}

char* mystrncpy(char * s1, const char * s2, size_t n)
 {
     char *dst = s1;
     const char *src = s2;
     /* Copy bytes, one at a time.  */
     while (n > 0) {
         n--;
         if ((*dst++ = *src++) == '\0') {
             /* If we get here, we found a null character at the end
                of s2, so use memset to put null bytes at the end of
                s1.  */
             mymemset(dst, '\0', n);
             break;
         }
     }
     return s1;
 }
 
size_t mystrlen(const char *s)
{
    const char *p = s;
    /* Loop over the data in s.  */
    while (*p != '\0')
        p++;
    return (size_t)(p - s);
}
 
size_t mystrnlen(const char *s, size_t max) {
    const char *p = s;
    for(; *p && max--; ++p);
    return(p - s);
}

char* mystrcat(char * s1, const char * s2)
 {
     char *s = s1;
     /* Move s so that it points to the end of s1.  */
     while (*s != '\0')
         s++;
     /* Copy the contents of s2 into the space at the end of s1.  */
     mystrcpy(s, s2);
     return s1;
 }
 
 char* mystrncat(char * s1, const char * s2, size_t n)
 {
     char *s = s1;
     /* Loop over the data in s1.  */
     while (*s != '\0')
         s++;
     /* s now points to s1's trailing null character, now copy
        up to n bytes from s1 into s stopping if a null character
        is encountered in s2.
        It is not safe to use strncpy here since it copies EXACTLY n
        characters, NULL padding if necessary.  */
     while (n != 0 && (*s = *s2++) != '\0') {
         n--;
         s++;
     }
     if (*s != '\0')
         *s = '\0';
     return s1;
 }
 
#endif
#endif
