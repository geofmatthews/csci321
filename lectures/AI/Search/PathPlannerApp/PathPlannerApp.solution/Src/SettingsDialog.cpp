// SettingsDialog.cpp : implementation file
//

#include "stdafx.h"
#include "PathPlannerApp.h"
#include "SettingsDialog.h"

#include <iostream>
using namespace std;

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CSettingsDialog dialog


CSettingsDialog::CSettingsDialog(CWnd* pParent /*=NULL*/)
	: CDialog(CSettingsDialog::IDD, pParent)
{
	//{{AFX_DATA_INIT(CSettingsDialog)
	m_algorithm = -1;
	m_timeSlice = 0;
	m_drawProgress = FALSE;
	m_gx = 0;
	m_gy = 0;
	m_ix = 0;
	m_iy = 0;
	m_nodesConstructed = 0;
	m_nodesDestructed = 0;
	//}}AFX_DATA_INIT
}


void CSettingsDialog::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CSettingsDialog)
	DDX_CBIndex(pDX, IDC_ALGORITHM, m_algorithm);
	DDX_Text(pDX, IDC_TIME_SLICE, m_timeSlice);
	DDX_Check(pDX, IDC_DRAW_PROGRESS, m_drawProgress);
	DDX_Text(pDX, IDC_GX, m_gx);
	DDX_Text(pDX, IDC_GY, m_gy);
	DDX_Text(pDX, IDC_IX, m_ix);
	DDX_Text(pDX, IDC_IY, m_iy);
	DDX_Text(pDX, IDC_NODES_CONSTRUCTED, m_nodesConstructed);
	DDX_Text(pDX, IDC_NODES_DESTRUCTED, m_nodesDestructed);
	//}}AFX_DATA_MAP
}


BEGIN_MESSAGE_MAP(CSettingsDialog, CDialog)
	//{{AFX_MSG_MAP(CSettingsDialog)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CSettingsDialog message handlers
