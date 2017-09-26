/**
 *	Author: Syrus Mesdaghi, SyrusM@hotmail.com
 */

// PathPlannerBreadthFirst.h: interface for the PathPlannerBreadthFirst class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(PATHPLANNERBREADTHFIRST_H)
#define PATHPLANNERBREADTHFIRST_H

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include "PathPlannerBase.h"
#include "PlannerNode.h"

// STL
#include <vector>
#include <list>
using namespace std;



class PathPlannerBreadthFirst : public PathPlannerBase  
{
	
public:
	
	PlannerNode* current;


	list<PlannerNode *>	closed;
	list<PlannerNode *>	open;
	vector<PlannerNode *>	solution;

	list<PlannerNode *>::iterator iterator;

	int ix, iy, gx, gy;
	bool	foundGoal,
			isDone;

public:
	PathPlannerBreadthFirst();
	virtual ~PathPlannerBreadthFirst();

	void Draw(CDC *dc);
	void PlanPath(int _ix, int _iy, int _gx, int _gy);
	void Run();
	bool IsDone();
	void ShowInfo();
	void CleanUp();
	
};

#endif // !defined(PATHPLANNERBREADTHFIRST_H)
