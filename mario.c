#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while(height <= 0 || height > 8);
    for(int i = 0; i < height; i++)
    {
        for(int a = 0; a < height; a++)
        {
            if(a < height - i - 1){
                printf(" ");
            }else{
                printf("#");
            }

        }
        printf("\n");
    }
}