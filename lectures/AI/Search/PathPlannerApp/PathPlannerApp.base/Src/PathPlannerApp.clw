; CLW file contains information for the MFC ClassWizard

[General Info]
Version=1
LastClass=CSettingsDialog
LastTemplate=CDialog
NewFileInclude1=#include "stdafx.h"
NewFileInclude2=#include "PathPlannerApp.h"
LastPage=0

ClassCount=7
Class1=CPathPlannerApp
Class3=CMainFrame
Class4=CAboutDlg

ResourceCount=4
Resource1=IDR_MAINFRAME
Resource2=IDD_ABOUTBOX
Class2=CChildView
Class5=CSettingsDialog
Class6=CInfoDialog
Resource3=IDD_DIALOG_SETTINGS
Class7=CPlannerSettingsDialog
Resource4=IDD_PLANNER_SETTINGS

[CLS:CPathPlannerApp]
Type=0
HeaderFile=pathplannerapp.h
ImplementationFile=pathplannerapp.cpp
BaseClass=CWinApp
LastObject=CPathPlannerApp
Filter=N
VirtualFilter=AC

[CLS:CChildView]
Type=0
HeaderFile=ChildView.h
ImplementationFile=ChildView.cpp
Filter=N
LastObject=CChildView
BaseClass=CWnd 
VirtualFilter=WC

[CLS:CMainFrame]
Type=0
HeaderFile=MainFrm.h
ImplementationFile=MainFrm.cpp
Filter=T
LastObject=ID_DRAW_PROGRESS
BaseClass=CFrameWnd
VirtualFilter=fWC




[CLS:CAboutDlg]
Type=0
HeaderFile=PathPlannerApp.cpp
ImplementationFile=PathPlannerApp.cpp
Filter=D
LastObject=CAboutDlg

[DLG:IDD_ABOUTBOX]
Type=1
Class=CAboutDlg
ControlCount=6
Control1=IDC_STATIC,static,1342177283
Control2=IDC_STATIC,static,1342308480
Control3=IDC_STATIC,static,1342308352
Control4=IDC_STATIC,static,1342308352
Control5=IDC_STATIC,static,1342308352
Control6=IDOK,button,1342373889

[MNU:IDR_MAINFRAME]
Type=1
Class=CMainFrame
Command1=ID_FILE_OPEN
Command2=ID_APP_EXIT
Command3=ID_SETTINGS
Command4=ID_PLANNER_SETTINGS
Command5=ID_VIEW_ZOOM_2X
Command6=ID_VIEW_ZOOM_4X
Command7=ID_VIEW_ZOOM_8X
Command8=ID_VIEW_RESIZE
Command9=ID_PLANNER_INFO
Command10=ID_RUN_START
Command11=ID_RUN_STOP
Command12=ID_RUN_RESTART
Command13=ID_RUN_PAUSE
Command14=ID_APP_ABOUT
CommandCount=14

[ACL:IDR_MAINFRAME]
Type=1
Class=CMainFrame
Command1=ID_SETTINGS
Command2=ID_PLANNER_INITIALIZE
Command3=ID_PLANNER_DESTROY
Command4=ID_PLANNER_INFO
Command5=ID_FILE_OPEN
Command6=ID_RUN_PAUSE
Command7=ID_APP_EXIT
Command8=ID_RUN_START
Command9=ID_PLANNER_SETTINGS
Command10=ID_NEXT_PANE
Command11=ID_PREV_PANE
CommandCount=11

[TB:IDR_MAINFRAME]
Type=1
Class=?
Command1=ID_FILE_OPEN
Command2=ID_SETTINGS
Command3=ID_PLANNER_INITIALIZE
Command4=ID_PLANNER_DESTROY
Command5=ID_RUN_START
Command6=ID_RUN_PAUSE
Command7=ID_RUN_STOP
Command8=ID_RUN_RESTART
Command9=ID_PLANNER_SETTINGS
Command10=ID_PLANNER_INFO
Command11=ID_DRAW_PROGRESS
Command12=ID_APP_ABOUT
CommandCount=12

[CLS:CSettingsDialog]
Type=0
HeaderFile=SettingsDialog.h
ImplementationFile=SettingsDialog.cpp
BaseClass=CDialog
Filter=D
VirtualFilter=dWC
LastObject=CSettingsDialog

[CLS:CInfoDialog]
Type=0
HeaderFile=InfoDialog.h
ImplementationFile=InfoDialog.cpp
BaseClass=CDialog
Filter=D
LastObject=CInfoDialog
VirtualFilter=dWC

[DLG:IDD_DIALOG_SETTINGS]
Type=1
Class=CSettingsDialog
ControlCount=16
Control1=IDC_ALGORITHM,combobox,1344342083
Control2=IDC_IX,edit,1350631552
Control3=IDC_IY,edit,1350631552
Control4=IDC_GX,edit,1350631552
Control5=IDC_GY,edit,1350631552
Control6=IDC_TIME_SLICE,edit,1350631552
Control7=IDC_DRAW_PROGRESS,button,1342242819
Control8=IDOK,button,1342242817
Control9=IDCANCEL,button,1342242816
Control10=IDC_STATIC,static,1342308352
Control11=IDC_STATIC,static,1342308352
Control12=IDC_STATIC,static,1342308352
Control13=IDC_STATIC,static,1342308352
Control14=IDC_STATIC,static,1342308352
Control15=IDC_NODES_DESTRUCTED,edit,1350641792
Control16=IDC_NODES_CONSTRUCTED,edit,1350633604

[DLG:IDD_PLANNER_SETTINGS]
Type=1
Class=CPlannerSettingsDialog
ControlCount=7
Control1=IDC_HEURISTIC_WIGHT,edit,1350631552
Control2=IDC_CLOSED_HASHTABLE_SIZE,edit,1350631552
Control3=IDC_DIAGONAL_PENALTY,button,1342242819
Control4=IDOK,button,1342242817
Control5=IDCANCEL,button,1342242816
Control6=IDC_STATIC,static,1342308364
Control7=IDC_STATIC,static,1342308352

[CLS:CPlannerSettingsDialog]
Type=0
HeaderFile=PlannerSettingsDialog.h
ImplementationFile=PlannerSettingsDialog.cpp
BaseClass=CDialog
Filter=D
VirtualFilter=dWC
LastObject=CPlannerSettingsDialog

