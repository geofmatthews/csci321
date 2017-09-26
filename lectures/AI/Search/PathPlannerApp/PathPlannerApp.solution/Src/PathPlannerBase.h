/**
 *	The   Path   Planner  Application  is  made to allow 
 *  convenient  creation,  demonstration,  and  analysis 
 *  of  different  path planning  algorithms.  Different 
 *  algorithms  can  be  implemented  as  separate class 
 *  files. for  information on each  implementation  and 
 *  its author, see the header file corresponding to the 
 *  specific algorithm.
 *
 *	Created by Syrus Mesdaghi, SyrusM@hotmail.com
 */


/**
 * This class is the interface that allows the Application to control a path planner.
 * See the description for each function
 */

 // NOTE: it should not have any member variables ... and have only vitual functions    


// PathPlannerBase.h: interface for the PathPlannerBase class.
//
//////////////////////////////////////////////////////////////////////


#if !defined(PATHPLANNERBASE_H)
#define PATHPLANNERBASE_H

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include <afxwin.h>


class PathPlannerBase
{

public:
	
	PathPlannerBase();	
	virtual ~PathPlannerBase();

	// the framework will call this function to ask a planner 
	// find a path (solution) from initial coordinate to the goal coordinate.
	virtual	void PlanPath(int ix, int iy, int gx, int gy);

	// this function where the planning happens. it should not take too long or else the application will hault.
	// a planner should be designed to return after a rather small time slice. The application will recall the run
	// function untill the IsDone() function (see below) returns true
	virtual	void Run();

	// allows the framework to see if the planner is done so it does not recall the run function
	virtual bool IsDone();

	// this function is called by the framework to allow the planner do any drawing.
	// for example, an A* planner should draw the start, gloal, closed, open, and path nodes. 
	virtual	void Draw(CDC *dc);

	// should pop up a dialog and get the settings specific to this algorithm. Note that this is different than the 
	// application settings
	virtual void Settings();

	// should pop up a dialog showing the information about the planner and its author
	virtual void ShowInfo();

	// should do any clean up 
	// for example an A* planner should delete the nodes in open and closed
	virtual void CleanUp();

};

#endif // !defined(PATHPLANNERBASE_H)
