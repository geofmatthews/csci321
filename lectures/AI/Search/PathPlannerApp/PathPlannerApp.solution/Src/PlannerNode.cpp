

#include "PlannerNode.h"

int PlannerNode::nodesConstructed = 0;
int PlannerNode::nodesDestructed  = 0;

PlannerNode::PlannerNode()
{
	nodesConstructed++;

	x = y = 0;
	finalCost = givenCost = heuristicCost = 0;
	parent = hashTableNext = NULL;
	meshNode = NULL;
}


PlannerNode::PlannerNode(int _x, int _y, PlannerNode *_parent)
{
	nodesConstructed++;

	finalCost = givenCost = heuristicCost = 0;
	hashTableNext = NULL;

	x = _x;
	y = _y;		
	parent = _parent;
	meshNode = NULL;
}

PlannerNode::PlannerNode(MeshNode* _meshNode, PlannerNode *_parent){
	nodesConstructed++;

	finalCost = givenCost = heuristicCost = 0;
	hashTableNext = NULL;

	parent = _parent;
	meshNode = _meshNode;
}


PlannerNode::~PlannerNode()
{
	nodesDestructed++;
}

void PlannerNode::computeHeuristicCost(int goalX, int goalY){		
	
	heuristicCost = (float)sqrt(  ( ((goalX - x)) * ((goalX - x)) ) + ( ((goalY - y)) * ((goalY - y)) ) );
}

void PlannerNode::print(){
	printf("PlannerNode: x: %d, y: %d, g: %.1f h: %.1f, f: %f\n", x, y, givenCost, heuristicCost, finalCost);
}


