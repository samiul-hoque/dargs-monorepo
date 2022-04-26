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
  CFormLabel,
  CButton,
} from '@coreui/react'
import { CChart } from '@coreui/react-chartjs'
import { rgbToHex } from '@coreui/utils'
import { DocsLink } from 'src/components'
import API from '../../../api'
import Select from 'react-select'
import mockdata from './mockdata'

import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(new File([], ''))
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const getAllData = async () => {}

    console.log(selectedFile)
    getAllData()
  }, [selectedFile])

  return (
    <>
      {!loading && (
        <CCard className="mb-4">
          <CCardHeader>File Upload and Reset</CCardHeader>
          <CCardBody>
            <CForm className="row g-3">
              <CCol xs="auto">
                <CFormInput type="file" onChange={(e) => setSelectedFile(e.target.files[0])} />
              </CCol>
              <CCol xs="auto">
                <CButton
                  type="submit"
                  className="mb-3"
                  onClick={async (e) => {
                    e.preventDefault()
                    setLoading(true)
                    await API.uploadFile(selectedFile)
                    setLoading(false)
                    toast('File uploaded successfully')
                  }}
                >
                  Upload
                </CButton>
                <ToastContainer />
              </CCol>
            </CForm>
            {!loading && (
              <CForm>
                <CButton
                  color="danger"
                  onClick={async (e) => {
                    e.preventDefault()
                    setLoading(true)
                    await API.clearDatabase()
                    setLoading(false)
                    toast('Database cleared successfully')
                  }}
                >
                  Clear Database
                </CButton>
                <ToastContainer />
              </CForm>
            )}
          </CCardBody>
        </CCard>
      )}
      {loading && <CSpinner></CSpinner>}
    </>
  )
}

export default FileUpload
