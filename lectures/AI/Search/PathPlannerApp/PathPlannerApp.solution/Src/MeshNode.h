/**
 *	Author: Syrus Mesdaghi, SyrusM@hotmail.com
 */

/**
 *	this node class is used to represent points of interest in the world. It can be used as an alternate approach 
 *  to representing the world. Most planners in this project do NOT use this node class at all. 
 */

#ifndef NODE_H
#define	NODE_H

#pragma warning (disable:4786)
#include <list>

class MeshNode  
{
public:

	int x, 
		y;

	int weight;

	static int	nodesConstructed,	// counter that counts the number of nodes ever constructed 
				nodesDestructed;	// counter that counts the number of nodes ever destructed

	std::list<MeshNode*>	connections;	// other possible nodes that we can go to from this node

	MeshNode();
	MeshNode(int _x, int _y, int _weight);
	~MeshNode();
};

#endif