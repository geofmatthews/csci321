
/**
 *  This class is a timer that uses the QueryPerformanceCounter to 
 *  compute high resolution elapsed time. getElapsedTimeInSeconds()
 *  returns a double that indicated the amount of time elapsed since 
 *  last reset(). 
 *	Created by Syrus Mesdaghi, SyrusM@hotmail.com
 */

/**
 *	Author: Syrus Mesdaghi, SyrusM@hotmail.com
 */

#ifndef HIGH_RESOLUTION_TIMER_H
#define HIGH_RESOLUTION_TIMER_H

#include <windows.h>

class HighResolutionTimer  
{
public:
	
	HighResolutionTimer();
	virtual ~HighResolutionTimer();
	
	// returns a high resolution elapsed time 
	double getElapsedTimeInSeconds();	

	//resets the timer
	void reset();	


private:

	LARGE_INTEGER	counterStart,
					counterEnd;


	unsigned long frequency;

	double	elapsedTime,
			frequencyInverse;
};

#endif
