
#include <string>
#include <sstream>
#include <iostream>
#include <stdlib.h>

using namespace std;

void Error()
{
	cout << "detected\n";
	exit(-14);
}

int main(int argc, char **argv)
{
	// STRING ECHO
	//
	// Sample usage:
	//   strecho repeat=4,str=pleaseechome

	// Get argument.
	if (argc != 2) {
		Error();
	}
	string argument(argv[1]);

	//
	size_t repeat_pos = argument.find("repeat=");
	if (repeat_pos == string::npos || repeat_pos != 0) {
		Error();
	} else {
		repeat_pos += 7;
	}
	size_t end_repeat_pos = argument.find(",str=");
	if (end_repeat_pos == string::npos) { Error(); }
	size_t repeat_length = end_repeat_pos - repeat_pos;
	if (end_repeat_pos < repeat_pos) { Error(); }

	string repeat_value_str(argument.substr(repeat_pos, repeat_length));
	if (repeat_value_str.size() == 0) { Error(); }
	istringstream repeat_value_buffer(repeat_value_str);
	int repeat_value;
	if (!(repeat_value_buffer >> repeat_value)) { Error(); }

	size_t str_pos = end_repeat_pos + 5;
	string str_value_str(argument.substr(str_pos));
	if (str_value_str.size() == 0) { Error(); }

	if (repeat_value <= 0) { Error(); }
	for (int i = 0; i < repeat_value; ++i)
	{
		cout << str_value_str << "\n";
	}

	return -14;
}
