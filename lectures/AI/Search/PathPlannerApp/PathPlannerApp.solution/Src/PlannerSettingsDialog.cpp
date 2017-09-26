// PlannerSettingsDialog.cpp : implementation file
//

#include "stdafx.h"
#include "PathPlannerApp.h"
#include "PlannerSettingsDialog.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// PlannerSettingsDialog message handlers
/////////////////////////////////////////////////////////////////////////////
// CPlannerSettingsDialog dialog


CPlannerSettingsDialog::CPlannerSettingsDialog(CWnd* pParent /*=NULL*/)
	: CDialog(CPlannerSettingsDialog::IDD, pParent)
{
	//{{AFX_DATA_INIT(CPlannerSettingsDialog)
	m_closedHashTableSize = 0;
	m_diagonalPenalty = FALSE;
	m_heuristicWeight = 0.0f;
	//}}AFX_DATA_INIT
}


void CPlannerSettingsDialog::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CPlannerSettingsDialog)
	DDX_Text(pDX, IDC_CLOSED_HASHTABLE_SIZE, m_closedHashTableSize);
	DDX_Check(pDX, IDC_DIAGONAL_PENALTY, m_diagonalPenalty);
	DDX_Text(pDX, IDC_HEURISTIC_WIGHT, m_heuristicWeight);
	//}}AFX_DATA_MAP
}


BEGIN_MESSAGE_MAP(CPlannerSettingsDialog, CDialog)
	//{{AFX_MSG_MAP(CPlannerSettingsDialog)
	ON_WM_CANCELMODE()
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CPlannerSettingsDialog message handlers

void CPlannerSettingsDialog::OnCancelMode() 
{
	CDialog::OnCancelMode();
	
	// TODO: Add your message handler code here
	
}
