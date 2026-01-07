import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { 
  FileText, 
  Brain, 
  Zap, 
  Shield, 
  Search, 
  Sparkles,
  ArrowRight,
  CheckCircle,
  BarChart3
} from 'lucide-react'
import AuthModal from './AuthModal'
import { useState } from 'react'

const features = [
  {
    icon: FileText,
    title: 'Smart Document Processing',
    description: 'Upload PDFs, DOCX, and text files. Our AI extracts and processes content intelligently.',
    color: 'from-blue-500 to-cyan-500'
  },
  {
    icon: Brain,
    title: 'AI-Powered Summarization',
    description: 'Get comprehensive summaries of your documents using advanced language models.',
    color: 'from-purple-500 to-pink-500'
  },
  {
    icon: Search,
    title: 'RAG-Based Querying',
    description: 'Ask questions about your documents and get accurate answers using Retrieval Augmented Generation.',
    color: 'from-green-500 to-emerald-500'
  },
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Process documents in seconds with our optimized pipeline and cloud infrastructure.',
    color: 'from-yellow-500 to-orange-500'
  },
  {
    icon: Shield,
    title: 'Secure & Private',
    description: 'Your documents are encrypted and stored securely. We never share your data.',
    color: 'from-red-500 to-rose-500'
  },
  {
    icon: BarChart3,
    title: 'Analytics & Insights',
    description: 'Track your document processing history and gain insights from your content.',
    color: 'from-indigo-500 to-purple-500'
  }
]

const benefits = [
  'No credit card required',
  'Free tier available',
  'Enterprise-grade security',
  '24/7 support',
  'API access included'
]

export default function LandingPage() {
  const navigate = useNavigate()
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [authMode, setAuthMode] = useState('login')

  const handleGetStarted = () => {
    setAuthMode('register')
    setShowAuthModal(true)
  }

  const handleTryNow = () => {
    setAuthMode('login')
    setShowAuthModal(true)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-purple-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 glass-effect border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center space-x-2"
            >
              <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-purple-600 rounded-lg flex items-center justify-center">
                <FileText className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-gradient">DocIntelligence</span>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center space-x-4"
            >
              <button
                onClick={handleTryNow}
                className="px-4 py-2 text-primary-600 font-medium hover:text-primary-700 transition-colors"
              >
                Sign In
              </button>
              <button
                onClick={handleGetStarted}
                className="px-6 py-2 bg-gradient-to-r from-primary-600 to-purple-600 text-white rounded-lg font-medium hover:shadow-lg transition-all transform hover:scale-105"
              >
                Get Started
              </button>
            </motion.div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring" }}
              className="inline-block mb-6"
            >
              <div className="relative">
                <Sparkles className="w-16 h-16 text-primary-600 animate-pulse" />
                <div className="absolute inset-0 bg-primary-600 blur-2xl opacity-30 rounded-full"></div>
              </div>
            </motion.div>
            
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="text-gradient">Transform Documents</span>
              <br />
              <span className="text-gray-800">Into Intelligence</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
              AI-powered document processing platform with RAG-based querying. 
              Upload, analyze, and interact with your documents like never before.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleGetStarted}
                className="px-8 py-4 bg-gradient-to-r from-primary-600 to-purple-600 text-white text-lg font-semibold rounded-xl shadow-xl hover:shadow-2xl transition-all flex items-center space-x-2"
              >
                <span>Start Free Trial</span>
                <ArrowRight className="w-5 h-5" />
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => document.getElementById('features').scrollIntoView({ behavior: 'smooth' })}
                className="px-8 py-4 bg-white text-primary-600 text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all border-2 border-primary-200"
              >
                Learn More
              </motion.button>
            </div>
            
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
              className="mt-12 flex flex-wrap justify-center gap-6"
            >
              {benefits.map((benefit, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.9 + index * 0.1 }}
                  className="flex items-center space-x-2 text-gray-600"
                >
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span>{benefit}</span>
                </motion.div>
              ))}
            </motion.div>
          </motion.div>

          {/* Animated Hero Image/Illustration */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4, duration: 0.6 }}
            className="relative max-w-5xl mx-auto mb-20"
          >
            <div className="relative bg-white rounded-2xl shadow-2xl p-8 border border-gray-100">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[1, 2, 3].map((i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 + i * 0.1 }}
                    className="bg-gradient-to-br from-primary-50 to-purple-50 rounded-xl p-6 border border-primary-100"
                  >
                    <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-purple-500 rounded-lg mb-4 flex items-center justify-center">
                      <FileText className="w-6 h-6 text-white" />
                    </div>
                    <div className="h-2 bg-primary-200 rounded-full mb-2"></div>
                    <div className="h-2 bg-primary-200 rounded-full w-3/4"></div>
                  </motion.div>
                ))}
              </div>
            </div>
            <div className="absolute -inset-4 bg-gradient-to-r from-primary-600 to-purple-600 rounded-2xl blur-2xl opacity-20 -z-10"></div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Powerful <span className="text-gradient">Features</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Everything you need to process, analyze, and interact with your documents
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                  whileHover={{ y: -5 }}
                  className="bg-white rounded-xl p-8 shadow-lg border border-gray-100 card-hover"
                >
                  <div className={`w-16 h-16 bg-gradient-to-br ${feature.color} rounded-xl flex items-center justify-center mb-6 shadow-lg`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold mb-3 text-gray-800">{feature.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{feature.description}</p>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-primary-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Transform Your Documents?
            </h2>
            <p className="text-xl text-primary-100 mb-8">
              Join thousands of users who are already using AI to unlock insights from their documents
            </p>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleGetStarted}
              className="px-10 py-5 bg-white text-primary-600 text-lg font-semibold rounded-xl shadow-2xl hover:shadow-3xl transition-all inline-flex items-center space-x-2"
            >
              <span>Get Started Free</span>
              <ArrowRight className="w-5 h-5" />
            </motion.button>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-600 to-purple-600 rounded-lg flex items-center justify-center">
              <FileText className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-white">DocIntelligence</span>
          </div>
          <p className="text-sm">© 2024 Document Intelligence Platform. All rights reserved.</p>
        </div>
      </footer>

      {showAuthModal && (
        <AuthModal
          mode={authMode}
          onClose={() => setShowAuthModal(false)}
          onSwitchMode={(mode) => setAuthMode(mode)}
        />
      )}
    </div>
  )
}
