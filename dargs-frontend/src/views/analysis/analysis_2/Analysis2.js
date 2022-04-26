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

const Analysis2 = () => {
  const [semesters, setSemesters] = useState([])
  const [yearSemesters, setSelectedYearSemesters] = useState([])
  const [studentCount, setStudentCount] = useState(20)
  const [analysis, setAnalysis] = useState([])

  useEffect(() => {
    const getAllData = async () => {
      const schools = await API.getAllSchools()
      const semesters = await API.getAllSemesters([])

      setSemesters(semesters)

      const apicalls = yearSemesters.map((sem) => API.getAnalysis(2, [], '', studentCount, sem))
      const selectedSemesterTabularData = await Promise.all(apicalls)
      setAnalysis(selectedSemesterTabularData)
    }

    getAllData()
  }, [yearSemesters, studentCount])

  return (
    <>
      <CCard className="mb-4">
        <CCardHeader>Input Panel | Analysis 2</CCardHeader>
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
          <CForm>
            <CFormInput
              label="Enrollment Count"
              placeholder="Enrollment count"
              defaultValue={20}
              onChange={(e) => setStudentCount(e.target.value)}
            />
          </CForm>
        </CCardBody>
      </CCard>
      {analysis.map(function (m, i) {
        return (
          <CCard key={i} className="mb-4">
            <CCardHeader>{`${m.semester} | Analysis 2 - Enrollment Analysis`}</CCardHeader>
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
    </>
  )
}

export default Analysis2
