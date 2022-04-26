import React from 'react'
import CIcon from '@coreui/icons-react'
import {
  cilBell,
  cilCalculator,
  cilChartPie,
  cilCloudUpload,
  cilCursor,
  cilDrop,
  cilFile,
  cilNotes,
  cilPencil,
  cilPuzzle,
  cilSpeedometer,
  cilStar,
} from '@coreui/icons'
import { CNavGroup, CNavItem, CNavTitle } from '@coreui/react'

const _nav = [
  {
    component: CNavTitle,
    name: 'Analysis',
  },
  {
    component: CNavItem,
    name: 'Upload Tally File',
    to: '/analysis/fileupload',
    icon: <CIcon icon={cilCloudUpload} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Analysis 1',
    to: '/analysis/analysis_1',
    icon: <CIcon icon={cilCalculator} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Analysis 2',
    to: '/analysis/analysis_2',
    icon: <CIcon icon={cilCalculator} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Analysis 3',
    to: '/analysis/analysis_3',
    icon: <CIcon icon={cilCalculator} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Analysis 4',
    to: '/analysis/analysis_4',
    icon: <CIcon icon={cilCalculator} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Analysis 5',
    to: '/analysis/analysis_5',
    icon: <CIcon icon={cilCalculator} customClassName="nav-icon" />,
  },
]

export default _nav
