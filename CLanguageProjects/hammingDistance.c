#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 4) {
        return 1;
    }

    unsigned long number1 = strtoul(argv[1], NULL, 10);
    unsigned long number2 = strtoul(argv[2], NULL, 10);
    unsigned long base = strtoul(argv[3], NULL, 10);

    unsigned long hamDistance = 0;

    while (number1 > 0 && number2 > 0) {
        if ((number1 % base) != (number2 % base)) {
            hamDistance++;
        }
        number1 /= base;
        number2 /= base;
    }

    while (number1 > 0) {
        hamDistance++;
        number1 /= base;
    }
    while (number2 > 0) {
        hamDistance++;
        number2 /= base;
    }

    printf("%lu\n", hamDistance);

    return 0;
}