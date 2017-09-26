
// PathPlannerApp.cpp : Defines the class behaviors for the application.
//

#include "stdafx.h"


#include "PathPlannerApp.h"
#include "PathPlannerBreadthFirst.h"
#include "PathPlannerBestFirst.h"
#include "PathPlannerDijkstra.h"
#include "PathPlannerAStar.h"
#include "PathPlannerAStarOptimized.h"
#include "PathPlannerAStarNodeMesh.h"


#include "MainFrm.h"
#include "SettingsDialog.h"
#include "HighResolutionTimer.h"

#include <io.h>		// console output
#include <FCNTL.H>	// console defines


#include <iostream>
using namespace std;


#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CPathPlannerApp

// initialize the static member of the class
CPathPlannerApp *CPathPlannerApp::instance = NULL;


BEGIN_MESSAGE_MAP(CPathPlannerApp, CWinApp)
	//{{AFX_MSG_MAP(CPathPlannerApp)
	ON_COMMAND(ID_RUN_START, OnRunStart)
	ON_COMMAND(ID_RUN_STOP, OnRunStop)
	ON_COMMAND(ID_RUN_PAUSE, OnRunPause)
	ON_COMMAND(ID_FILE_OPEN, OnFileOpen)
	ON_COMMAND(ID_DRAW_PROGRESS, OnDrawProgress)
	ON_COMMAND(ID_SETTINGS, OnSettings)
	ON_COMMAND(ID_PLANNER_INITIALIZE, OnPlannerInitialize)
	ON_COMMAND(ID_PLANNER_SETTINGS, OnPlannerSettings)
	ON_COMMAND(ID_PLANNER_INFO, OnPlannerInfo)
	ON_COMMAND(ID_PLANNER_DESTROY, OnPlannerDestroy)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()


/////////////////////////////////////////////////////////////////////////////
// CPathPlannerApp construction

CPathPlannerApp::CPathPlannerApp()
{
	instance = this;


#ifdef PATH_PLANNER_CREATE_CONSOLE	
	CreateConsoleAndSetStdout();
	cout << "console created" << endl;
//	MessageBox(NULL, "console created", "CPathPlannerApp", MB_OK);
#endif

	highResolutionTimer = new HighResolutionTimer();


	applicationState = ApplicationState::STATE_DEFAULT;
	algorithmId = AlgorithmId::ALGORITHM_DEFAULT;	 
	drawProgress = true;
	timeSlice = -1;
	planner = NULL;

	collisionMapFilename = NULL;
	collisionMapData = NULL;

}

CPathPlannerApp::~CPathPlannerApp()
{
	cout << "CPathPlannerApp::~CPathPlannerApp" << endl;
	
	if (planner!= NULL){
		delete planner;
		planner = NULL;
	}

	DeleteCollisionMapData();

	if (collisionMapFilename != NULL)
		delete collisionMapFilename;

#ifdef	PATH_PLANNER_CREATE_CONSOLE
	FreeConsole();
#endif

	delete highResolutionTimer;
	
	//confirm that destructor was called
	//MessageBeep(MB_OK);
}

/////////////////////////////////////////////////////////////////////////////
// The one and only CPathPlannerApp object

CPathPlannerApp theApp;

/////////////////////////////////////////////////////////////////////////////
// CPathPlannerApp initialization

BOOL CPathPlannerApp::InitInstance()
{
	AfxEnableControlContainer();

	// Standard initialization
	// If you are not using these features and wish to reduce the size
	//  of your final executable, you should remove from the following
	//  the specific initialization routines you do not need.

#ifdef _AFXDLL
	Enable3dControls();			// Call this when using MFC in a shared DLL
#else
	Enable3dControlsStatic();	// Call this when linking to MFC statically
#endif

	// Change the registry key under which our settings are stored.
	// TODO: You should modify this string to be something appropriate
	// such as the name of your company or organization.
	SetRegistryKey(_T("Local AppWizard-Generated Applications"));


	// To create the main window, this code creates a new frame window
	// object and then sets it as the application's main window object.

	pFrame = new CMainFrame;
	m_pMainWnd = pFrame;

	// create and load the frame with its resources

	pFrame->LoadFrame(IDR_MAINFRAME, WS_OVERLAPPEDWINDOW | FWS_ADDTOTITLE, NULL, NULL);

	m_hWnd = pFrame->m_hWnd;



	// defaul map file 
	defaultCollisionMapFilename = "Data\\CollisionMap\\CollisionMapBop.size100.color24bit.bmp";
	
	SetCollisionMap(defaultCollisionMapFilename);

	// The one and only window has been initialized, so show and update it.
	pFrame->ShowWindow(SW_SHOW);
	pFrame->UpdateWindow();


	//display the settings dialog on startup
	OnSettings();
	
	return TRUE;
}


void CPathPlannerApp::SetCollisionMap(char *filename){
	FILE* file = NULL;
	
	if ( (file = fopen( filename, "r") ) == NULL ){
		printf("====>> File could not be opened: %s\n", filename);
		collisionMapFilename = NULL;
		return; 
	
	}else{
		fclose(file);
		
		delete collisionMapFilename;

		int length = strlen(filename) + 1;
		collisionMapFilename = new char [length];
		memcpy(collisionMapFilename, filename, length);   
		cout << "collisionMapFilename: " << collisionMapFilename <<endl;
	}

	
	LoadCollisionMap();

	// tell the child window to load the map as well 
	pFrame->GetChildView()->LoadCollisionMap();
	pFrame->OnViewResize();
}

/**
 *	creates a console and sets it up so cout... print to it
 */
void CPathPlannerApp::CreateConsoleAndSetStdout(){

	// Allocate a console for this app 
	AllocConsole(); 
	SetConsoleCtrlHandler(CloseConsoleHandlerRoutine, TRUE); 

	// Redirect unbuffered STDOUT to the console 
	HANDLE consoleStdOutHandle = GetStdHandle(STD_OUTPUT_HANDLE); 

	*stdout = *( _fdopen(_open_osfhandle((long)consoleStdOutHandle, _O_TEXT), "w") ); 
	setvbuf(stdout, NULL, _IONBF, 0);
}


BOOL WINAPI CloseConsoleHandlerRoutine(DWORD dwCtrlType)
{
	cout << "CloseConsoleHandlerRoutine()"<< endl;
	
    switch (dwCtrlType)
   {
      case CTRL_CLOSE_EVENT:
		  CloseWindow(CPathPlannerApp::instance->m_hWnd);
		  return TRUE;
		  break;
   }
   return FALSE;
}

void CPathPlannerApp::YieldToMessages(bool postPaintMsg){
	
	//call child view's invalidate
	if (drawProgress && postPaintMsg){
		// generate paint msg
		pFrame->GetChildView()->Invalidate(FALSE);	
	}
	
	MSG			msg;
	// check for msg
	while(PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)){
		
		//printf("msg.message: %u\n", msg.message);
		TranslateMessage(&msg);

		// Send the message to the window proc.
		DispatchMessage(&msg);
	}
	
}

void CPathPlannerApp::DeleteCollisionMapData(){
	
	if (collisionMapData != NULL){
		for (int yi = 0; yi < collisionMapHeight; yi++)
			delete collisionMapData[yi];
	}

	delete collisionMapData;

	collisionMapData = NULL;


}


void CPathPlannerApp::LoadCollisionMap(){

	if (collisionMapFilename == NULL){
		MessageBox(NULL, "collisionMapFilename is NULL", "Path Planner", MB_ICONINFORMATION);
		return;
	}

	/**
	 *  load a device independent (DI) copy which will be used for extracting the map information
	 */
	HBITMAP collisionMapDI = (HBITMAP)LoadImage(NULL, collisionMapFilename,IMAGE_BITMAP, collisionMapWidth , collisionMapHeight, LR_CREATEDIBSECTION | LR_LOADFROMFILE);

	BITMAP bitmapInformation;
	GetObject(collisionMapDI, sizeof(bitmapInformation), &bitmapInformation);
	
	if (bitmapInformation.bmBitsPixel != 24){
		MessageBox(NULL, "Only 24 bit bitmaps are supported.", "Path Planner", MB_ICONINFORMATION);
		cout << "====> CRITICAL: Only 24 bit bitmaps are supported. the loaded image is: " << bitmapInformation.bmBitsPixel << endl;
	}

	collisionMapWidth = bitmapInformation.bmWidth;
	collisionMapHeight = bitmapInformation.bmHeight;

	initialX = 1;
	initialY = 1;

	goalX = collisionMapWidth - 2;
	goalY = collisionMapHeight - 2;
	
	
	DeleteCollisionMapData();
	
	// Dynamically Allocate memory for collision map data array.
	collisionMapData = new int* [collisionMapHeight];
	memset(collisionMapData, 0, sizeof(int)*collisionMapHeight);

	for (int yi = 0; yi < collisionMapHeight; yi++)
		collisionMapData[yi] = new int [collisionMapWidth];


	unsigned char	red,
					green,
					blue;

	unsigned char	*bitmapByte = (unsigned char *)bitmapInformation.bmBits;
	

	for (int y = collisionMapHeight - 1; y >= 0 ; y--){
		for (int x = 0 ; x < collisionMapWidth ; x++){

			blue	= *bitmapByte;
			bitmapByte++;
			green	= *bitmapByte;
			bitmapByte++;
			red		= *bitmapByte;
			bitmapByte++;

			/**
			cout << "["<< y << "][" << x << "]  red: " << (int)red << ", green: " << (int)green << ", blue:" << (int)blue << endl;
			if (red == 255 && green == 0 && blue == 0){
				MessageBox(NULL, "Found: red", "Path Planner", MB_ICONINFORMATION);
			}
			*/

			if (red == MAP_COLOR_WEIGHT1 && green == MAP_COLOR_WEIGHT1 && blue == MAP_COLOR_WEIGHT1){
				collisionMapData[y][x] = MAP_DATA_WEIGHT1;

			}else if (red == MAP_COLOR_WALL && green == MAP_COLOR_WALL && blue == MAP_COLOR_WALL){
				collisionMapData[y][x] = MAP_DATA_WALL;
			
			}else if (red == MAP_COLOR_WEIGHT2 && green == MAP_COLOR_WEIGHT2 && blue == MAP_COLOR_WEIGHT2){
				collisionMapData[y][x] = MAP_DATA_WEIGHT2;
				
			}else if (red == MAP_COLOR_WEIGHT3 && green == MAP_COLOR_WEIGHT3 && blue == MAP_COLOR_WEIGHT3){
				collisionMapData[y][x] = MAP_DATA_WEIGHT3;

			}else if (red == MAP_COLOR_WEIGHT4 && green == MAP_COLOR_WEIGHT4 && blue == MAP_COLOR_WEIGHT4){
				collisionMapData[y][x] = MAP_DATA_WEIGHT4;
				
			}else {
				
				collisionMapData[y][x] = MAP_DATA_WALL;			
				cout << "WARNING: undefined color was used in the map. converting it to MAP_DATA_WALL"<< endl;
			}
		}
	}

	// we no longer need the DI version of the image
	DeleteObject(collisionMapDI);


	/**
	// dump the content of collisionMapData 
	for (y = 0; y < collisionMapHeight; y++){
		for (int x = 0; x < collisionMapWidth; x++){
			cout << "["<< y << "][" << x << "] : " << collisionMapData[y][x] << endl;
		}
	}
	*/
}


BOOL CPathPlannerApp::OnIdle(LONG lCount) 
{

	//cout << "---> elapsed time: " << highResolutionTimer->getElapsedTimeInSeconds() << endl;
	CWinApp::OnIdle(lCount);

	switch(applicationState){

	case STATE_IDLE:
		Sleep(10);
		break;

	case STATE_RUN_START:
		StateRunStart();
		break;

	case STATE_RUN:
		StateRun();
		break;

	case STATE_RUN_END:
		StateRunEnd();
		break;

	default:
		cout << "===> Invalid appliation state" << endl;
		break;

	}

	return true;
}

void CPathPlannerApp::Draw(CDC *dc){
	
	if (!drawProgress){	
		cout << "Warning: CPathPlannerApp::Draw was called" <<endl;
	}

	if (planner != NULL)
		planner->Draw(dc);
}


void CPathPlannerApp::ResetSharedMembers(){
	cout << "CPathPlannerApp::ResetSharedMembers()" << endl;

	//--------- reset reusable variables
	PlannerNode::nodesConstructed = 0;
	PlannerNode::nodesDestructed  = 0;
	elapsedTime = 0;
	runCount = 0;
}


void CPathPlannerApp::StateRunStart(){
	cout << "CPathPlannerApp::StateRunStart()" << endl;

	pFrame->GetChildView()->ResetCollisionMap();	

			
	OnPlannerInitialize();	
	

	//tell the planner that we wanna start the planner  
	planner->PlanPath(initialX, initialY, goalX, goalY);


	// yield before starting the timer
	// final draw
	pFrame->GetChildView()->Invalidate(FALSE);
	cout << "CPathPlannerApp::OnRunStart. starting the timer" <<endl;	

	highResolutionTimer->reset();

	
	applicationState = STATE_RUN;
}


void CPathPlannerApp::StateRun(){
	//cout << "CPathPlannerApp::StateRun()" << endl;

	runCount++;
	planner->Run();	
	
	if (drawProgress){
		pFrame->GetChildView()->Invalidate(FALSE);
	}

	if (planner->IsDone()){
		applicationState = STATE_RUN_END;
	}
}


void CPathPlannerApp::StateRunEnd(){
	cout << "CPathPlannerApp::StateRunEnd()" << endl;
	cout << "CPathPlannerApp::StateRunEnd. planner is done. stoping the timer" <<endl;	

	elapsedTime = highResolutionTimer->getElapsedTimeInSeconds();
	cout << "Elapsed time: " << elapsedTime << endl;
	
	MessageBeep(MB_OK);


	// final draw
	pFrame->GetChildView()->Invalidate(FALSE);
	applicationState = STATE_IDLE;	
}


//this function initializes and runs the planner 
void CPathPlannerApp::OnRunStart() 
{
	cout << "CPathPlannerApp::OnRunStart()" << endl;

	if (applicationState == STATE_RUN){
		cout << "planner already running" << endl;
		return;
	}

	applicationState = STATE_RUN_START;
}



void CPathPlannerApp::OnRunStop() 
{
	cout << "CPathPlannerApp::OnRunStop" << endl;

	applicationState = STATE_RUN_END;
}


void CPathPlannerApp::OnRunPause() 
{
	MessageBox(m_hWnd, "Paused, click OK to continue", "CPathPlannerApp", MB_OK);
	
}

void CPathPlannerApp::OnPlannerReuse() 
{
	cout << "CPathPlannerApp::OnPlannerReuse()" << endl;

	planner->CleanUp();
	ResetSharedMembers();	
}

void CPathPlannerApp::OnPlannerInitialize() 
{
	cout << "CPathPlannerApp::OnPlannerCreate()" << endl;

	if(planner != NULL){
		OnPlannerReuse();
		return;
	}


	ResetSharedMembers();	


	switch(algorithmId){

	case AlgorithmId::ALGORITHM_BREADTH_FIRST:
		planner =  new PathPlannerBreadthFirst();
		break;

	case AlgorithmId::ALGORITHM_BEST_FIRST:
		planner =  new PathPlannerBestFirst();	
		break;

	case AlgorithmId::ALGORITHM_DIJKSTRA:
		planner =  new PathPlannerDijkstra();	
		break;

	case AlgorithmId::ALGORITHM_ASTAR:
		planner =  new PathPlannerAStar();	
		break;

	case AlgorithmId::ALGORITHM_ASTAR_OPTIMIZED:
		planner =  new PathPlannerAStarOptimized();	
		break;

	case AlgorithmId::ALGORITHM_ASTAR_NODE_MESH:
		planner =  new PathPlannerAStarNodeMesh();	
		break;

	default:
		planner = NULL;
		MessageBox(m_hWnd, "code segment not defined for algorithmId\n see CPathPlannerApp::OnPlannerInitialize()'s switch statement", "CPathPlannerApp", MB_OK);
		return;
	}
}

void CPathPlannerApp::OnPlannerDestroy() 
{
	if (planner!= NULL){
		delete planner;
		planner = NULL;
	}

	pFrame->GetChildView()->ResetCollisionMap();
	pFrame->GetChildView()->Invalidate(FALSE);

}

void CPathPlannerApp::OnPlannerSettings() 
{
	cout << "CPathPlannerApp::PlannerSettings()" << endl;

	if (planner == NULL){		
		OnPlannerInitialize();	
	}
	
	planner->Settings();
}

void CPathPlannerApp::OnPlannerInfo() 
{
	cout << "CPathPlannerApp::ShowInfo()" << endl;

	if (planner == NULL){		
		OnPlannerInitialize();	
	}

	planner->ShowInfo();
}

void CPathPlannerApp::OnFileOpen() 
{
	CFileDialog dialog( true, NULL, NULL, 0, NULL, pFrame);	

	if (dialog.DoModal() == IDOK){
		OnPlannerInitialize();
		SetCollisionMap(dialog.GetPathName().GetBuffer(dialog.GetPathName().GetLength()));
	}	
}

void CPathPlannerApp::OnDrawProgress() 
{
	drawProgress = !drawProgress;
}

void CPathPlannerApp::OnSettings() 
{
	cout << "CPathPlannerApp::OnSettings() " << endl;

	CSettingsDialog	dialog(pFrame);


	dialog.m_algorithm			= algorithmId;
	dialog.m_drawProgress		= drawProgress;
	dialog.m_ix					= initialX;
	dialog.m_iy					= initialY;
	dialog.m_gx					= goalX;
	dialog.m_gy					= goalY;
	dialog.m_timeSlice			= timeSlice;
	dialog.m_nodesConstructed	= PlannerNode::nodesConstructed;
	dialog.m_nodesDestructed	= PlannerNode::nodesDestructed;

	if (dialog.DoModal() == IDOK){

		if (applicationState == CPathPlannerApp::ApplicationState::STATE_RUN){
			cout << "WARNING: cannot change settings while planner is running" << endl;
			return;
		}

		drawProgress	= dialog.m_drawProgress? true: false;
		initialX		= dialog.m_ix;
		initialY		= dialog.m_iy;
		goalX			= dialog.m_gx;
		goalY			= dialog.m_gy;
		timeSlice		= dialog.m_timeSlice;

		if (dialog.m_algorithm != algorithmId){
			OnPlannerDestroy();
			algorithmId = dialog.m_algorithm;
		}

		OnPlannerInitialize();
	}

}

