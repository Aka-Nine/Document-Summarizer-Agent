'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Upload, FileText, X, CheckCircle, AlertCircle, Loader } from 'lucide-react'
import axios from 'axios'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1'

export default function DocumentUpload() {
  const [file, setFile] = useState<File | null>(null)
  const [questions, setQuestions] = useState('')
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error' | ''; text: string }>({ type: '', text: '' })
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0])
    }
  }

  const handleFileSelect = (selectedFile: File) => {
    const allowedTypes = ['.pdf', '.docx', '.txt', '.md']
    const fileExt = '.' + selectedFile.name.split('.').pop()?.toLowerCase()
    const maxBytes = 10 * 1024 * 1024 // align with backend default
    
    if (!fileExt || !allowedTypes.includes(fileExt)) {
      setMessage({ type: 'error', text: 'Invalid file type. Please upload PDF, DOCX, TXT, or MD files.' })
      return
    }

    if (selectedFile.size > maxBytes) {
      setMessage({ type: 'error', text: 'File size exceeds 10MB free-tier limit.' })
      return
    }

    setFile(selectedFile)
    setMessage({ type: '', text: '' })
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0])
    }
  }

  const formatFileSize = (bytes: number) => {
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

    if (questions.length > 2000) {
      setMessage({ type: 'error', text: 'Questions too long. Please keep under 2000 characters.' })
      return
    }

    const questionLines = questions
      .split('\n')
      .map(q => q.trim())
      .filter(Boolean)
    if (questionLines.length > 10) {
      setMessage({ type: 'error', text: 'Please limit to 10 questions.' })
      return
    }

    setUploading(true)
    setMessage({ type: '', text: '' })

    try {
      const formData = new FormData()
      formData.append('file', file)
      if (questionLines.length > 0) {
        formData.append('questions', questionLines.join('\n'))
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
      const fileInput = document.getElementById('fileInput') as HTMLInputElement
      if (fileInput) fileInput.value = ''
    } catch (error: any) {
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
        <h1 className="text-3xl font-bold text-white mb-2">Upload Document</h1>
        <p className="text-gray-400">Upload PDF, DOCX, TXT, or MD files for AI processing</p>
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
            ? 'border-primary-500 bg-primary-900/20'
            : 'border-gray-700 bg-gray-900 hover:border-primary-500 hover:bg-gray-800'
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
              <p className="font-semibold text-white">{file.name}</p>
              <p className="text-sm text-gray-400 mt-1">{formatFileSize(file.size)}</p>
            </div>
            <button
              onClick={() => {
                setFile(null)
                const fileInput = document.getElementById('fileInput') as HTMLInputElement
                if (fileInput) fileInput.value = ''
              }}
              className="inline-flex items-center space-x-2 text-red-400 hover:text-red-300"
            >
              <X className="w-4 h-4" />
              <span>Remove</span>
            </button>
          </motion.div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-center">
              <div className="w-16 h-16 bg-gray-800 rounded-xl flex items-center justify-center">
                <Upload className="w-8 h-8 text-gray-500" />
              </div>
            </div>
            <div>
              <p className="text-lg font-semibold text-gray-200 mb-2">
                Drag and drop your file here
              </p>
              <p className="text-sm text-gray-500 mb-4">or</p>
              <label htmlFor="fileInput">
                <span className="inline-block px-6 py-3 bg-gradient-to-r from-primary-600 to-purple-600 text-white rounded-lg font-semibold cursor-pointer hover:shadow-lg transition-all">
                  Browse Files
                </span>
              </label>
            </div>
            <p className="text-xs text-gray-500 mt-4">
              Supported formats: PDF, DOCX, TXT, MD (Max 10MB)
            </p>
          </div>
        )}
      </div>

      {/* Optional Questions */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Optional: Questions to Answer (one per line)
        </label>
        <textarea
          value={questions}
          onChange={(e) => setQuestions(e.target.value)}
          rows={4}
          placeholder="What is the main topic of this document?&#10;What are the key points?&#10;What are the main conclusions?"
          className="w-full px-4 py-3 bg-gray-800 border border-gray-700 text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none placeholder-gray-500"
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
