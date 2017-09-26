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

// ChildView.h : interface of the CChildView class
//
/////////////////////////////////////////////////////////////////////////////

#if !defined(AFX_CHILDVIEW_H__9AE4027F_5BB4_4B6D_A6C3_3447A6555AAD__INCLUDED_)
#define AFX_CHILDVIEW_H__9AE4027F_5BB4_4B6D_A6C3_3447A6555AAD__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

/////////////////////////////////////////////////////////////////////////////
// CChildView window

class CChildView : public CWnd
{
// Construction
public:
	CChildView();

// Attributes
public:

	HBITMAP		collisionMap,			// bitmap that contains the collisionmap
				collisionMapCopy;

	CDC			cdcCollisionMap,
				cdcCollisionMapCopy;	// device context used to select the collision bitmap 

	int			mapZoom;


// Operations
public:

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CChildView)
	public:
	virtual BOOL Create(LPCTSTR lpszClassName, LPCTSTR lpszWindowName, DWORD dwStyle, const RECT& rect, CWnd* pParentWnd, UINT nID, CCreateContext* pContext = NULL);
	protected:
	virtual BOOL PreCreateWindow(CREATESTRUCT& cs);
	//}}AFX_VIRTUAL

// Implementation
public:
	virtual ~CChildView();
	void LoadCollisionMap();			//loads image for drawing and creats/sets appropriate dc s
	void ReleaseCollisionMap();			//loads image for drawing and creats/sets appropriate dc s
	void ResetCollisionMap();
	// Generated message map functions
protected:
	//{{AFX_MSG(CChildView)
	afx_msg void OnPaint();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_CHILDVIEW_H__9AE4027F_5BB4_4B6D_A6C3_3447A6555AAD__INCLUDED_)
