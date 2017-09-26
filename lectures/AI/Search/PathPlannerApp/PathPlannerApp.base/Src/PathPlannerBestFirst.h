/**
 *	Author: Syrus Mesdaghi, SyrusM@hotmail.com
 */


// PathPlannerBestFirst.h: interface for the PathPlannerBestFirst class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(PATHPLANNERBESTFIRST_H)
#define PATHPLANNERBESTFIRST_H

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include "PathPlannerBase.h"
#include "PlannerNode.h"

// STL
#include <vector>
#include <list>
using namespace std;


// computes the hash code of a pair of coordinates
// WARNING: this methode will fail if the x or y values are greater than 0xFFFF or 65,535
// TODO: write the hash code macro
#define COMPUTE_HASH_CODE(x, y)	(0xFFFF0000 & (x << 16) | (0xFFFF & y))



class PathPlannerBestFirst : public PathPlannerBase  
{
	
public:
	
	PlannerNode* current;


	list<PlannerNode *>	closed;				
	vector<PlannerNode *>	open;				
	vector<PlannerNode *>	solution;

	list<PlannerNode *>::iterator iterator;

	int ix, iy, gx, gy;
	bool	foundGoal,
			isDone;

public:
	PathPlannerBestFirst();
	virtual ~PathPlannerBestFirst();

	void Draw(CDC *dc);
	void PlanPath(int ix, int iy, int gx, int gy);
	void Run();
	bool IsDone();
	void Settings();
	void ShowInfo();
	void CleanUp();


	
	// inserts the node into the provided vector. it searches the vector to find the "correct" insertion point.
	// it assumes that vec is already sorted. the PlannerNode class MUST provide a compare() function that allows SmartInsert 
	// determine wether a node is <, >, or == to another
	void SmartInsert(vector<PlannerNode *> *vec, PlannerNode * node);

};

#endif // !defined(PATHPLANNERBESTFIRST_H)
