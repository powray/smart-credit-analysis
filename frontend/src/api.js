import axios from 'axios'
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080'
export async function uploadStatement(file){
  const fd = new FormData();
  fd.append('file', file)
  const resp = await axios.post(`${API_BASE}/analyze`, fd, { responseType: 'blob' })
  return resp.data
}
