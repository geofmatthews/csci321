

// Note: this function returns time in seconds as a double. to convert to, say, milliseconds multiply the returned value by 1000. 
// Note: 32 bit number takes about 9 min to rollOver (with freq of 3579545 (p4 1.8)), but a 64bit number it will take 2576688388288 seconds to rollOver ~ 81706 years :)


#include "HighResolutionTimer.h"


#include <iostream>
using namespace std;

HighResolutionTimer::HighResolutionTimer(){

	counterStart.QuadPart = 0;
	counterEnd.QuadPart = 0;

	elapsedTime = 0;
	frequencyInverse = 0;
	frequency = 0;


	QueryPerformanceFrequency((LARGE_INTEGER*)&frequency);
	
	if (frequency == 0){
		cout << "====> System does NOT support high-res performance counter <====" << endl;
	}else{			
		frequencyInverse = 1.0/frequency;
		cout << "System counter  frequency: " << frequency << "   frequencyInverse: " << frequencyInverse << endl;
		reset();
	}
}

HighResolutionTimer::~HighResolutionTimer()
{	
	cout << "HighResolutionTimer::~HighResolutionTimer()" << endl;
}


void HighResolutionTimer::reset(){
	QueryPerformanceCounter(&counterStart);
	elapsedTime = 0;
}


double HighResolutionTimer::getElapsedTimeInSeconds(){
	
	QueryPerformanceCounter(&counterEnd);

	elapsedTime	= ((counterEnd).QuadPart - (counterStart).QuadPart) * frequencyInverse;			

	return elapsedTime;
}	
