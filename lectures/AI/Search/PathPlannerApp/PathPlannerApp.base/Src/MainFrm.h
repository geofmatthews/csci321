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
 *  November 2002
 */


// MainFrm.h : interface of the CMainFrame class
//
/////////////////////////////////////////////////////////////////////////////

#if !defined(AFX_MAINFRM_H__E47349F4_D5BA_4D87_932D_476953912934__INCLUDED_)
#define AFX_MAINFRM_H__E47349F4_D5BA_4D87_932D_476953912934__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include "ChildView.h"

class CMainFrame : public CFrameWnd
{
	
public:
	CMainFrame();
protected: 
	DECLARE_DYNAMIC(CMainFrame)

// Attributes
public:

// Operations
public:

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CMainFrame)
	virtual BOOL PreCreateWindow(CREATESTRUCT& cs);
	virtual BOOL OnCmdMsg(UINT nID, int nCode, void* pExtra, AFX_CMDHANDLERINFO* pHandlerInfo);
	//}}AFX_VIRTUAL

// Implementation
public:
	virtual ~CMainFrame();
	
	CChildView*	GetChildView(){
		return &m_wndView;
	}	

#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:  // control bar embedded members
	CStatusBar  m_wndStatusBar;
	CToolBar    m_wndToolBar;
	CChildView    m_wndView;

// Generated message map functions
protected:
	//{{AFX_MSG(CMainFrame)
	afx_msg int OnCreate(LPCREATESTRUCT lpCreateStruct);
	afx_msg void OnSetFocus(CWnd *pOldWnd);
	afx_msg void OnAppAbout();
	afx_msg void OnViewZoom2x();
	afx_msg void OnViewZoom4x();
	afx_msg void OnViewZoom8x();
	afx_msg void OnViewToolbar();
	afx_msg void OnUpdateDrawProgress(CCmdUI* pCmdUI);
	afx_msg void OnUpdateRunStart(CCmdUI* pCmdUI);
	afx_msg void OnUpdateRunStop(CCmdUI* pCmdUI);
	afx_msg void OnUpdateRunPause(CCmdUI* pCmdUI);
	afx_msg void OnUpdateSettings(CCmdUI* pCmdUI);
	afx_msg void OnUpdatePlannerSettings(CCmdUI* pCmdUI);
	afx_msg void OnUpdatePlannerInitialize(CCmdUI* pCmdUI);
	afx_msg void OnUpdatePlannerDestroy(CCmdUI* pCmdUI);
	afx_msg void OnUpdatePlannerInfo(CCmdUI* pCmdUI);
	afx_msg void OnViewStatusBar();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()

public:
	afx_msg void OnViewResize();
	afx_msg void OnOptionsSettings();

};

/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_MAINFRM_H__E47349F4_D5BA_4D87_932D_476953912934__INCLUDED_)
