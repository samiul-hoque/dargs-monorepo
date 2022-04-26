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
  CSpinner,
  CFormInput,
  CForm,
} from '@coreui/react'
import { CChart } from '@coreui/react-chartjs'
import { rgbToHex } from '@coreui/utils'
import { DocsLink } from 'src/components'
import API from '../../../api'
import Select from 'react-select'
import mockdata from './mockdata'

const Analysis4 = () => {
  const [semesters, setSemesters] = useState([])
  const [sizeRanges, setSizeRanges] = useState({ ranges: [] })
  const [selectedRanges, setSelectedRanges] = useState([])
  const [yearSemesters, setSelectedYearSemesters] = useState([])
  const [analysis, setAnalysis] = useState([])
  const [analysis6, setAnalysis6] = useState({ columns: [], tabularData: [] })

  useEffect(() => {
    const getAllData = async () => {
      const semesters = await API.getAllSemesters([])
      const _sizeRanges = await API.getSizeRangeOptions(5)
      // const analysis4 = await API.getAnalysis(4, yearSemesters, '', 0, )
      const apicalls = yearSemesters.map((yearSemester) =>
        API.getAnalysis(5, [], '', 0, yearSemester, selectedRanges),
      )
      const apicallData = await Promise.all(apicalls)

      const analysis6data = await API.getAnalysis(6)

      setSemesters(semesters)
      setAnalysis(apicallData)
      setAnalysis6(analysis6data)
      setSizeRanges(_sizeRanges)
    }

    getAllData()
  }, [yearSemesters, selectedRanges])

  return (
    <>
      <CCard className="mb-4">
        <CCardHeader>Input Panel | Analysis 5</CCardHeader>
        <CCardBody>
          <h3 className="h5">Problem statement</h3>
          <p>Problem statement goes here</p>
          <Select
            isMulti={true}
            onChange={(values) => setSelectedYearSemesters(values.map((v) => v.value))}
            options={semesters.map((s) => ({
              value: `${s.Year}_${s.Semester_name}`,
              label: `${s.Year}_${s.Semester_name}`,
            }))}
          />
          <Select
            isMulti={true}
            onChange={(values) => setSelectedRanges(values.map((v) => v.value))}
            options={sizeRanges?.ranges.map((s) => ({
              value: s,
              label: s,
            }))}
          />
        </CCardBody>
      </CCard>

      {analysis.map(function (m, i) {
        return (
          <CCard key={i} className="mb-4">
            <CCardHeader>{`${m.semester} | Analysis 4`}</CCardHeader>
            <CCardBody>
              <CTable>
                <CTableHead>
                  <CTableRow>
                    {m.columns.map((c) => (
                      <CTableHeaderCell key={c}>{c}</CTableHeaderCell>
                    ))}
                  </CTableRow>
                </CTableHead>
                <CTableBody>
                  {m.tabularData.map((td, index) => (
                    <CTableRow key={index}>
                      {Object.values(td).map((datacell, cellindex) => (
                        <CTableDataCell key={`${index}-${cellindex}`}>{datacell}</CTableDataCell>
                      ))}
                    </CTableRow>
                  ))}
                </CTableBody>
              </CTable>
            </CCardBody>
          </CCard>
        )
      })}

      <CCard className="mb-4">
        <CCardHeader>{`Analysis 5`}</CCardHeader>
        <CCardBody>
          <CTable>
            <CTableHead>
              <CTableRow>
                {analysis6.columns.map((c) => (
                  <CTableHeaderCell key={c}>{c}</CTableHeaderCell>
                ))}
              </CTableRow>
            </CTableHead>
            <CTableBody>
              {analysis6.tabularData.map((td, index) => (
                <CTableRow key={index}>
                  {Object.values(td).map((datacell, cellindex) => (
                    <CTableDataCell key={`${index}-${cellindex}`}>{datacell}</CTableDataCell>
                  ))}
                </CTableRow>
              ))}
            </CTableBody>
          </CTable>
        </CCardBody>
      </CCard>
    </>
  )
}

export default Analysis4
