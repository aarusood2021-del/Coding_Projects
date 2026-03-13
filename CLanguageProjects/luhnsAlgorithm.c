#include <stdio.h>

int main() {
    char x;
    int convertednumber;
    int sum = 0; 
    int counter = 0; 
    while (scanf("%c", &x) == 1){
        convertednumber = x - '0';
        if (convertednumber < 0 || convertednumber > 9) break;
        if (counter % 2 == 1){
            sum = sum + convertednumber;
        }
        else{
            if (2*convertednumber >= 10){
                sum = sum + ((2*convertednumber)-9);
            }
            else{
                sum = sum + (2*convertednumber);
            }
        }
        counter = counter + 1;
    }
    if (counter % 2 == 0){
        sum = sum - convertednumber;
        if ((sum*9) % 10 == convertednumber){
            printf("Valid\n");
        }
        else{
            printf("Invalid\n");
        }
    }
    else{
        if (2*convertednumber >= 10){
            sum = sum - ((2*convertednumber)-9);
            if ((sum*9) % 10 == convertednumber){
                printf("Valid\n");
            }
            else{
                printf("Invalid\n");
            } 
        }
        else {
            sum = sum - (2*convertednumber);
            if ((sum*9) % 10 == convertednumber){
                printf("Valid\n");
            }
            else{
                printf("Invalid\n");
            } 
        }      
    }
    return 0;
}