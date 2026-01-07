'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { useAuth } from '@/context/AuthContext'
import { useRouter } from 'next/navigation'
import { 
  Upload, 
  FileText, 
  Search, 
  LogOut, 
  User,
  Menu,
  X,
  Sparkles
} from 'lucide-react'
import DocumentUpload from './DocumentUpload'
import DocumentList from './DocumentList'
import DocumentQuery from './DocumentQuery'

export default function Dashboard() {
  const { user, logout } = useAuth()
  const router = useRouter()
  const [activeTab, setActiveTab] = useState('upload')
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const handleLogout = () => {
    logout()
    router.push('/')
    router.refresh()
  }

  const tabs = [
    { id: 'upload', label: 'Upload', icon: Upload },
    { id: 'documents', label: 'My Documents', icon: FileText },
    { id: 'query', label: 'Query', icon: Search },
  ]

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="bg-black border-b border-white/5 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden p-2 rounded-lg hover:bg-gray-800 text-gray-300"
              >
                {sidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
              <div className="flex items-center space-x-2">
                <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <span className="text-xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">DocIntelligence</span>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="hidden sm:flex items-center space-x-2 text-gray-300">
                <User className="w-5 h-5" />
                <span className="font-medium">{user?.username}</span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 px-4 py-2 text-gray-300 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
              >
                <LogOut className="w-5 h-5" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex max-w-7xl mx-auto">
        {/* Sidebar */}
        <motion.aside
          initial={{ x: -300 }}
          animate={{ x: sidebarOpen ? 0 : -300 }}
          className={`fixed lg:static inset-y-0 left-0 top-16 lg:top-0 w-64 bg-gray-900 border-r border-gray-800 z-30 lg:z-auto transition-transform duration-300`}
        >
          <nav className="p-4 space-y-2">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id)
                    setSidebarOpen(false)
                  }}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
                    activeTab === tab.id
                      ? 'bg-gradient-to-r from-primary-600 to-purple-600 text-white shadow-lg'
                      : 'text-gray-300 hover:bg-gray-800'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{tab.label}</span>
                </button>
              )
            })}
          </nav>
        </motion.aside>

        {/* Main Content */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="max-w-5xl mx-auto"
          >
            {activeTab === 'upload' && <DocumentUpload />}
            {activeTab === 'documents' && <DocumentList />}
            {activeTab === 'query' && <DocumentQuery />}
          </motion.div>
        </main>
      </div>

      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/80 z-20 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  )
}
