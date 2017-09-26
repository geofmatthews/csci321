// ChildView.cpp : implementation of the CChildView class
//


#include "stdafx.h"
#include "PathPlannerApp.h"
#include "ChildView.h"

#include <iostream>
using namespace std;

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CChildView

CChildView::CChildView()
{
	cout << "CChildView::CChildView" << endl;

	mapZoom = 4;
	collisionMap = NULL;
	collisionMapCopy = NULL;
}

CChildView::~CChildView()
{
	ReleaseCollisionMap();
	cout << "CChildView::~CChildView()" << endl;
}


BEGIN_MESSAGE_MAP(CChildView,CWnd )
	//{{AFX_MSG_MAP(CChildView)
	ON_WM_PAINT()
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()


/////////////////////////////////////////////////////////////////////////////
// CChildView message handlers

BOOL CChildView::PreCreateWindow(CREATESTRUCT& cs) 
{
	if (!CWnd::PreCreateWindow(cs))
		return FALSE;

	cs.dwExStyle |= WS_EX_CLIENTEDGE;
	cs.style &= ~WS_BORDER;
	cs.lpszClass = AfxRegisterWndClass(CS_HREDRAW|CS_VREDRAW|CS_DBLCLKS, 
		::LoadCursor(NULL, IDC_ARROW), HBRUSH(COLOR_WINDOW+1), NULL);

	return TRUE;
}


BOOL CChildView::Create(LPCTSTR lpszClassName, LPCTSTR lpszWindowName, DWORD dwStyle, const RECT& rect, CWnd* pParentWnd, UINT nID, CCreateContext* pContext) 
{
	BOOL rValue = CWnd::Create(lpszClassName, lpszWindowName, dwStyle, rect, pParentWnd, nID, pContext);
	
	CPaintDC dc(this);
	dc.SetStretchBltMode(COLORONCOLOR);
	cdcCollisionMap.CreateCompatibleDC(&dc);
	cdcCollisionMapCopy.CreateCompatibleDC(&dc);

	return rValue;
}

void CChildView::LoadCollisionMap(){
	cout << "void CChildView::LoadCollisionMap()" <<endl;
	
	ReleaseCollisionMap();


	/**
	 *  load a device dependent copy of the bitmap which will be shown to the user
	 */
	collisionMap		= (HBITMAP)LoadImage(NULL, CPathPlannerApp::instance->collisionMapFilename,IMAGE_BITMAP,CPathPlannerApp::instance->collisionMapWidth, CPathPlannerApp::instance->collisionMapHeight, LR_LOADFROMFILE);
	collisionMapCopy	= (HBITMAP)CopyImage(collisionMap, IMAGE_BITMAP, CPathPlannerApp::instance->collisionMapWidth, CPathPlannerApp::instance->collisionMapHeight, LR_COPYRETURNORG);

	cdcCollisionMap.SelectObject(collisionMap);	
	cdcCollisionMapCopy.SelectObject(collisionMapCopy);	


	Invalidate(FALSE);
}

void CChildView::ReleaseCollisionMap(){
	cout << "void CChildView::ReleaseCollisionMap()" <<endl;

	if (collisionMap)
		DeleteObject(collisionMap);

	if (collisionMapCopy)
		DeleteObject(collisionMapCopy);
}



void CChildView::OnPaint() 
{
	//cout << "void CChildView::OnPaint() " <<endl;
	
	ResetCollisionMap();
	

	// allow application to draw on top of it (this is the back buffer)
	CPathPlannerApp::instance->Draw(&cdcCollisionMapCopy);	

	CPaintDC dc(this); // device context for painting
	
	// flip to front
	dc.StretchBlt(
	  0,						// x-coordinate of upper-left corner of dest. rectangle
	  0,						// y-coordinate of upper-left corner of dest. rectangle
	  CPathPlannerApp::instance->collisionMapWidth * mapZoom,	// width of destination rectangle
	  CPathPlannerApp::instance->collisionMapHeight * mapZoom,	// height of destination rectangle
	  &cdcCollisionMapCopy,			// handle to source device context
	  0,						// x-coordinate of upper-left corner of source rectangle
	  0,						// y-coordinate of upper-left corner of source rectangle
	  CPathPlannerApp::instance->collisionMapWidth,				// width of source rectangle
	  CPathPlannerApp::instance->collisionMapHeight,				// height of source rectangle
	  SRCCOPY					// raster operation code
	);
}

void CChildView::ResetCollisionMap(){
	// reset cdcCollisionMapCopy to original image
	cdcCollisionMapCopy.BitBlt(
	  0,						// x-coordinate of upper-left corner of dest. rectangle
	  0,						// y-coordinate of upper-left corner of dest. rectangle
	  CPathPlannerApp::instance->collisionMapWidth,		// width of destination rectangle
	  CPathPlannerApp::instance->collisionMapHeight,	// height of destination rectangle
	  &cdcCollisionMap,			// handle to source device context
	  0,						// x-coordinate of upper-left corner of source rectangle
	  0,						// y-coordinate of upper-left corner of source rectangle
	  SRCCOPY					// raster operation code
	);
}
