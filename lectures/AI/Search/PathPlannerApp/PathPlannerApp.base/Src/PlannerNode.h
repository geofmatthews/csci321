/**
 *	Author: Syrus Mesdaghi, SyrusM@hotmail.com
 */

#ifndef PLANNER_NODE_H
#define	PLANNER_NODE_H

#include "MeshNode.h"

#include <math.h>
#include <stdio.h>


class PlannerNode  
{
public:

	int x, 
		y;

	float	heuristicCost,	// the heuristic of the node used for planners such as best first and A*
			givenCost;		// the given cost used for planners such as dijkstra and A*
			
	double	finalCost;		// final cost used by A*

	PlannerNode	*parent,				
				*hashTableNext;			// pointer used by the hash table
	

	// if you are path planning on the "grid" (or collisionMapData[][]), you can ignore this member. When planning on a nodemesh, a planner node needs to 
	// keep track of which meshNode (a node of the nodemesh) it referes to. this member is in some sense the replacement for x, y members of this class
	// when planning on a nodemesh.
	MeshNode* meshNode;


	// these are for debugging purposes 
	static int	nodesConstructed,	// counter that counts the number of nodes ever constructed 
				nodesDestructed;	// counter that counts the number of nodes ever destructed


	PlannerNode();
	PlannerNode(int _x, int _y, PlannerNode *_parent);		// for planning on a grid
	PlannerNode(MeshNode* _meshNode, PlannerNode *_parent); // for planning on a nodeMesh instead of a grid
	~PlannerNode();


	// computes the heuristic of a node, with respect to a goal 
	void	computeHeuristicCost(int goalX, int goalY);

	// writes the significant data of the node to the console
	void	print();
	
	
	// This function is called by "SmartInsert" when a node is being inserted into
	// the vector (see prototype for SmartInsert). This function will help SmartInsert
	// to figure out where a node should be inserted into the vector, so that the vector 
	// remains sorted.
	//
	// Compares the node "* second" to "this" and returns 1, 0, -1 based on wheather
	// "this" is greater, equal, or smaller than "* second"
	//
	// NOTE: What member variable of a PlannerNode determins if a PlannerNode is "less than" another?
	//       you will have to compare different member variable based on which planning 
	//       algorithm you are implementing. (such as Djikstra's, Best First, A*)
	int compareBestFirst(PlannerNode *second){
		//TODO: insert your code here
		return 0;
	}
	
	int compareDijkstra(PlannerNode *second){
		//TODO: insert your code here
		return 0;
	}
	
	int compareAStar(PlannerNode *second){
		//TODO: insert your code here
		return 0;
	}
	
};

#endif