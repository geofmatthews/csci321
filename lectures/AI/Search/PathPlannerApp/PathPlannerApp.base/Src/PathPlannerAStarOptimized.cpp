// PathPlannerAStarOptimized.cpp: implementation of the PathPlannerAStarOptimized class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"

#include "PathPlannerApp.h"
#include "PathPlannerAStarOptimized.h"
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

PathPlannerAStarOptimized::PathPlannerAStarOptimized()
{
	cout << "PathPlannerAStarOptimized::PathPlannerAStarOptimized" <<endl;

	ix = iy = gx = gy = 0;
	current		= NULL;
	foundGoal	= false;
	isDone		= false;	
	diagonalPenalty = false;
	heuristicWeight = 1;

	// some prime numbers that can be used for hash table size
	// 101, 151, 199, 307, 401, 499, 599, 797, 911, 997, 1999, 4001
	// NOTE:	when you turn in your project, it should be using hash table size of 
	//			199. When writing your hash table functions, you should try table sizes
	//          of 1 and 4001. 
	createdNodesHashTableSize = 199;

	createdNodesHashTable = new PlannerNode *[createdNodesHashTableSize];
	memset(createdNodesHashTable, 0, sizeof(PlannerNode*) * createdNodesHashTableSize);
}

PathPlannerAStarOptimized::~PathPlannerAStarOptimized()
{
	cout << "PathPlannerAStarOptimized::~PathPlannerAStarOptimized" <<endl;

	CleanUp();
	
	delete createdNodesHashTable;
}



void PathPlannerAStarOptimized::PlanPath(int _ix, int _iy, int _gx, int _gy)
{
	cout << "PathPlannerAStarOptimized::PlanPath" <<endl;

	ix = _ix;
	iy = _iy;
	gx = _gx;
	gy = _gy;

	current = NULL;
	foundGoal = false;
	isDone = false;


	//TODO: insert your code here
}

void PathPlannerAStarOptimized::Run()
{

	DWORD startTime = GetTickCount();


	while (!open.empty()){

		//TODO: insert your code here

		//After doing one step of the planning, see if we have run over our allowed timeslice
		if ((int)(GetTickCount() - startTime) > CPathPlannerApp::instance->timeSlice)
			return;
	}

	isDone = true;

}


bool PathPlannerAStarOptimized::IsDone()
{
	//cout << "PathPlannerAStarOptimized::isDone" <<endl;
	return isDone;
}

void PathPlannerAStarOptimized::Draw(CDC *dc)
{
	//cout << "PathPlannerAStarOptimized::Draw" <<endl;

	//TODO: insert your code here
}


void PathPlannerAStarOptimized::Settings()
{
	cout << "PathPlannerAStarOptimized::Settings()" << endl;

	CPlannerSettingsDialog dialog(NULL);

	dialog.m_heuristicWeight		= heuristicWeight;
	dialog.m_diagonalPenalty		= diagonalPenalty;
	dialog.m_closedHashTableSize	= createdNodesHashTableSize;


	if (dialog.DoModal() == IDOK){
		heuristicWeight	= dialog.m_heuristicWeight;
		diagonalPenalty	= dialog.m_diagonalPenalty? true: false;
	}
}


void PathPlannerAStarOptimized::ShowInfo()
{
	cout << "PathPlannerAStarOptimized::ShowInfo" <<endl;

	
	float goalGiveCost = -1.0;
	if (!solution.empty())
		goalGiveCost = solution[0]->givenCost;	



	char buffer[512]; 
	memset(&buffer, 0, sizeof(buffer));

	sprintf(
		buffer, 	
		" elapsedTime: %g\n runCount: %d\n isDone: %d\n foundGoal: %d\n goalGiveCost: %g\n nodesConstructed: %d\n nodesDestructed: %d\n open.size: %d\n solution.size: %d\n heuristicWeight: %g\n createdNodesHashTableSize: %d\n",		
		(double)CPathPlannerApp::instance->elapsedTime,
		CPathPlannerApp::instance->runCount,
		isDone,
		foundGoal,
		goalGiveCost,
		PlannerNode::nodesConstructed, 
		PlannerNode::nodesDestructed, 
		open.size(), 
		solution.size(),
		heuristicWeight,
		createdNodesHashTableSize
	);

	MessageBox(CPathPlannerApp::instance->m_hWnd, buffer, "Planner Information", MB_OK);
}


void PathPlannerAStarOptimized::CleanUp(){
	cout << "PathPlannerAStarOptimized::CleanUp" <<endl;

	//TODO: insert your code here
}

// inserts so the lowest priority is in the end. if lower is better for you, just use vec_back() to get it
void PathPlannerAStarOptimized::SmartInsert(vector<PlannerNode *> *vec, PlannerNode * node){
	// binarySearch: 
	// determines the index of the search key, if it is contained in the list; otherwise, (-(insertion point) - 1). 
	// The insertion point is defined as the point at which the key would be inserted into the list: the index of the 
	// first element greater than the key, or list.size(), if all elements in the list are less than the specified key. Note that this guarantees that the return value will be >= 0 if and only if the key is found.

	int insertPosition = 0;

    int i = 0;
    for(int k = (*vec).size() - 1; i <= k;)
    {
        int l = (i + k) / 2;
        int i1 = node->compareAStar((*vec)[l]);
        
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


// createdNodesHashTable functions
void PathPlannerAStarOptimized::HashTableInsert(PlannerNode *node){
	//TODO: insert your code here
}

PlannerNode* PathPlannerAStarOptimized::HashTableFind(int x, int y){

	//TODO: insert your code here
	return NULL;
}

PlannerNode* PathPlannerAStarOptimized::HashTableRemove(int x, int y)
{
	//TODO: insert your code here
	return NULL;
}


