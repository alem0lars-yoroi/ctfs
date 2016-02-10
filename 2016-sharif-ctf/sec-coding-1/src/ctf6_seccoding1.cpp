
#include <vector>
#include <iostream>
#include <windows.h>

using namespace std;


int main()
{
	vector<char> str(MAX_PATH);
	
	cout << "Enter your name: ";
	cin >> str.data();

	cout << "Hello " << str.data() << " :)" << endl;

	return -14;
}
