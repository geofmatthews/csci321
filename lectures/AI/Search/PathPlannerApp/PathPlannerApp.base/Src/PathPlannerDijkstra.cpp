// PathPlannerDijkstra.cpp: implementation of the PathPlannerDijkstra class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"

#include "PathPlannerApp.h"
#include "PathPlannerDijkstra.h"
#include "PlannerSettingsDialog.h"

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

PathPlannerDijkstra::PathPlannerDijkstra()
{
	cout << "PathPlannerDijkstra::PathPlannerDijkstra" <<endl;

	ix = iy = gx = gy = 0;
	current		= NULL;
	foundGoal	= false;
	isDone		= false;
	
	diagonalPenalty = false;
}

PathPlannerDijkstra::~PathPlannerDijkstra()
{
	cout << "PathPlannerDijkstra::~PathPlannerDijkstra" <<endl;
	CleanUp();
}



void PathPlannerDijkstra::PlanPath(int _ix, int _iy, int _gx, int _gy)
{
	cout << "PathPlannerDijkstra::PlanPath" <<endl;

	ix = _ix;
	iy = _iy;
	gx = _gx;
	gy = _gy;

	current		= NULL;
	foundGoal	= false;
	isDone		= false;

	
	//TODO: insert your code here
}

void PathPlannerDijkstra::Run()
{
	//cout << "PathPlannerDijkstra::Run" <<endl;

	DWORD startTime = GetTickCount();


	while (!open.empty()){

		//TODO: insert your code here

		//After doing one step of the planning, see if we have run over our allowed timeslice
		if ((int)(GetTickCount() - startTime) > CPathPlannerApp::instance->timeSlice)
			return;

	}


	isDone = true;

}


bool PathPlannerDijkstra::IsDone()
{
	//cout << "PathPlannerDijkstra::isDone" <<endl;
	return isDone;
}

void PathPlannerDijkstra::Draw(CDC *dc)
{
	//cout << "PathPlannerDijkstra::Draw" <<endl;

	//TODO: insert your code here
}

void PathPlannerDijkstra::Settings()
{
	cout << "PathPlannerDijkstra::Settings()" << endl;

	CPlannerSettingsDialog dialog(NULL);

	dialog.m_diagonalPenalty		= diagonalPenalty;
	dialog.m_closedHashTableSize	= 0;


	if (dialog.DoModal() == IDOK){
		diagonalPenalty			= dialog.m_diagonalPenalty? true: false;
	}
}

void PathPlannerDijkstra::ShowInfo()
{
	cout << "PathPlannerDijkstra::ShowInfo" <<endl;

	
	float goalGiveCost = -1.0;
	if (!solution.empty())
		goalGiveCost = solution[0]->givenCost;	



	char buffer[512]; 
	memset(&buffer, 0, sizeof(buffer));

	sprintf(
		buffer, 	
		" elapsedTime: %g\n runCount: %d\n isDone: %d\n foundGoal: %d\n goalGiveCost: %g\n nodesConstructed: %d\n nodesDestructed: %d\n open.size: %d\n solution.size: %d\n heuristicWeight: %g\n closedHashTableSize: %d\n",		
		(double)CPathPlannerApp::instance->elapsedTime,
		CPathPlannerApp::instance->runCount,
		isDone,
		foundGoal,
		goalGiveCost,
		PlannerNode::nodesConstructed, 
		PlannerNode::nodesDestructed, 
		open.size(), 
		solution.size(),
		0.0,
		0
	);

	MessageBox(CPathPlannerApp::instance->m_hWnd, buffer, "Planner Information", MB_OK);
}


void PathPlannerDijkstra::CleanUp(){
	cout << "PathPlannerDijkstra::CleanUp" <<endl;

	//TODO: insert your code here
}

// inserts so the lowest priority is in the end. if lower is better for you, just use vec_back() to get it
void PathPlannerDijkstra::SmartInsert(vector<PlannerNode *> *vec, PlannerNode * node){
	// binarySearch: 
	// determines the index of the search key, if it is contained in the list; otherwise, (-(insertion point) - 1). 
	// The insertion point is defined as the point at which the key would be inserted into the list: the index of the 
	// first element greater than the key, or list.size(), if all elements in the list are less than the specified key. Note that this guarantees that the return value will be >= 0 if and only if the key is found.

	int insertPosition = 0;

    int i = 0;
    for(int k = (*vec).size() - 1; i <= k;)
    {
        int l = (i + k) / 2;
        int i1 = node->compareDijkstra((*vec)[l]);
        
		if(i1 < 0){
            i = l + 1;
			insertPosition = -(i + 1);

		}else if(i1 > 0){
            k = l - 1;
			insertPosition = -(i + 1);
        
		}else{
            insertPosition = l;
			break;
		}
    }

	if (insertPosition < 0)
		insertPosition= -insertPosition - 1;
	
	(*vec).insert(&((*vec)[insertPosition]), node);
}