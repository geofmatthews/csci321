// PathPlannerAStarNodeMesh.cpp: implementation of the PathPlannerAStarNodeMesh class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"

#include "PathPlannerApp.h"
#include "PathPlannerAStarNodeMesh.h"
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

PathPlannerAStarNodeMesh::PathPlannerAStarNodeMesh()
{
	cout << "PathPlannerAStarNodeMesh::PathPlannerAStarNodeMesh" <<endl;

	ix = iy = gx = gy = 0;
	current		= NULL;
	foundGoal	= false;
	isDone		= false;	
	diagonalPenalty = false;
	heuristicWeight = 1;
}

PathPlannerAStarNodeMesh::~PathPlannerAStarNodeMesh()
{
	cout << "PathPlannerAStarNodeMesh::~PathPlannerAStarNodeMesh" <<endl;

	CleanUp();
}



void PathPlannerAStarNodeMesh::PlanPath(int _ix, int _iy, int _gx, int _gy)
{
	cout << "PathPlannerAStarNodeMesh::PlanPath" <<endl;

	plannerState = STATE_DEFAULT;	

	ix = _ix;
	iy = _iy;
	gx = _gx;
	gy = _gy;

	current = NULL;
	foundGoal = false;
	isDone = false;

	currentMeshNode = NULL;
}

void PathPlannerAStarNodeMesh::Run()
{
	static int successorData[8][2] = {	{0,  -1},	// N
										{1,  -1},	// NE	
										{1,   0},	// E	
										{1,   1},	// SE
										{0,   1},	// S	
										{-1,  1},	// SW						
										{-1,  0},	// W
										{-1, -1}	// NW	
	};

	DWORD startTime = GetTickCount();


	switch (plannerState){

		case STATE_MESH_BUILD_START:
			{
				currentMeshNode = new MeshNode(ix, iy, CPathPlannerApp::instance->collisionMapData[iy][ix]);
				OpenMeshNodes.push_back(currentMeshNode);
				createdMeshNodes[COMPUTE_HASH_CODE(currentMeshNode->x, currentMeshNode->y)] = currentMeshNode;
				plannerState = STATE_MESH_BUILD;
				return;
			}

		case STATE_MESH_BUILD:
			{
				while (!OpenMeshNodes.empty()){
					currentMeshNode = OpenMeshNodes.front();
					OpenMeshNodes.pop_front();

					// for every possible successor
					for (int i=0; i<8; i++){

						int successorX = successorData[i][0] + currentMeshNode->x, 
							successorY = successorData[i][1] + currentMeshNode->y,
							mapData	= CPathPlannerApp::instance->collisionMapData[successorY][successorX];
							
						if (mapData == MAP_DATA_WALL)
							continue;

						MeshNode *foundMeshNode = createdMeshNodes[COMPUTE_HASH_CODE(successorX, successorY)];
						if (foundMeshNode){
							currentMeshNode->connections.push_back(foundMeshNode);
							continue;
						}

						MeshNode* successorMeshNode = new MeshNode(successorX, successorY, mapData);

						currentMeshNode->connections.push_back(successorMeshNode);

						OpenMeshNodes.push_back(successorMeshNode);
						createdMeshNodes[COMPUTE_HASH_CODE(successorMeshNode->x, successorMeshNode->y)] = successorMeshNode;
					}

					if ((int)(GetTickCount() - startTime) > CPathPlannerApp::instance->timeSlice)
						return;
				}
				
				plannerState = STATE_PLAN_START;
			}
			return;

		case STATE_PLAN_START:
			{
				cout << "PathPlannerAStarNodeMesh, STATE_PLAN_START" <<endl;

				PlannerNode	*rootNode = new PlannerNode(createdMeshNodes[COMPUTE_HASH_CODE(ix, iy)], NULL);

				rootNode->heuristicCost = (float)sqrt(  ( ((gx - rootNode->meshNode->x)) * ((gx - rootNode->meshNode->x)) ) + ( ((gy - rootNode->meshNode->y)) * ((gy - rootNode->meshNode->y)) ) );
				rootNode->finalCost = heuristicWeight * rootNode->heuristicCost;

				SmartInsert(&open, rootNode);
				createdPlannerNodes[(unsigned long)rootNode->meshNode] = rootNode;

				plannerState = STATE_PLAN;
			}
			return;

		case STATE_PLAN:
			{
				PlannerNode	*successor = NULL,
							*foundNode = NULL;


				while (!open.empty()){

					// get the next best node
					current = open.back();
					open.pop_back();


					// is it the goal?
					if (current->meshNode->x == gx && current->meshNode->y == gy){
						cout << "goal found" << endl;
						foundGoal = true;

						while (current != NULL){
							solution.push_back(current);
							current = current->parent;
						}
						break;
					}

					for (list<MeshNode*>::iterator itr = current->meshNode->connections.begin(); itr != current->meshNode->connections.end(); itr++){

						// compute the successor's Given cost
						float successorG;

						// if diagonal move
						if (diagonalPenalty && (((*itr)->x - current->meshNode->x) != 0) && (((*itr)->y - current->meshNode->y) != 0) ){
							successorG = current->givenCost + (*itr)->weight * 1.4142f;
						}else{
							successorG = current->givenCost + (*itr)->weight;
						}

						foundNode = createdPlannerNodes[(unsigned long)(*itr)];


						// skip nodes that we have already generated AND are worst.
						if (foundNode && (foundNode->givenCost <= successorG))				
							continue;

						if (foundNode){

							// is it in open? if so remove it!
							for(int j = 0, size = open.size(); j<size; j++){
								if( open[j]->meshNode == (*itr) ){
									open.erase(&open[j]);
									break;
								}
							}

							foundNode->parent = current;
							foundNode->givenCost = successorG;
							foundNode->finalCost = foundNode->givenCost + heuristicWeight * foundNode->heuristicCost;

							SmartInsert(&open, foundNode);

						}else{

							// set up the child 
							successor = new PlannerNode((*itr), current);
							successor->givenCost = successorG;
							successor->heuristicCost = (float)sqrt(  ( ((gx - (*itr)->x)) * ((gx - (*itr)->x)) ) + ( ((gy - (*itr)->y)) * ((gy - (*itr)->y)) ) );
							successor->finalCost = successor->givenCost + heuristicWeight * successor->heuristicCost;

							// put the successor in open
							SmartInsert(&open, successor);

							// every time a node is made, we will add it to the "generated list"
							// this list contains both open and closed nodes. 
							createdPlannerNodes[(unsigned long)successor->meshNode] = successor;
						}			
					}


					//After doing one step of the planning, see if we have run over our allowed timeslice
					if ((int)(GetTickCount() - startTime) > CPathPlannerApp::instance->timeSlice)
						return;
				}

				isDone = true;
			}
			return;
	}
}


bool PathPlannerAStarNodeMesh::IsDone()
{
	//cout << "PathPlannerAStarNodeMesh::isDone" <<endl;
	return isDone;
}

void PathPlannerAStarNodeMesh::Draw(CDC *dc)
{
	//cout << "PathPlannerAStarNodeMesh::Draw" <<endl;


	// draw the node mesh
	for (map<int, MeshNode*>::iterator mapItr= createdMeshNodes.begin(); mapItr != createdMeshNodes.end(); mapItr++){
		int mapData	= 20 * ((*mapItr).second)->weight;
		MeshNode *node = ((*mapItr).second);
		dc->SetPixel(node->x, node->y, RGB(250 - mapData, 150 - mapData, 250 - mapData));
	}


	// draw the created nodes
	for (map<unsigned long, PlannerNode*>::iterator mapItr2= createdPlannerNodes.begin(); mapItr2 != createdPlannerNodes.end(); mapItr2++){
		PlannerNode *node = ((*mapItr2).second);
		int mapData	= 20 * node->meshNode->weight;
		dc->SetPixel(node->meshNode->x, node->meshNode->y, RGB(150 - mapData, 150 - mapData, 250 - mapData));
	}
	
	for (int i=0, size = open.size(); i<size; i++){
		int mapData	= 20 * CPathPlannerApp::instance->collisionMapData[open[i]->meshNode->y][open[i]->meshNode->x];
		dc->SetPixel(open[i]->meshNode->x, open[i]->meshNode->y, RGB(150 - mapData, 250 - mapData, 150 - mapData));
	}

	// draw the path (solution)
	if (!solution.empty()){
		for(int c=0, size = solution.size(); c<size; c++){
			int mapData	= 20 * CPathPlannerApp::instance->collisionMapData[solution[c]->meshNode->y][solution[c]->meshNode->x];
			dc->SetPixel(solution[c]->meshNode->x, solution[c]->meshNode->y, RGB(250 - mapData, 150 - mapData, 150 - mapData));
		}
	
	// draw the "current path"
	}else if (!open.empty()){
		
		PlannerNode *node = current;

		while(node != NULL){
			int mapData	= 20 * CPathPlannerApp::instance->collisionMapData[node->meshNode->y][node->meshNode->x];
			dc->SetPixel(node->meshNode->x, node->meshNode->y, RGB(250 - mapData, 150 - mapData, 150 - mapData));
			node = node->parent;
		}
	}
	
}


void PathPlannerAStarNodeMesh::Settings()
{
	cout << "PathPlannerAStarNodeMesh::Settings()" << endl;

	CPlannerSettingsDialog dialog(NULL);

	dialog.m_heuristicWeight		= heuristicWeight;
	dialog.m_diagonalPenalty		= diagonalPenalty;


	if (dialog.DoModal() == IDOK){
		heuristicWeight	= dialog.m_heuristicWeight;
		diagonalPenalty	= dialog.m_diagonalPenalty? true: false;
	}
}


void PathPlannerAStarNodeMesh::ShowInfo()
{
	cout << "PathPlannerAStarNodeMesh::ShowInfo" <<endl;

	
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
		-1
	);

	MessageBox(CPathPlannerApp::instance->m_hWnd, buffer, "Planner Information", MB_OK);
}


void PathPlannerAStarNodeMesh::CleanUp(){
	cout << "PathPlannerAStarNodeMesh::CleanUp" <<endl;


	PlannerNode	*current = NULL, 
				*next    = NULL;
	
	// draw the node mesh
	for (map<int, MeshNode*>::iterator mapItr= createdMeshNodes.begin(); mapItr != createdMeshNodes.end(); mapItr++){
		delete ((*mapItr).second);
	}


	// draw the created nodes
	for (map<unsigned long, PlannerNode*>::iterator mapItr2= createdPlannerNodes.begin(); mapItr2 != createdPlannerNodes.end(); mapItr2++){
		delete ((*mapItr2).second);
	}
	
	createdMeshNodes.clear();
	createdPlannerNodes.clear();
	OpenMeshNodes.clear();
	solution.clear();
	open.clear();

	cout << "MeshNode::nodesConstructed: " << MeshNode::nodesConstructed << endl;
	cout << "MeshNode::nodesDestructed: " << MeshNode::nodesDestructed << endl;

	cout << "PathPlannerAStarNodeMesh::CleanUp Done" <<endl;
}

// inserts so the lowest priority is in the end. if lower is better for you, just use vec_back() to get it
void PathPlannerAStarNodeMesh::SmartInsert(vector<PlannerNode *> *vec, PlannerNode * node){
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