import axios from 'axios'

const backendUrl = `${document.location.protocol}//${document.location.hostname}:8000`

export default axios.create({
  baseURL: backendUrl + '/api/v1'
})