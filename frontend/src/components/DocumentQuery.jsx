import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, Send, FileText, Loader, Bot, User, Sparkles } from 'lucide-react'
import axios from 'axios'
import { useSearchParams } from 'react-router-dom'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1'

export default function DocumentQuery() {
  const [searchParams] = useSearchParams()
  const [documents, setDocuments] = useState([])
  const [selectedDocId, setSelectedDocId] = useState(searchParams.get('doc') || '')
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [chatHistory, setChatHistory] = useState([])
  const [loadingDocs, setLoadingDocs] = useState(true)

  useEffect(() => {
    fetchDocuments()
  }, [])

  useEffect(() => {
    if (searchParams.get('doc')) {
      setSelectedDocId(searchParams.get('doc'))
    }
  }, [searchParams])

  const fetchDocuments = async () => {
    try {
      const response = await axios.get(`${API_BASE}/auth/documents`)
      const completedDocs = response.data.filter(
        doc => doc.status === 'completed' && doc.vector_db_indexed
      )
      setDocuments(completedDocs)
      
      if (completedDocs.length > 0 && !selectedDocId) {
        setSelectedDocId(completedDocs[0].id)
      }
    } catch (err) {
      console.error('Failed to load documents:', err)
    } finally {
      setLoadingDocs(false)
    }
  }

  const handleQuery = async () => {
    if (!query.trim() || !selectedDocId) return

    const queryText = query.trim()
    const userMessage = { role: 'user', content: queryText }
    setChatHistory(prev => [...prev, userMessage])
    setQuery('')
    setLoading(true)

    try {
      const response = await axios.post(
        `${API_BASE}/auth/documents/${selectedDocId}/query`,
        {
          query: queryText,
          document_id: selectedDocId
        }
      )

      const botMessage = {
        role: 'assistant',
        content: response.data.answer || 'No answer provided',
        sources: response.data.sources || [],
        responseTime: response.data.response_time
      }

      setChatHistory(prev => [...prev, botMessage])
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: error.response?.data?.detail || 'Failed to process query. Please try again.',
        error: true
      }
      setChatHistory(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleQuery()
    }
  }

  const selectedDoc = documents.find(doc => doc.id === selectedDocId)

  return (
    <div className="space-y-6 h-[calc(100vh-12rem)] flex flex-col">
      <div>
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Query Documents</h1>
        <p className="text-gray-600">Ask questions about your processed documents using AI</p>
      </div>

      {/* Document Selector */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select Document
        </label>
        {loadingDocs ? (
          <div className="flex items-center space-x-2 text-gray-500">
            <Loader className="w-4 h-4 animate-spin" />
            <span>Loading documents...</span>
          </div>
        ) : documents.length === 0 ? (
          <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg text-yellow-800">
            No processed documents available. Please upload and process a document first.
          </div>
        ) : (
          <select
            value={selectedDocId}
            onChange={(e) => {
              setSelectedDocId(e.target.value)
              setChatHistory([])
            }}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white"
          >
            {documents.map(doc => (
              <option key={doc.id} value={doc.id}>
                {doc.filename} {doc.chunks_indexed > 0 && `(${doc.chunks_indexed} chunks)`}
              </option>
            ))}
          </select>
        )}
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col bg-white rounded-xl border border-gray-200 shadow-lg overflow-hidden">
        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {chatHistory.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="w-20 h-20 bg-gradient-to-br from-primary-500 to-purple-500 rounded-2xl flex items-center justify-center mb-4">
              <Sparkles className="w-10 h-10 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              Start a Conversation
            </h3>
            <p className="text-gray-600 max-w-md">
              Select a document and ask questions to get AI-powered answers based on its content.
            </p>
          </div>
          ) : (
            <AnimatePresence>
              {chatHistory.map((message, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`flex items-start space-x-3 max-w-3xl ${
                      message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                    }`}
                  >
                    <div
                      className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                        message.role === 'user'
                          ? 'bg-gradient-to-br from-primary-500 to-purple-500'
                          : 'bg-gradient-to-br from-purple-500 to-pink-500'
                      }`}
                    >
                      {message.role === 'user' ? (
                        <User className="w-5 h-5 text-white" />
                      ) : (
                        <Bot className="w-5 h-5 text-white" />
                      )}
                    </div>
                    <div
                      className={`rounded-2xl px-4 py-3 ${
                        message.role === 'user'
                          ? 'bg-gradient-to-r from-primary-600 to-purple-600 text-white'
                          : message.error
                          ? 'bg-red-50 text-red-700 border border-red-200'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{message.content}</p>
                      {message.sources && message.sources.length > 0 && (
                        <div className="mt-3 pt-3 border-t border-gray-300">
                          <p className="text-xs font-semibold mb-2">Sources:</p>
                          <div className="space-y-1">
                            {message.sources.slice(0, 3).map((source, idx) => (
                              <p key={idx} className="text-xs opacity-80">
                                • {source.text?.substring(0, 100)}...
                              </p>
                            ))}
                          </div>
                        </div>
                      )}
                      {message.responseTime && (
                        <p className="text-xs opacity-70 mt-2">
                          Response time: {message.responseTime.toFixed(2)}s
                        </p>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          )}

          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-start space-x-3"
            >
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="bg-gray-100 rounded-2xl px-4 py-3">
                <Loader className="w-5 h-5 animate-spin text-gray-600" />
              </div>
            </motion.div>
          )}
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 p-4">
          <div className="flex items-end space-x-2">
            <div className="flex-1 relative">
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask a question about the document..."
                rows={1}
                disabled={!selectedDocId || loading}
                className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none disabled:bg-gray-50 disabled:cursor-not-allowed"
                style={{ minHeight: '48px', maxHeight: '120px' }}
              />
            </div>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleQuery}
              disabled={!query.trim() || !selectedDocId || loading}
              className="px-6 py-3 bg-gradient-to-r from-primary-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              {loading ? (
                <Loader className="w-5 h-5 animate-spin" />
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  <span className="hidden sm:inline">Send</span>
                </>
              )}
            </motion.button>
          </div>
          {selectedDoc && (
            <p className="text-xs text-gray-500 mt-2">
              Querying: <span className="font-medium">{selectedDoc.filename}</span>
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
