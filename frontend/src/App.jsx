import React, {useState} from 'react'
import axios from 'axios'

export default function App(){
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)

  const onSubmit = async (e)=>{
    e.preventDefault()
    if(!file) return
    setLoading(true)
    try{
      const fd = new FormData()
      fd.append('file', file)
      const resp = await axios.post((import.meta.env.VITE_API_BASE || 'http://localhost:8080') + '/analyze', fd, { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([resp.data], {type: 'application/pdf'}))
      const a = document.createElement('a')
      a.href = url
      a.download = 'credit_report.pdf'
      document.body.appendChild(a)
      a.click()
      a.remove()
    }catch(err){
      alert('Error: ' + (err.message || err))
    }finally{setLoading(false)}
  }

  return (
    <div style={{padding:20}}>
      <h2>Smart Credit Analysis — OpenAI enhanced</h2>
      <form onSubmit={onSubmit}>
        <input type="file" accept="application/pdf,image/*" onChange={e=>setFile(e.target.files[0])} />
        <button type="submit" disabled={loading}>{loading ? 'Processing...' : 'Upload & Analyze'}</button>
      </form>
    </div>
  )
}
