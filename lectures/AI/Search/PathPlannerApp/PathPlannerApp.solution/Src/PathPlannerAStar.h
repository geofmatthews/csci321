/**
 *	Author: Syrus Mesdaghi, SyrusM@hotmail.com
 */


// PathPlannerAStar.h: interface for the PathPlannerAStar class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(PATHPLANNERASTAR_H)
#define PATHPLANNERASTAR_H

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



class PathPlannerAStar : public PathPlannerBase  
{
	
public:
	
	PlannerNode* current;

	vector<PlannerNode *>	open;				
	vector<PlannerNode *>	solution;

	list<PlannerNode *>::iterator iterator;

	int ix, iy, gx, gy;

	bool	foundGoal,
			isDone,
			diagonalPenalty;

	float heuristicWeight;
	
	PlannerNode **closedHashTable;	// pointer to hashTable's table 

	// some prime numbers that can be used for hash table size
	// 101, 151, 199, 307, 401, 499, 599, 797, 911, 997, 1999, 4001
	// NOTE:	when you turn in your project, it should be using hash table size of 
	//			199. When writing your hash table functions, you should try table sizes
	//          of 1 and 4001. 
	int		closedHashTableSize;


public:
	PathPlannerAStar();
	virtual ~PathPlannerAStar();

	void Draw(CDC *dc);
	void PlanPath(int ix, int iy, int gx, int gy);
	void Run();
	bool IsDone();
	void ShowInfo();
	void Settings();
	void CleanUp();


	
	// inserts the node into the provided vector. it searches the vector to find the "correct" insertion point.
	// it assumes that vec is already sorted. the PlannerNode class MUST provide a compare() function that allows SmartInsert 
	// determine wether a node is <, >, or == to another
	void SmartInsert(vector<PlannerNode *> *vec, PlannerNode * node);

	// inserts node into hashTable[]
	void	HashTableInsert(PlannerNode *node);

	// removes node from give the x and y
	PlannerNode*	HashTableRemove(int x, int y);

	// checkes wether or not a node with coordinates x, y, exists in the table.
	// if so, it returns the pointer to that node else it returns NULL
	PlannerNode*	HashTableFind(int x, int y);
};

#endif // !defined(PATHPLANNERASTAR_H)
