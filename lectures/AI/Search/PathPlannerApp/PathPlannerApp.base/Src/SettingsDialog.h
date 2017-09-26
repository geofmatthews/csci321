/**
 *	Author: Syrus Mesdaghi, SyrusM@hotmail.com
 */
#if !defined(AFX_SETTINGSDIALOG_H__059CC9E8_8F5E_43E6_86C5_587C1839ECF1__INCLUDED_)
#define AFX_SETTINGSDIALOG_H__059CC9E8_8F5E_43E6_86C5_587C1839ECF1__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
// SettingsDialog.h : header file
//

/////////////////////////////////////////////////////////////////////////////
// CSettingsDialog dialog

class CSettingsDialog : public CDialog
{
// Construction
public:
	CSettingsDialog(CWnd* pParent = NULL);   // standard constructor

// Dialog Data
	//{{AFX_DATA(CSettingsDialog)
	enum { IDD = IDD_DIALOG_SETTINGS };
	int		m_algorithm;
	int		m_timeSlice;
	BOOL	m_drawProgress;
	int		m_gx;
	int		m_gy;
	int		m_ix;
	int		m_iy;
	int		m_nodesConstructed;
	int		m_nodesDestructed;
	//}}AFX_DATA


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CSettingsDialog)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:

	// Generated message map functions
	//{{AFX_MSG(CSettingsDialog)
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_SETTINGSDIALOG_H__059CC9E8_8F5E_43E6_86C5_587C1839ECF1__INCLUDED_)
