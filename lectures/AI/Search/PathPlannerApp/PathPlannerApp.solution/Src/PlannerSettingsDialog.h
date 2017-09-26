/**
 *	Author: Syrus Mesdaghi, SyrusM@hotmail.com
 */
#if !defined(AFX_PLANNERSETTINGSDIALOG_H__7768C03F_7D55_4ACA_A3D9_0C6D00FAF5A5__INCLUDED_)
#define AFX_PLANNERSETTINGSDIALOG_H__7768C03F_7D55_4ACA_A3D9_0C6D00FAF5A5__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
// PlannerSettingsDialog.h : header file
//

/////////////////////////////////////////////////////////////////////////////
// CPlannerSettingsDialog dialog

class CPlannerSettingsDialog : public CDialog
{
// Construction
public:
	CPlannerSettingsDialog(CWnd* pParent = NULL);   // standard constructor

// Dialog Data
	//{{AFX_DATA(CPlannerSettingsDialog)
	enum { IDD = IDD_PLANNER_SETTINGS };
	int		m_closedHashTableSize;
	BOOL	m_diagonalPenalty;
	float	m_heuristicWeight;
	//}}AFX_DATA


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CPlannerSettingsDialog)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:

	// Generated message map functions
	//{{AFX_MSG(CPlannerSettingsDialog)
	afx_msg void OnCancelMode();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};
//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_PLANNERSETTINGSDIALOG_H__7768C03F_7D55_4ACA_A3D9_0C6D00FAF5A5__INCLUDED_)
