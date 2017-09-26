/**
 *	Author: Syrus Mesdaghi, SyrusM@hotmail.com
 */


// PathPlannerAStarNodeMesh.h: interface for the PathPlannerAStarNodeMesh class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(PATHPLANNERASTARNODEMESH_H)
#define PATHPLANNERASTARNODEMESH_H

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include "PathPlannerBase.h"
#include "PlannerNode.h"
#include "MeshNode.h"

// STL
#pragma warning (disable:4786)

#include <vector>
#include <list>
#include <map>
using namespace std;


// computes the hash code of a pair of coordinates
// WARNING: this methode will fail if the x or y values are greater than 0xFFFF or 65,535
// TODO: write the hash code macro
#define COMPUTE_HASH_CODE(x, y)	(0xFFFF0000 & (x << 16) | (0xFFFF & y))



class PathPlannerAStarNodeMesh : public PathPlannerBase  
{
	
public:

	typedef enum PlannerState{
		STATE_MESH_BUILD_START,
		STATE_MESH_BUILD,
		STATE_PLAN_START,
		STATE_PLAN,
		STATE_DONE,

		STATE_DEFAULT = STATE_MESH_BUILD_START
	};

	PlannerState plannerState;

	PlannerNode* current;

	vector<PlannerNode *>	open;				
	vector<PlannerNode *>	solution;
	map<unsigned long, PlannerNode*> createdPlannerNodes;

	int ix, iy, gx, gy;

	bool	foundGoal,
			isDone,
			diagonalPenalty;

	float heuristicWeight;
	

	//--------------- Members regarding NodeMesh---------------
	MeshNode *currentMeshNode;
	list<MeshNode*> OpenMeshNodes;
	map<int, MeshNode*> createdMeshNodes;
	
public:
	PathPlannerAStarNodeMesh();
	virtual ~PathPlannerAStarNodeMesh();

	void Draw(CDC *dc);
	void PlanPath(int ix, int iy, int gx, int gy);
	void Run();
	bool IsDone();
	void ShowInfo();
	void Settings();
	void CleanUp();


	
	// inserts the node into the provided vector. it searches the vector to find the "correct" insertion point.
	// it assumes that vec is already sorted. the PlannerNode class MUST provide a compare() function that allows SmartInsert 
	// determine wheather a node is <, >, or == to another
	void SmartInsert(vector<PlannerNode *> *vec, PlannerNode * node);
};

#endif // !defined(PATHPLANNERASTARNODEMESH_H)
