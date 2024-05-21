#include<iostream>
#include<fstream>
#include<stdio.h>
#include <unistd.h>

using namespace std;


int main(){
    fstream file;
    int a = 0 ;
    file.open("/home/ivan/Pictures/Screenshots/Screenshot from 2024-04-18 17-50-22.png", ios::in | ios::binary);
        
        if(file.is_open()){
        cout<<"[LOG] : File is ready to Transmit.\n";
        }
    cout << a;
}