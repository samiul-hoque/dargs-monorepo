import axios from 'axios'

const APIClient = axios.create({
  baseURL: 'http://localhost:8000/dargs',
})

export default {
  getAnalysis: (
    analysisId,
    semesters = [],
    school = '',
    students = 0,
    year_semester = '',
    sizeRanges = [],
  ) => {
    let sem = ''
    let szs = ''

    for (let i = 0; i < semesters.length; i++) {
      if (i === semesters.length - 1) sem += semesters[i]
      else sem += semesters[i] + ','
    }

    for (let i = 0; i < sizeRanges.length; i++) {
      if (i === sizeRanges.length - 1) szs += sizeRanges[i]
      else szs += sizeRanges[i] + ','
    }

    console.log({ sem })

    if (analysisId === 1) {
      return APIClient.get(`/analysis/${analysisId}?semesters=${semesters}&school=${school}`)
        .then((response) => response.data)
        .catch((response) => response.error)
    } else if (analysisId === 2) {
      return APIClient.get(
        `/analysis/${analysisId}?year_semester=${year_semester}&max_enrolled=${students}`,
      )
        .then((response) => response.data)
        .catch((response) => response.error)
    } else if (analysisId === 3) {
      return APIClient.get(`/analysis/${analysisId}?semester=${year_semester}`)
        .then((response) => response.data)
        .catch((response) => response.error)
    } else if (analysisId === 4 || analysisId === 5) {
      return APIClient.get(`/analysis/${analysisId}?semester=${year_semester}&ranges=${szs}`)
        .then((response) => response.data)
        .catch((response) => response.error)
    } else if (analysisId === 6) {
      return APIClient.get(`/analysis/${analysisId}`)
        .then((response) => response.data)
        .catch((response) => response.error)
    }
  },

  getAllSchools: () => {
    return APIClient.get(`/school`)
      .then((response) => response.data)
      .catch((e) => e.error)
  },

  getAllSemesters: () => {
    return APIClient.get(`/semester`)
      .then((response) => response.data)
      .catch((e) => e.error)
  },

  getSizeRangeOptions: (analysis) => {
    return APIClient.get(`/size?analysis=${analysis}`)
      .then((response) => response.data)
      .catch((e) => e.error)
  },

  uploadFile: (file) => {
    let formData = new FormData()
    formData.append('file', file)

    return APIClient.post(`/upload/${file.name}`, formData)
      .then((response) => response.data)
      .catch((response) => response.error)
  },

  clearDatabase: () => {
    return APIClient.delete('/clear')
      .then((response) => response.data)
      .catch((response) => response.error)
  },
}
