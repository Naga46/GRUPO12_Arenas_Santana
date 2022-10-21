#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <wiringSerial.h>
#include <iostream>
#include <fstream>

int main (){
    int fd ;
    int i=0;
    int contador=0;
    int j=0;

    if ((fd = serialOpen ("/dev/ttyACM3", 115200)) < 0){
        fprintf (stderr, "Unable to open serial device: %s\n", strerror (errno)) ;
        return 1 ;
    }
    do{
    ofstream file;
    file.open("contador");
    file << fd;
    if (j==32000){
        contador=contador+1;
        file.close();
    }
    j=j+1;

    }while (i<2);
}
