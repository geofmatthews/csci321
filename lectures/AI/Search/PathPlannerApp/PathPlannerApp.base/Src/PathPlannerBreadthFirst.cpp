// PathPlannerBreadthFirst.cpp: implementation of the PathPlannerBreadthFirst class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"

#include "PathPlannerApp.h"
#include "PathPlannerBreadthFirst.h"

#include <iostream>
using namespace std;

#ifdef _DEBUG
#undef THIS_FILE
static char THIS_FILE[]=__FILE__;
#define new DEBUG_NEW
#endif

//////////////////////////////////////////////////////////////////////
// Construction/Destruction
//////////////////////////////////////////////////////////////////////

PathPlannerBreadthFirst::PathPlannerBreadthFirst()
{
	cout << "PathPlannerBreadthFirst::PathPlannerBreadthFirst" <<endl;
	
	ix = iy = gx = gy = 0;
	current = NULL;
	foundGoal = false;
	isDone = false;
}

PathPlannerBreadthFirst::~PathPlannerBreadthFirst()
{
	cout << "PathPlannerBreadthFirst::~PathPlannerBreadthFirst" <<endl;
	CleanUp();
}



void PathPlannerBreadthFirst::PlanPath(int _ix, int _iy, int _gx, int _gy)
{
	cout << "PathPlannerBreadthFirst::PlanPath" <<endl;

	ix = _ix;
	iy = _iy;
	gx = _gx;
	gy = _gy;

	current		= NULL;
	foundGoal	= false;
	isDone		= false;

	//TODO: insert your code here
}

void PathPlannerBreadthFirst::Run()
{
	//cout << "PathPlannerBreadthFirst::Run" <<endl;

	DWORD startTime = GetTickCount();

	while (!open.empty()){
			
		//TODO: insert your code here

		//After doing one step of the planning, see if we have run over our allowed timeslice
		if ((int)(GetTickCount() - startTime) > CPathPlannerApp::instance->timeSlice)
			return;
	}


	isDone = true;

}


bool PathPlannerBreadthFirst::IsDone()
{
	//cout << "PathPlannerBreadthFirst::isDone" <<endl;
	return isDone;
}

void PathPlannerBreadthFirst::Draw(CDC *dc)
{
	//cout << "PathPlannerBreadthFirst::Draw" <<endl;

	//TODO: insert your code here
}


void PathPlannerBreadthFirst::ShowInfo()
{
	cout << "PathPlannerBreadthFirst::ShowInfo" <<endl;

	
	float goalGiveCost = -1.0;
	if (!solution.empty())
		goalGiveCost = solution[0]->givenCost;	



	char buffer[512]; 
	memset(&buffer, 0, sizeof(buffer));

	sprintf(
		buffer, 	
		"elapsedTime: %g\n runCount: %d\n isDone: %d\n foundGoal: %d\n goalGiveCost: %g\n nodesConstructed: %d\n nodesDestructed: %d\n open.size: %d\n closed.size: %d\n solution.size: %d\n",		
		(double)CPathPlannerApp::instance->elapsedTime,
		CPathPlannerApp::instance->runCount,
		isDone,
		foundGoal,
		goalGiveCost,
		PlannerNode::nodesConstructed, 
		PlannerNode::nodesDestructed, 
		open.size(), 
		closed.size(),
		solution.size()
	);
	
	MessageBox(CPathPlannerApp::instance->m_hWnd, buffer, "Planner Information", MB_OK);
}


void PathPlannerBreadthFirst::CleanUp(){
	cout << "PathPlannerBreadthFirst::CleanUp" <<endl;

	//TODO: insert your code here
}

