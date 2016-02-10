
#include <math.h>
#include <stdio.h>
#include <windows.h>


int main(int argc, char **argv)
{
	// STRING ECHO
	//
	// Sample usage:
	//   strecho repeat=4,str=pleaseechome

	char *str = (char *)malloc(100);
	int repeat = 0;

	char *line = GetCommandLineA();

	while (*line != ' ')
		line++;
	line++;

	if (strncmp(line, "repeat=", 7) == 0)
	{
		line += 7;
		repeat = atoi(line);
		line += (int)ceil(log10((double)repeat)) + 1;
	}

	if (strncmp(line, "str=", 4) == 0)
	{
		line += 4;
		str = strtok(line, " ");
	}

	for (int i = 0; i < repeat; i++)
		printf("%s\n", str);

	line += strlen(str);
	for (; line >= GetCommandLineA(); line--)
		*line = '\x0';

	free(str);

	return -14;
}
