import { useState } from 'react'
import { motion } from 'framer-motion'
import { Upload, FileText, X, CheckCircle, AlertCircle, Loader } from 'lucide-react'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1'

export default function DocumentUpload() {
  const [file, setFile] = useState(null)
  const [questions, setQuestions] = useState('')
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0])
    }
  }

  const handleFileSelect = (selectedFile) => {
    const allowedTypes = ['.pdf', '.docx', '.txt', '.md']
    const fileExt = '.' + selectedFile.name.split('.').pop().toLowerCase()
    
    if (!allowedTypes.includes(fileExt)) {
      setMessage({ type: 'error', text: 'Invalid file type. Please upload PDF, DOCX, TXT, or MD files.' })
      return
    }

    if (selectedFile.size > 50 * 1024 * 1024) {
      setMessage({ type: 'error', text: 'File size exceeds 50MB limit.' })
      return
    }

    setFile(selectedFile)
    setMessage({ type: '', text: '' })
  }

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0])
    }
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  const handleUpload = async () => {
    if (!file) {
      setMessage({ type: 'error', text: 'Please select a file first.' })
      return
    }

    setUploading(true)
    setMessage({ type: '', text: '' })

    try {
      const formData = new FormData()
      formData.append('file', file)
      if (questions.trim()) {
        formData.append('questions', questions)
      }

      const response = await axios.post(`${API_BASE}/auth/documents/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setMessage({
        type: 'success',
        text: `Document uploaded successfully! Document ID: ${response.data.document_id}. Processing has started...`
      })
      
      // Reset form
      setFile(null)
      setQuestions('')
      document.getElementById('fileInput').value = ''
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Upload failed. Please try again.'
      })
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Upload Document</h1>
        <p className="text-gray-600">Upload PDF, DOCX, TXT, or MD files for AI processing</p>
      </div>

      {message.text && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className={`p-4 rounded-lg flex items-center space-x-2 ${
            message.type === 'success'
              ? 'bg-green-50 text-green-700 border border-green-200'
              : 'bg-red-50 text-red-700 border border-red-200'
          }`}
        >
          {message.type === 'success' ? (
            <CheckCircle className="w-5 h-5" />
          ) : (
            <AlertCircle className="w-5 h-5" />
          )}
          <span>{message.text}</span>
        </motion.div>
      )}

      {/* File Upload Area */}
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-all ${
          dragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 bg-white hover:border-primary-400 hover:bg-gray-50'
        }`}
      >
        <input
          id="fileInput"
          type="file"
          accept=".pdf,.docx,.txt,.md"
          onChange={handleFileInput}
          className="hidden"
        />

        {file ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="space-y-4"
          >
            <div className="flex items-center justify-center">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-purple-500 rounded-xl flex items-center justify-center">
                <FileText className="w-8 h-8 text-white" />
              </div>
            </div>
            <div>
              <p className="font-semibold text-gray-800">{file.name}</p>
              <p className="text-sm text-gray-500 mt-1">{formatFileSize(file.size)}</p>
            </div>
            <button
              onClick={() => {
                setFile(null)
                document.getElementById('fileInput').value = ''
              }}
              className="inline-flex items-center space-x-2 text-red-600 hover:text-red-700"
            >
              <X className="w-4 h-4" />
              <span>Remove</span>
            </button>
          </motion.div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-center">
              <div className="w-16 h-16 bg-gray-100 rounded-xl flex items-center justify-center">
                <Upload className="w-8 h-8 text-gray-400" />
              </div>
            </div>
            <div>
              <p className="text-lg font-semibold text-gray-700 mb-2">
                Drag and drop your file here
              </p>
              <p className="text-sm text-gray-500 mb-4">or</p>
              <label htmlFor="fileInput">
                <span className="inline-block px-6 py-3 bg-gradient-to-r from-primary-600 to-purple-600 text-white rounded-lg font-semibold cursor-pointer hover:shadow-lg transition-all">
                  Browse Files
                </span>
              </label>
            </div>
            <p className="text-xs text-gray-400 mt-4">
              Supported formats: PDF, DOCX, TXT, MD (Max 50MB)
            </p>
          </div>
        )}
      </div>

      {/* Optional Questions */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Optional: Questions to Answer (one per line)
        </label>
        <textarea
          value={questions}
          onChange={(e) => setQuestions(e.target.value)}
          rows={4}
          placeholder="What is the main topic of this document?&#10;What are the key points?&#10;What are the main conclusions?"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
        />
        <p className="text-xs text-gray-500 mt-2">
          Leave blank to use default questions
        </p>
      </div>

      {/* Upload Button */}
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={handleUpload}
        disabled={!file || uploading}
        className="w-full py-4 bg-gradient-to-r from-primary-600 to-purple-600 text-white rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
      >
        {uploading ? (
          <>
            <Loader className="w-5 h-5 animate-spin" />
            <span>Uploading...</span>
          </>
        ) : (
          <>
            <Upload className="w-5 h-5" />
            <span>Upload & Process Document</span>
          </>
        )}
      </motion.button>
    </div>
  )
}
