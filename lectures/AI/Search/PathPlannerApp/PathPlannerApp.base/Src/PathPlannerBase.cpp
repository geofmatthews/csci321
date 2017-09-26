// PathPlannerBase.cpp: implementation of the PathPlannerBase class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "PathPlannerBase.h"

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

PathPlannerBase::PathPlannerBase()
{
}

PathPlannerBase::~PathPlannerBase()
{

}


void PathPlannerBase::PlanPath(int ix, int iy, int gx, int gy)
{
	cout << "WARNING: PathPlannerBase::PlanPath" <<endl;

}

void PathPlannerBase::Draw(CDC *dc)
{
	cout << "WARNING: PathPlannerBase::Draw" <<endl;

}

 
void PathPlannerBase::Run()
{
	cout << "WARNING: PathPlannerBase::Run" <<endl;

}


bool PathPlannerBase::IsDone()
{
	cout << "WARNING: PathPlannerBase::IsDone" <<endl;
	return true;
}

void PathPlannerBase::Settings()
{
	cout << "WARNING: PathPlannerBase::Settings" <<endl;

}

void PathPlannerBase::ShowInfo()
{
	cout << "WARNING: PathPlannerBase::ShowInfo" <<endl;

}


void PathPlannerBase::CleanUp()
{
	cout << "WARNING: PathPlannerBase::CleanUp" <<endl;

}

