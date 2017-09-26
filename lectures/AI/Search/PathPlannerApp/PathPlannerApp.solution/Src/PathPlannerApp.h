/**
 *	The   Path   Planner  Application  is  made to allow 
 *  convenient  creation,  demonstration,  and  analysis 
 *  of  different  path planning  algorithms.  Different 
 *  algorithms  can  be  implemented  as  separate class 
 *  files. for  information on each  implementation  and 
 *  its author, see the header file corresponding to the 
 *  specific algorithm.
 *
 *	Created by Syrus Mesdaghi, SyrusM@hotmail.com
 */


/**
 * PathPlannerApp.h is the header of the application. most of the functionalities of the 
 * app are defined here and the planning process is initiated from this class. Each planning 
 * algorithm can be implemented as separate class. The application can access the planner
 * functions inherited from PathPlannerBase.h
 *
 * The application initializes a planner, gives it the chance to run, and then destroys the instance.
 * For more information, see PathPlannerBase.h
 *
 */ 


// PathPlannerApp.h : main header file for the PathPlannerApp
//

#if !defined(PATHPLANNERAPP_H)
#define PATHPLANNERAPP_H

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif


#include "resource.h"       // main symbols
#include "PathPlannerBase.h"
#include "HighResolutionTimer.h"


//------------------- DEBUG flags  -----------------------
//#define PATH_PLANNER_DEBUG
//#define PATH_PLANNER_CREATE_CONSOLE

#ifdef _DEBUG
	#define PATH_PLANNER_CREATE_CONSOLE
#endif




//---- when a collisionmap is loaded, a 2d table is generated and the corresponding indeces are
//     filled with the following values
#define MAP_DATA_WALL			-1	// black region. impassable
#define MAP_DATA_UNDEFINED		0	// reserved
#define MAP_DATA_WEIGHT1		1	// white region 
#define MAP_DATA_WEIGHT2		2	// light gray
#define MAP_DATA_WEIGHT3		3	// gray
#define MAP_DATA_WEIGHT4		4	// dark gray


/**
 *	Colors recognized in the bitmap which maps are mapped to the values above
 */
#define MAP_COLOR_WALL			0	// black region. impassable
#define MAP_COLOR_WEIGHT1		255	// white region 
#define MAP_COLOR_WEIGHT2		204	// light gray
#define MAP_COLOR_WEIGHT3		153	// gray
#define MAP_COLOR_WEIGHT4		102	// dark gray



class CMainFrame;
/////////////////////////////////////////////////////////////////////////////
// CPathPlannerApp:
// See PathPlannerApp.cpp for the implementation of this class
//

class CPathPlannerApp : public CWinApp
{
public:

	//WARNING: the following IDs have to be assigned so that they 
	//         match the IDs in the text Combo (List) Box of the Settings Dialog (IDD_DIALOG_SETTINGS)
	//         make sure the order is identical to what appears in the comboBox
	//         when the app launches.
	typedef enum {
		ALGORITHM_ASTAR,
		ALGORITHM_ASTAR_OPTIMIZED,
		ALGORITHM_ASTAR_NODE_MESH,
		ALGORITHM_BEST_FIRST,
		ALGORITHM_BREADTH_FIRST,
		ALGORITHM_DIJKSTRA,
		ALGORITHM_IDASTAR,

		ALGORITHM_DEFAULT = ALGORITHM_ASTAR_OPTIMIZED
	} AlgorithmId;


	// flags that indicate the current state of the application
	typedef enum {
		STATE_IDLE,
		STATE_RUN_START,
		STATE_RUN,
		STATE_RUN_END,

		STATE_DEFAULT = STATE_IDLE
	} ApplicationState;


	// singleton instance
	static	CPathPlannerApp *instance;	

	HighResolutionTimer *highResolutionTimer;
	
	// maine frame
	CMainFrame* pFrame;
	HWND		m_hWnd;

	// pointer to 
	PathPlannerBase	*planner;

	
	ApplicationState	applicationState;		

	int algorithmId;	
		
	int	initialX,
		initialY,
		goalX,
		goalY;

	int	**collisionMapData; // Collision map data 	
							// (-1, 1, 2, 3, 4 to indicate different regions of the map)

	int	collisionMapWidth,
		collisionMapHeight;

	int runCount,
		timeSlice;		//time slice in milliseconds

	char *collisionMapFilename,
		 *defaultCollisionMapFilename;

	//DWORD	startTime;		// time stamp when the planner started
	double	elapsedTime;	// time in milliseconds that the planner spent searching

	bool	drawProgress;
			//plannerIsRunning;

public:
	CPathPlannerApp();
	~CPathPlannerApp();

	void StateRunStart();
	void StateRun();
	void StateRunEnd();
// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CPathPlannerApp)
	public:
	virtual BOOL InitInstance();
	virtual BOOL OnIdle(LONG lCount);
	//}}AFX_VIRTUAL

// Implementation

public:
	//{{AFX_MSG(CPathPlannerApp)
	afx_msg void OnRunStart();
	afx_msg void OnRunStop();
	afx_msg void OnRunPause();
	afx_msg void OnFileOpen();
	afx_msg void OnDrawProgress();
	afx_msg void OnSettings();
	afx_msg void OnPlannerInitialize();
	afx_msg void OnPlannerSettings();
	afx_msg void OnPlannerInfo();
	afx_msg void OnPlannerDestroy();
	afx_msg void OnPlannerReuse();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()

	//TODO: TO ADD: call back for window updates

public:
	/**
	 *	If a planner needs to hold on to  the main thread, the application will not get the 
	 *  chance to process any msgs. Call this function to yield to any pending messages. 
	 *  if true is pased as argument, a repaint gets forced.
	 */
	void YieldToMessages(bool postPaintMsg);
	
	// loads the corresponding collision map and makes the proper updates
	void SetCollisionMap(char *filename);

	// frees up the resources used by the collision map
	void DeleteCollisionMapData();
	
	// called by the mainframe to allow the app to call the draw of the planner
	void Draw(CDC *dc);

	// creates a console and sets it up so cout... print to it
	// WARNING: this function has to get called before the first write to the console happens
	void	CreateConsoleAndSetStdout();

	// loads a bitmap specified by collisionMapFilename. it assumes the bitmap ONLY uses colors
	// defined by MAP_COLOR_WALL, MAP_COLOR_WEIGHT1, MAP_COLOR_WEIGHT2, MAP_COLOR_WEIGHT3, MAP_COLOR_WEIGHT4
	// it uses thoes colors to fill the table collisionMapData[][] with values MAP_DATA_WALL, MAP_DATA_WEIGHT1, ...
	void	LoadCollisionMap();

	void	ResetSharedMembers();
};

// the console handler routine
BOOL	WINAPI CloseConsoleHandlerRoutine(DWORD dwCtrlType);

/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(PATHPLANNERAPP_H)
