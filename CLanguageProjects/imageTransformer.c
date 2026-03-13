#include <stdio.h>
#include <stdlib.h>

struct IntArray {
    int *arr;
    int len;
    int cap;
};

void append(struct IntArray *p, int v) {
    if (p->cap == p->len) {
        int newCap = (p->cap == 0) ? 4 : p->cap * 2;
        int *newArr = malloc(sizeof(int) * newCap);
        for (int i = 0; i < p->len; ++i) {
            newArr[i] = p->arr[i];
        }
        free(p->arr);
        p->arr = newArr;
        p->cap = newCap;
    }
    p->arr[p->len++] = v;
}

void applySepia(struct IntArray *ia, unsigned int width, unsigned int height) {
    for (unsigned int i = 0; i < height; i++) {
        for (unsigned int j = 0; j < width; j++) {
            unsigned int idx = (i * width + j) * 3;
            int r = ia->arr[idx];
            int g = ia->arr[idx + 1];
            int b = ia->arr[idx + 2];
            
            int newR = (int)(r * 0.393 + g * 0.769 + b * 0.189);
            int newG = (int)(r * 0.349 + g * 0.686 + b * 0.168);
            int newB = (int)(r * 0.272 + g * 0.534 + b * 0.131);
            
            if (newR > 255) newR = 255;
            if (newG > 255) newG = 255;
            if (newB > 255) newB = 255;
            
            ia->arr[idx] = newR;
            ia->arr[idx + 1] = newG;
            ia->arr[idx + 2] = newB;
        }
    }
}

void flipImage(struct IntArray *ia, unsigned int width, unsigned int height) {
    for (unsigned int i = 0; i < height; ++i) {
        for (unsigned int j = 0; j < width / 2; ++j) {
            unsigned int leftIdx = (i * width * 3) + (j * 3);
            unsigned int rightIdx = (i * width * 3) + ((width - 1 - j) * 3);
            for (int k = 0; k < 3; k++) {
                int temp = ia->arr[leftIdx + k];
                ia->arr[leftIdx + k] = ia->arr[rightIdx + k];
                ia->arr[rightIdx + k] = temp;
            }
        }
    }
}

int manualStrcmp(const char *s1, const char *s2) {
    while (*s1 && (*s1 == *s2)) {
        s1++;
        s2++;
    }
    return *(unsigned char *)s1 - *(unsigned char *)s2;
}

int main(int argc, char *argv[]) {
    char line[3];
    unsigned int width, height, max_val;
    int flip = 0;
    int sepia = 0;

    for (int i = 1; i < argc; i++) {
        if (manualStrcmp(argv[i], "-f") == 0) {
            flip = 1;
        } else if (manualStrcmp(argv[i], "-s") == 0) {
            sepia = 1;
        }
    }

    if (scanf("%2s", line) != 1) return 1;
    if (line[0] != 'P' || line[1] != '3') return 1;
    
    if (scanf("%u %u", &width, &height) != 2) return 1;
    if (scanf("%u", &max_val) != 1) return 1;

    struct IntArray ia;
    ia.cap = 4;
    ia.arr = malloc(sizeof(int) * ia.cap);
    ia.len = 0;

    unsigned int total_pixels = width * height * 3;
    for (unsigned int i = 0; i < total_pixels; ++i) {
        int val;
        if (scanf("%d", &val) == 1) {
            append(&ia, val);
        }
    }
    
    if (sepia) {
        applySepia(&ia, width, height);
    }
    
    if (flip) {
        flipImage(&ia, width, height);
    }

    printf("P3\n");
    printf("%u %u\n", width, height);
    printf("%u\n", max_val);

    for (unsigned int i = 0; i < height; i++) {
        for (unsigned int j = 0; j < width; j++) {
            unsigned int idx = (i * width + j) * 3;
            printf("%d %d %d", ia.arr[idx], ia.arr[idx + 1], ia.arr[idx + 2]);
            if (j < width - 1) {
                printf(" ");
            }
        }
        printf(" \n");
    }

    free(ia.arr);
    return 0;
}