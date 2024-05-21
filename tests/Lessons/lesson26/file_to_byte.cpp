#include <iostream>
#include <fstream>
#include <vector>
#include <bitset>


using namespace std;

int main() {

    ifstream file("C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\lesson26\\resurce_file\\last_love.mp3", ios::binary);
    
    if (!file.is_open()) {
        cerr << "Ошибка открытия файла1" << endl;
        return 1;
    }
    
    vector <unsigned char> fileBytes(istreambuf_iterator<char>(file), {});
    
    vector<int> vec;

    for (unsigned char byte : fileBytes) {
        bitset <8> bits(byte);
        vec.push_back(byte);
        cout << bits;
    }
    cout << endl;

    ofstream txt("C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\lesson26\\resurce_file\\1.mp3", ios::binary);

    //for (int num : vec) {
        //cout << num << " ";
   // } 

    if (txt.is_open())
    {
        for (int num : vec) {
            txt << num ;
        }   
        
    }

    txt.close(); 

//ofstream outputFile("C:\\Users\\Ivan\\Desktop\\lerning\\YADRO\\Adalm-Pluto-SDR\\tests\\Lessons\\lesson26\\2333.mp3", ios::binary);
   // for (unsigned char byte : vec) {
     //  outputFile << byte;
    //}
    
    //cout << "Содержимое файла успешно сконвертировано и сохранено в output.txt" << std::endl;
    
    return 0;
}
