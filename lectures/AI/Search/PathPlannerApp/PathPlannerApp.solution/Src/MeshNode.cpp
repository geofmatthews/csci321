
#include "MeshNode.h"
using namespace std;

int MeshNode::nodesConstructed = 0;
int MeshNode::nodesDestructed = 0;

MeshNode::MeshNode(int _x, int _y, int _weight)
{
	nodesConstructed++;
	x = _x;
	y = _y;
	weight = _weight;
}

MeshNode::~MeshNode(void)
{
	nodesDestructed++;
}
