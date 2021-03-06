import PropTypes from 'prop-types'
import React, { useEffect, useState, createRef } from 'react'
import classNames from 'classnames'
import {
  CRow,
  CCol,
  CCard,
  CCardHeader,
  CCardBody,
  CFormSelect,
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableDataCell,
  CTableBody,
} from '@coreui/react'
import { CChart } from '@coreui/react-chartjs'
import { rgbToHex } from '@coreui/utils'
import { DocsLink } from 'src/components'
import API from '../../../api'
import mockdata from './mockdata'
import Select from 'react-select'

const transformTableData = (mockdata) => {
  const keys = Object.keys(mockdata.revenueTable)
  let transformed = []
  keys.forEach((key) => {
    transformed.push({
      semester: key,
      revenue: mockdata.revenueTable[key],
    })
  })
  return transformed
}

const Analysis1 = () => {
  const [chartData, setChartData] = useState({
    revenueTable: {},
    revenueChart: { columns: [], values: [] },
    revenueSummary: {},
    tableColumns: [],
  })
  const [schools, setSchools] = useState([])
  const [semesters, setSemesters] = useState([])
  const [schoolName, setSchoolName] = useState('')
  const [yearSemesters, setSelectedYearSemesters] = useState([])

  useEffect(() => {
    const getAllData = async () => {
      const analysis = await API.getAnalysis(1, yearSemesters, schoolName)
      const schools = await API.getAllSchools()
      const semesters = await API.getAllSemesters()
      setSchools(schools)
      setChartData(analysis)
      setSemesters(semesters)
    }

    getAllData()

    console.log(yearSemesters)
  }, [schoolName, yearSemesters])

  return (
    <>
      <CCard className="mb-4">
        <CCardHeader>Analysis 1</CCardHeader>
        <CCardBody>
          <h3 className="h5">Problem statement</h3>
          <p>Analysis of the revenue generated by a selected school in selected semester/s and the
            percentage change in the revenues of the school.</p>

          <p className="h5">Select Semesters</p>

          <Select
            isMulti={true}
            onChange={(values) => setSelectedYearSemesters(values.map((v) => v.value))}
            options={semesters.map((s) => ({
              value: `${s.Year}_${s.Semester_name}`,
              label: `${s.Year}_${s.Semester_name}`,
            }))}
          />

          <br />

          <p className="h5">School</p>
          <CFormSelect
            size="lg"
            aria-label="Multiple select example"
            onChange={(e) => setSchoolName(e.target.value)}
          >
            {schools.map((school) => (
              <option key={school.School_ID}>{school.School_name}</option>
            ))}
          </CFormSelect>

          <CChart
            type="line"
            data={{
              labels: chartData.revenueChart.columns,
              datasets: [
                {
                  label: `${schoolName} | Revenue vs Semester`,
                  backgroundColor: 'rgba(151, 187, 205, 0.2)',
                  borderColor: 'rgba(151, 187, 205, 1)',
                  pointBackgroundColor: 'rgba(151, 187, 205, 1)',
                  pointBorderColor: '#fff',
                  data: chartData.revenueChart.values,
                },
              ],
            }}
          />
          <br />
          <p className="h3">Revenue Data</p>
          <CTable>
            <CTableHead>
              <CTableRow>
                {chartData.tableColumns.map((column, index) => (
                  <CTableHeaderCell scole="col" key={column}>
                    {column}
                  </CTableHeaderCell>
                ))}
              </CTableRow>
            </CTableHead>
            <CTableBody>
              {transformTableData(chartData).map((row, index) => (
                <CTableRow key={index}>
                  <CTableHeaderCell scope="row">{row.semester}</CTableHeaderCell>
                  {row.revenue.map((r, k) => (
                    <CTableDataCell key={k}>{r.Revenue}</CTableDataCell>
                  ))}
                  <CTableDataCell>{Object.values(chartData.revenueSummary)[index]}</CTableDataCell>
                </CTableRow>
              ))}
            </CTableBody>
          </CTable>
        </CCardBody>
      </CCard>
    </>
  )
}

export default Analysis1
