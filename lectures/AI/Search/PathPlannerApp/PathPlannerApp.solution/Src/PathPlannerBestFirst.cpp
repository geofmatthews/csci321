// PathPlannerBestFirst.cpp: implementation of the PathPlannerBestFirst class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"

#include "PathPlannerApp.h"
#include "PathPlannerBestFirst.h"
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

PathPlannerBestFirst::PathPlannerBestFirst()
{
	cout << "PathPlannerBestFirst::PathPlannerBestFirst" <<endl;

	
	ix = iy = gx = gy = 0;
	current		= NULL;
	foundGoal	= false;
	isDone		= false;
	
	
	// some prime numbers that can be used for hash table size
	// 101, 151, 199, 307, 401, 499, 599, 797, 911, 997, 1999, 4001
	// NOTE:	when you turn in your project, it should be using hash table size of 
	//			199. When writing your hash table functions, you should try table sizes
	//          of 1 and 4001. 
	closedHashTableSize = 199;

	closedHashTable = new PlannerNode *[closedHashTableSize];
	memset(closedHashTable, 0, sizeof(PlannerNode*) * closedHashTableSize);

}

PathPlannerBestFirst::~PathPlannerBestFirst()
{
	cout << "PathPlannerBestFirst::~PathPlannerBestFirst" <<endl;


	CleanUp();
	delete closedHashTable;
}



void PathPlannerBestFirst::PlanPath(int _ix, int _iy, int _gx, int _gy)
{
	cout << "PathPlannerBestFirst::PlanPath" <<endl;

	ix = _ix;
	iy = _iy;
	gx = _gx;
	gy = _gy;

	current		= NULL;
	foundGoal	= false;
	isDone		= false;

	PlannerNode	*rootNode = new PlannerNode(ix, iy, NULL);

	rootNode->computeHeuristicCost(gx, gy);
	SmartInsert(&open, rootNode);
}

void PathPlannerBestFirst::Run()
{
	//cout << "PathPlannerBestFirst::Run" <<endl;

	DWORD startTime = GetTickCount();

	static int successorData[8][2] = {	{0,  -1},	// N
										{1,  -1},	// NE	
										{1,   0},	// E	
										{1,   1},	// SE
										{0,   1},	// S	
										{-1,  1},	// SW						
										{-1,  0},	// W
										{-1, -1}	// NW	
	};


	PlannerNode	*successor		 = NULL;

	while (!open.empty()){

		current = open.back();
		open.pop_back();
		HashTableInsert(current);

		
		if (current->x == gx && current->y == gy){
			cout << "goal found" << endl;
			foundGoal = true;

			while (current != NULL){
				solution.push_back(current);
				current = current->parent;
			}

			break;
		}


		for (int i=0; i<8; i++){

			int successorX = successorData[i][0] + current->x, 
				successorY = successorData[i][1] + current->y,
				mapData	= CPathPlannerApp::instance->collisionMapData[successorY][successorX];


			if (mapData == MAP_DATA_WALL)
				continue;


			// skip if a node for the same point already exists in the closed list
			if ( HashTableFind(successorX, successorY) != NULL ){
				continue;
			}
			

			bool exists = false;
			
			// search the open List
			for(int j = 0, openSize = open.size(); j<openSize; j++){
				if( (open[j]->x == successorX) && (open[j]->y == successorY) ){
					exists = true;
					break;
				}
			}				

			if (exists)
				continue;

	
			// set up the child 
			successor = new PlannerNode(successorX, successorY, current);
			successor->computeHeuristicCost(gx, gy);

			// put the successor in open using smartInsert so that it is inserted in the proper 
			// spot. SmartInsert performs a binary search and the node's compare function to find the 
			// proper spot in the list. 
			SmartInsert(&open, successor);
		}

		//After doing one step of the planning, see if we have run over our allowed timeslice
		if ((int)(GetTickCount() - startTime) > CPathPlannerApp::instance->timeSlice)
			return;
	}

	isDone = true;
}


bool PathPlannerBestFirst::IsDone()
{
	//cout << "PathPlannerBestFirst::isDone" <<endl;
	return isDone;
}

void PathPlannerBestFirst::Draw(CDC *dc)
{
	//cout << "PathPlannerBestFirst::Draw" <<endl;

	PlannerNode* temp;
	
	// draw a pixel for each closed node
	for(int i=0; i<closedHashTableSize; i++){
		temp = closedHashTable[i];

		while (temp != NULL){
			int mapData	= 20 * CPathPlannerApp::instance->collisionMapData[temp->y][temp->x];
			dc->SetPixel(temp->x, temp->y, RGB(150 - mapData, 150 - mapData, 250 - mapData));
			temp = temp->hashTableNext;
		}
	}

	
	// draw a pixel for each open node
	for (int j=0, size = open.size(); j<size; j++){
		int mapData	= 20 * CPathPlannerApp::instance->collisionMapData[open[j]->y][open[j]->x];
		dc->SetPixel(open[j]->x, open[j]->y, RGB(150 - mapData, 250 - mapData, 150 - mapData));
	}


	// draw the path (solution) if we have resolved it
	if (!solution.empty()){
		for(int i=0, size = solution.size(); i<size; i++){
			int mapData	= 20 * CPathPlannerApp::instance->collisionMapData[solution[i]->y][solution[i]->x];
			dc->SetPixel(solution[i]->x, solution[i]->y, RGB(250 - mapData, 150 - mapData, 150 - mapData));
		}
	
	// else draw the "current path"
	}else if (!open.empty()){
		
		PlannerNode *node = current;

		while(node != NULL){
			int mapData	= 20 * CPathPlannerApp::instance->collisionMapData[node->y][node->x];
			dc->SetPixel(node->x, node->y, RGB(250 - mapData, 150 - mapData, 150 - mapData));
			node = node->parent;
		}
	}

}


void PathPlannerBestFirst::Settings()
{
	cout << "PathPlannerBestFirst::Settings()" << endl;

}

void PathPlannerBestFirst::ShowInfo()
{
	cout << "PathPlannerBestFirst::ShowInfo" <<endl;

	
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
		closedHashTableSize
	);

	MessageBox(CPathPlannerApp::instance->m_hWnd, buffer, "Planner Information", MB_OK);
}


void PathPlannerBestFirst::CleanUp(){
	cout << "PathPlannerBestFirst::CleanUp" <<endl;

	while(!open.empty()){
		delete open.back();
		open.pop_back();
	}

	PlannerNode	*toDelete = NULL;
	for(int i=0; i<closedHashTableSize; i++){	
		while (closedHashTable[i] != NULL){
			toDelete = closedHashTable[i];
			closedHashTable[i] = closedHashTable[i]->hashTableNext;
			delete toDelete;
		}
	}

	solution.clear();
}

// inserts so the lowest priority is in the end. if lower is better for you, just use vec_back() to get it
void PathPlannerBestFirst::SmartInsert(vector<PlannerNode *> *vec, PlannerNode * node){
	// binarySearch: 
	// determines the index of the search key, if it is contained in the list; otherwise, (-(insertion point) - 1). 
	// The insertion point is defined as the point at which the key would be inserted into the list: the index of the 
	// first element greater than the key, or list.size(), if all elements in the list are less than the specified key. Note that this guarantees that the return value will be >= 0 if and only if the key is found.

	int insertPosition = 0;

    int i = 0;
    for(int k = (*vec).size() - 1; i <= k;)
    {
        int l = (i + k) / 2;
        int i1 = node->compareBestFirst((*vec)[l]);
        
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


// closedHashTable functions
void PathPlannerBestFirst::HashTableInsert(PlannerNode *node){

	int hashCode = COMPUTE_HASH_CODE(node->x, node->y);
	int index = hashCode%closedHashTableSize;

	PlannerNode *temp;

	temp = closedHashTable[index];
	closedHashTable[index] = node;
	node->hashTableNext = temp;
}

PlannerNode* PathPlannerBestFirst::HashTableFind(int x, int y){

	int hashCode = COMPUTE_HASH_CODE(x, y);
	int index = hashCode%closedHashTableSize;

	PlannerNode *itr = closedHashTable[index];

	while(itr != NULL){
		if ((itr->x == x) && (itr->y == y) )
			return itr;

		itr = itr->hashTableNext;
	}

	return NULL;
}

PlannerNode* PathPlannerBestFirst::HashTableRemove(int x, int y)
{
	int hashCode = COMPUTE_HASH_CODE(x, y);
	int index = hashCode%closedHashTableSize;

	PlannerNode *iterator = closedHashTable[index];

	if (iterator->x == x && iterator->y == y){
		closedHashTable[index] = iterator->hashTableNext;
		return iterator;
	}

	while(iterator->hashTableNext){	
		if ((iterator->hashTableNext->x == x) && (iterator->hashTableNext->y == y)){
			iterator->hashTableNext = iterator->hashTableNext->hashTableNext;
			return iterator->hashTableNext;
		}

		iterator = iterator->hashTableNext;
	}

	return NULL;
}


