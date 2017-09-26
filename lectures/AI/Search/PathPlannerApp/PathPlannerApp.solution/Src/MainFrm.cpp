// MainFrm.cpp : implementation of the CMainFrame class
//

#include "stdafx.h"
#include "PathPlannerApp.h"
#include "PlannerNode.h"

#include "MainFrm.h"
//#include "InfoDialog.h"

#include <iostream>
using namespace std;

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CAboutDlg dialog used for App About

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();

// Dialog Data
	//{{AFX_DATA(CAboutDlg)
	enum { IDD = IDD_ABOUTBOX };
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CAboutDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	//{{AFX_MSG(CAboutDlg)
		// No message handlers
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
	//{{AFX_DATA_INIT(CAboutDlg)
	//}}AFX_DATA_INIT
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CAboutDlg)
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
	//{{AFX_MSG_MAP(CAboutDlg)
		// No message handlers
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()



/////////////////////////////////////////////////////////////////////////////
// CMainFrame

IMPLEMENT_DYNAMIC(CMainFrame, CFrameWnd)

BEGIN_MESSAGE_MAP(CMainFrame, CFrameWnd)
	//{{AFX_MSG_MAP(CMainFrame)
	ON_WM_CREATE()
	ON_WM_SETFOCUS()
	ON_COMMAND(ID_APP_ABOUT, OnAppAbout)
	ON_COMMAND(ID_VIEW_ZOOM_2X, OnViewZoom2x)
	ON_COMMAND(ID_VIEW_ZOOM_4X, OnViewZoom4x)
	ON_COMMAND(ID_VIEW_ZOOM_8X, OnViewZoom8x)
	ON_COMMAND(ID_VIEW_TOOLBAR, OnViewToolbar)
	ON_UPDATE_COMMAND_UI(ID_DRAW_PROGRESS, OnUpdateDrawProgress)
	ON_UPDATE_COMMAND_UI(ID_RUN_START, OnUpdateRunStart)
	ON_UPDATE_COMMAND_UI(ID_RUN_STOP, OnUpdateRunStop)
	ON_UPDATE_COMMAND_UI(ID_RUN_PAUSE, OnUpdateRunPause)
	ON_UPDATE_COMMAND_UI(ID_SETTINGS, OnUpdateSettings)
	ON_UPDATE_COMMAND_UI(ID_PLANNER_SETTINGS, OnUpdatePlannerSettings)
	ON_UPDATE_COMMAND_UI(ID_PLANNER_INITIALIZE, OnUpdatePlannerInitialize)
	ON_UPDATE_COMMAND_UI(ID_PLANNER_DESTROY, OnUpdatePlannerDestroy)
	ON_UPDATE_COMMAND_UI(ID_PLANNER_INFO, OnUpdatePlannerInfo)
	ON_COMMAND(ID_VIEW_STATUS_BAR, OnViewStatusBar)
	ON_COMMAND(ID_VIEW_RESIZE, OnViewResize)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

static UINT indicators[] =
{
	ID_SEPARATOR,           // status line indicator
	ID_INDICATOR_CAPS,
	ID_INDICATOR_NUM,
	ID_INDICATOR_SCRL,
};

/////////////////////////////////////////////////////////////////////////////
// CMainFrame construction/destruction

CMainFrame::CMainFrame()
{
}

CMainFrame::~CMainFrame()
{
	cout << "CMainFrame::~CMainFrame()" << endl;
}

int CMainFrame::OnCreate(LPCREATESTRUCT lpCreateStruct)
{
	if (CFrameWnd::OnCreate(lpCreateStruct) == -1)
		return -1;
	// create a view to occupy the client area of the frame
	if (!m_wndView.Create(NULL, NULL, AFX_WS_DEFAULT_VIEW,
		CRect(0, 0, 0, 0), this, AFX_IDW_PANE_FIRST, NULL))
	{
		TRACE0("Failed to create view window\n");
		return -1;
	}

	SetIcon(CPathPlannerApp::instance->LoadIcon(IDR_MAINFRAME), TRUE);

	//ToolBar and Status Bar	
	if (!m_wndToolBar.CreateEx(this, TBSTYLE_FLAT, WS_CHILD | WS_VISIBLE | CBRS_TOP
		| CBRS_GRIPPER | CBRS_TOOLTIPS | CBRS_FLYBY | CBRS_SIZE_DYNAMIC) ||
		!m_wndToolBar.LoadToolBar(IDR_MAINFRAME))
	{
		TRACE0("Failed to create toolbar\n");
		return -1;      // fail to create
	}

	if (!m_wndStatusBar.Create(this) ||
		!m_wndStatusBar.SetIndicators(indicators,
		  sizeof(indicators)/sizeof(UINT)))
	{
		TRACE0("Failed to create status bar\n");
		return -1;      // fail to create
	}

/*	// TODO: Delete these three lines if you don't want the toolbar to
	//  be dockable
	m_wndToolBar.EnableDocking(CBRS_ALIGN_ANY);
	EnableDocking(CBRS_ALIGN_ANY);
	DockControlBar(&m_wndToolBar);
*/
	return 0;
}

BOOL CMainFrame::PreCreateWindow(CREATESTRUCT& cs)
{
	if( !CFrameWnd::PreCreateWindow(cs) )
		return FALSE;
	// TODO: Modify the Window class or styles here by modifying
	//  the CREATESTRUCT cs

	cs.dwExStyle &= ~WS_EX_CLIENTEDGE;
	cs.lpszClass = AfxRegisterWndClass(0);
	cs.cx = 200;
	cs.cy = 200;
	return TRUE;
}

/////////////////////////////////////////////////////////////////////////////
// CMainFrame diagnostics

#ifdef _DEBUG
void CMainFrame::AssertValid() const
{
	CFrameWnd::AssertValid();
}

void CMainFrame::Dump(CDumpContext& dc) const
{
	CFrameWnd::Dump(dc);
}

#endif //_DEBUG

/////////////////////////////////////////////////////////////////////////////
// CMainFrame message handlers
void CMainFrame::OnSetFocus(CWnd* pOldWnd)
{
	// forward focus to the view window
	m_wndView.SetFocus();
}

BOOL CMainFrame::OnCmdMsg(UINT nID, int nCode, void* pExtra, AFX_CMDHANDLERINFO* pHandlerInfo)
{
	// let the view have first crack at the command
	if (m_wndView.OnCmdMsg(nID, nCode, pExtra, pHandlerInfo))
		return TRUE;

	// otherwise, do default handling
	return CFrameWnd::OnCmdMsg(nID, nCode, pExtra, pHandlerInfo);
}

// App command to run the dialog
void CMainFrame::OnAppAbout() 
{
	CAboutDlg aboutDlg;
	aboutDlg.DoModal();	
}



void CMainFrame::OnViewResize() 
{

	CRect rectTemp(0,0, CPathPlannerApp::instance->collisionMapWidth * GetChildView()->mapZoom, CPathPlannerApp::instance->collisionMapHeight * GetChildView()->mapZoom);
	

	//cout << "rectTemp:  " << rectTemp.left << ", " << rectTemp.top << " ," << rectTemp.right << ", " << rectTemp.bottom << endl;

	LONG currentStyle = GetWindowLong(m_hWnd, GWL_STYLE);
	LONG currentStyleEx = GetWindowLong(m_hWnd, GWL_EXSTYLE);
	
	
	AdjustWindowRectEx(&rectTemp, currentStyle, TRUE, currentStyleEx);

	rectTemp.right += 4; // hardcoded offset to compensate for error
	rectTemp.bottom += 47; // hardcoded offset to compensate for toolBar and statusBar

	//cout << "rectTemp:  " << rectTemp.left << ", " << rectTemp.top << " ," << rectTemp.right << ", " << rectTemp.bottom << endl;

	CRect rectWindow;
	GetWindowRect(&rectWindow);

	SetWindowPos(NULL, rectWindow.left, rectWindow.top, rectTemp.Width(), rectTemp.Height(), 0 );
}


void CMainFrame::OnViewZoom2x()
{
	GetChildView()->mapZoom	= 2;
	OnViewResize();
}

void CMainFrame::OnViewZoom4x() 
{
	GetChildView()->mapZoom	= 4;
	OnViewResize();
}

void CMainFrame::OnViewZoom8x() 
{
	GetChildView()->mapZoom	= 8;
	OnViewResize();
}


void CMainFrame::OnViewToolbar() 
{
	if (m_wndToolBar.IsVisible()){
		m_wndToolBar.ShowWindow(SW_HIDE);
	}else{
		m_wndToolBar.ShowWindow(SW_SHOW);
	}

	OnViewResize();
}


void CMainFrame::OnViewStatusBar() 
{
	if (m_wndStatusBar.IsVisible()){
		m_wndStatusBar.ShowWindow(SW_HIDE);
	}else{
		m_wndStatusBar.ShowWindow(SW_SHOW);
	}

	OnViewResize();
}

void CMainFrame::OnUpdateDrawProgress(CCmdUI* pCmdUI) 
{
	pCmdUI->SetCheck(CPathPlannerApp::instance->drawProgress?1:0);
}

void CMainFrame::OnUpdateRunStart(CCmdUI* pCmdUI) 
{
	bool run = CPathPlannerApp::instance->planner && (CPathPlannerApp::instance->applicationState == CPathPlannerApp::ApplicationState::STATE_RUN);
	pCmdUI->Enable(run?0:1);
}

void CMainFrame::OnUpdateRunStop(CCmdUI* pCmdUI) 
{
	bool run = (CPathPlannerApp::instance->applicationState == CPathPlannerApp::ApplicationState::STATE_RUN);
	pCmdUI->Enable(run?1:0);
}

void CMainFrame::OnUpdateRunPause(CCmdUI* pCmdUI) 
{
	bool run = (CPathPlannerApp::instance->applicationState == CPathPlannerApp::ApplicationState::STATE_RUN);
	pCmdUI->Enable(run?1:0);
}

void CMainFrame::OnUpdateSettings(CCmdUI* pCmdUI) 
{
	bool run = (CPathPlannerApp::instance->applicationState == CPathPlannerApp::ApplicationState::STATE_RUN);
	pCmdUI->Enable(run?0:1);
}

void CMainFrame::OnUpdatePlannerInitialize(CCmdUI* pCmdUI) 
{
	pCmdUI->Enable(CPathPlannerApp::instance->planner?0:1);
}

void CMainFrame::OnUpdatePlannerDestroy(CCmdUI* pCmdUI) 
{
	bool enable = CPathPlannerApp::instance->planner && (CPathPlannerApp::instance->applicationState != CPathPlannerApp::ApplicationState::STATE_RUN);
	pCmdUI->Enable(enable?1:0);
}

void CMainFrame::OnUpdatePlannerSettings(CCmdUI* pCmdUI) 
{
	bool enable = CPathPlannerApp::instance->planner && (CPathPlannerApp::instance->applicationState != CPathPlannerApp::ApplicationState::STATE_RUN);
	pCmdUI->Enable(enable?1:0);
}

void CMainFrame::OnUpdatePlannerInfo(CCmdUI* pCmdUI) 
{
	pCmdUI->Enable(CPathPlannerApp::instance->planner?1:0);
}
