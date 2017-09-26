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

	PlannerNode* root = new PlannerNode(ix, iy, NULL);

	open.push_back(root);
}

void PathPlannerBreadthFirst::Run()
{
	//cout << "PathPlannerBreadthFirst::Run" <<endl;

	DWORD startTime = GetTickCount();

	// successor information table. it includes dx, dy
	static int successorData[8][2] = {	{0,  -1},	// N
										{1,  -1},	// NE	
										{1,   0},	// E	
										{1,   1},	// SE
										{0,   1},	// S	
										{-1,  1},	// SW						
										{-1,  0},	// W
										{-1, -1}	// NW	
	};


	while (!open.empty()){
			
		current = open.front();
		open.pop_front();
		
		// since every node coming out of open should end up in the closed list, 
		// it is easier and safe to insert it into closed immediately after poping it from open
		closed.push_back(current);

		
		if (current->x == gx && current->y == gy){
			cout << "goal found" << endl;
			foundGoal = true;

			// populate the solution list with the path
			while (current != NULL){
				solution.push_back(current);
				current = current->parent;
			}

			break;
		}


		// for every nearBy point
		for (int i=0; i<8; i++){

			int successorX = successorData[i][0] + current->x, 
				successorY = successorData[i][1] + current->y,
				mapData	= CPathPlannerApp::instance->collisionMapData[successorY][successorX];

			// skip if it is a wall
			if (mapData == MAP_DATA_WALL)
				continue;
			
			bool exists = false;
			
			// search the open list		
			for(iterator = open.begin(); iterator != open.end(); iterator++){
				if (successorX == (*iterator)->x && successorY == (*iterator)->y){
					exists = true;
					break;
				}
			}


			// skip if a node for the same point already exists in the open list
			if (exists)
				continue;


			// search the closed list
			for(iterator = closed.begin(); iterator != closed.end(); iterator++){
				if (successorX == (*iterator)->x && successorY == (*iterator)->y){
					exists = true;
					break;
				}
			}


			// skip if a node for the same point already exists in the closed list
			if (exists)
				continue;

			// if we make it this far, we can go ahead and make a new node for this spot of the map
			PlannerNode *successor = new PlannerNode(successorX, successorY, current);
			open.push_back(successor);			
		}

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

	// draw a pixel for each closed node
	for(iterator = closed.begin(); iterator != closed.end(); iterator++){
		dc->SetPixel((*iterator)->x, (*iterator)->y, RGB(0, 0, 255));
	}

	
	// draw a pixel for each open node
	for(iterator = open.begin(); iterator != open.end(); iterator++){
		dc->SetPixel((*iterator)->x, (*iterator)->y, RGB(0, 255, 0));
	}


	// draw the path (solution) if we have resolved it
	if (!solution.empty()){
		for(int i=0, size = solution.size(); i<size; i++){
			dc->SetPixel(solution[i]->x, solution[i]->y, RGB(255, 0, 0));
		}
	
	// else draw the "current path"
	}else if (current != NULL){
		
		// get the "best node" in open and draw the path back to start
		PlannerNode *node = current;

		while(node != NULL){
			dc->SetPixel(node->x, node->y, RGB(125, 0, 0));	
			node = node->parent;
		}
	}

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

	// delete all nodes in open
	while(!open.empty()){
		delete open.back();
		open.pop_back();
	}

	// delete all nodes in closed
	while(!closed.empty()){
		delete closed.back();
		closed.pop_back();
	}

	// since nodes in solution are already in open/closed list and were deleted, 
	// we should not try to delete them again. call clear to flush the pointers to
	// already deleted nodes
	solution.clear();
}

