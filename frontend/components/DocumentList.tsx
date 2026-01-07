'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FileText, RefreshCw, Clock, CheckCircle, XCircle, Loader, Eye } from 'lucide-react'
import axios from 'axios'
import { useRouter } from 'next/navigation'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1'

interface Document {
  id: string
  filename: string
  status: string
  file_type?: string
  file_size?: number
  chunks_indexed?: number
  summary?: string
  rag_enabled?: boolean
  vector_db_indexed?: boolean
  created_at?: string
}

const statusConfig: Record<string, { color: string; icon: typeof FileText }> = {
  pending: { color: 'bg-yellow-100 text-yellow-800', icon: Clock },
  processing: { color: 'bg-blue-100 text-blue-800', icon: Loader },
  completed: { color: 'bg-green-100 text-green-800', icon: CheckCircle },
  failed: { color: 'bg-red-100 text-red-800', icon: XCircle },
}

export default function DocumentList() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const router = useRouter()

  const fetchDocuments = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await axios.get(`${API_BASE}/auth/documents`)
      setDocuments(response.data)
    } catch (err) {
      setError('Failed to load documents. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDocuments()
    // Refresh every 5 seconds to check for status updates
    const interval = setInterval(fetchDocuments, 5000)
    return () => clearInterval(interval)
  }, [])

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'N/A'
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const formatFileSize = (bytes?: number) => {
    if (!bytes) return 'N/A'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">My Documents</h1>
          <p className="text-gray-400">View and manage your uploaded documents</p>
        </div>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={fetchDocuments}
          disabled={loading}
          className="flex items-center space-x-2 px-4 py-2 bg-gray-900 border border-gray-700 rounded-lg hover:bg-gray-800 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </motion.button>
      </div>

      {error && (
        <div className="p-4 bg-red-50 text-red-700 border border-red-200 rounded-lg">
          {error}
        </div>
      )}

      {loading && documents.length === 0 ? (
        <div className="flex items-center justify-center py-12">
          <Loader className="w-8 h-8 animate-spin text-primary-600" />
        </div>
      ) : documents.length === 0 ? (
        <div className="text-center py-12 bg-gray-900 rounded-xl border border-gray-800">
          <FileText className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-300 text-lg mb-2">No documents yet</p>
          <p className="text-gray-500 mb-4">Upload your first document to get started</p>
          <button
            onClick={() => router.push('/dashboard')}
            className="px-6 py-2 bg-gradient-to-r from-primary-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg transition-all"
          >
            Upload Document
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {documents.map((doc, index) => {
            const StatusIcon = statusConfig[doc.status]?.icon || FileText
            return (
              <motion.div
                key={doc.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-gray-900 rounded-xl border border-gray-800 p-6 hover:border-primary-500/50 transition-all card-hover"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3 flex-1">
                    <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-purple-500 rounded-lg flex items-center justify-center flex-shrink-0">
                      <FileText className="w-6 h-6 text-white" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold text-white truncate">{doc.filename}</h3>
                      <p className="text-sm text-gray-400 mt-1">
                        {formatFileSize(doc.file_size)} • {doc.file_type?.toUpperCase()}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-2 mb-4">
                  <span className={`inline-flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium ${
                    statusConfig[doc.status]?.color || 'bg-gray-100 text-gray-800'
                  }`}>
                    <StatusIcon className={`w-3 h-3 ${doc.status === 'processing' ? 'animate-spin' : ''}`} />
                    <span className="capitalize">{doc.status}</span>
                  </span>
                  {doc.rag_enabled && (
                    <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-medium">
                      RAG Enabled
                    </span>
                  )}
                </div>

                {doc.summary && (
                  <p className="text-sm text-gray-400 mb-4 line-clamp-3">
                    {doc.summary}
                  </p>
                )}

                <div className="flex items-center justify-between text-xs text-gray-500 pt-4 border-t border-gray-800">
                  <span>Uploaded: {formatDate(doc.created_at)}</span>
                  {doc.chunks_indexed && doc.chunks_indexed > 0 && (
                    <span>{doc.chunks_indexed} chunks indexed</span>
                  )}
                </div>

                {doc.status === 'completed' && (
                  <button
                    onClick={() => router.push(`/dashboard?tab=query&doc=${doc.id}`)}
                    className="mt-4 w-full flex items-center justify-center space-x-2 px-4 py-2 bg-primary-900/20 text-primary-400 rounded-lg hover:bg-primary-900/30 border border-primary-500/30 transition-colors"
                  >
                    <Eye className="w-4 h-4" />
                    <span>View & Query</span>
                  </button>
                )}
              </motion.div>
            )
          })}
        </div>
      )}
    </div>
  )
}
