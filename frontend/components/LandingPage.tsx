'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  FileText, 
  Sparkles,
  Zap,
  Shield,
  Code,
  ArrowRight,
  Menu,
  X,
  CheckCircle2,
  Cloud,
  Lock,
  Workflow,
  Search,
  Brain,
  Database,
  Globe,
} from 'lucide-react'
import AuthModal from './AuthModal'

export default function LandingPage() {
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [authMode, setAuthMode] = useState<'login' | 'register'>('register')
  const [mobileOpen, setMobileOpen] = useState(false)
  const [activeFilter, setActiveFilter] = useState('ALL')

  const openSignup = () => {
    setAuthMode('register')
    setShowAuthModal(true)
  }

  const openSignin = () => {
    setAuthMode('login')
    setShowAuthModal(true)
  }

  const filters = ['ALL', 'DOCUMENTS', 'SUMMARIES', 'API', 'FEATURES', 'USE CASES']

  const stories = [
    {
      category: 'DOCUMENTS',
      title: 'SHOP DOCUMENT SUMMARIZER AGENT EDITORS\' AI PROCESSING EDITS',
      date: 'DECEMBER 2024',
      featured: true,
    },
    {
      category: 'SUMMARIES',
      title: 'HOW AI SUMMARIZATION IS TRANSFORMING DOCUMENT WORKFLOWS',
      date: 'NOVEMBER 2024',
    },
    {
      category: 'API',
      title: 'INTEGRATING LANGCHAIN AND LANGSMITH FOR ENTERPRISE DOCUMENT INTELLIGENCE',
      date: 'OCTOBER 2024',
    },
  ];

  const documents = [
    {
      category: 'DOCUMENTS',
      title: 'PDF TO SUMMARY: THE MUST-HAVE AI INVESTMENT FOR ENTERPRISE TEAMS',
      date: 'AUG 2024',
      featured: true,
    },
    {
      category: 'DOCUMENTS',
      title: 'CELEBRITIES CLAIM THAT RAG-BASED QUERIES ARE BECOMING STANDARD',
      date: 'OCT 2024',
    },
    {
      category: 'DOCUMENTS',
      title: 'TAILORED MINIMALISM THE DOCUMENT PROCESSING WAY',
      date: 'NOV 2024',
    },
    {
      category: 'DOCUMENTS',
      title: 'ALL THE COOL TEAMS ARE USING VECTOR EMBEDDINGS',
      date: 'NOV 2024',
    },
  ];

  const features = [
    {
      category: 'FEATURES',
      title: 'ELEVATE YOUR DOCUMENT WORKFLOW: TIPS AND TRICKS FOR AI-NATIVE PROCESSING',
      date: 'MAY 2024',
      textOnly: true,
    },
    {
      category: 'FEATURES',
      title: 'STAY AHEAD OF THE GAME WITH THE HOTTEST AI SUMMARIZATION MODELS',
      date: 'AUG 2024',
    },
    {
      category: 'FEATURES',
      title: 'DOCUMENT INTELLIGENCE: NAVIGATING THE LATEST TRENDS IN RAG AND LLM INTEGRATION',
      date: 'OCT 2024',
      textOnly: true,
    },
    {
      category: 'FEATURES',
      title: 'HOW CAN YOU ACTUALLY TELL WHEN YOUR DOCUMENT IS PROPERLY PROCESSED?',
      date: 'MAR 2024',
      textOnly: true,
    },
    {
      category: 'FEATURES',
      title: 'DISCOVERING HIDDEN GEMS FOR YOUR DOCUMENT PIPELINE',
      date: 'AUG 2024',
    },
  ];

  const useCases = [
    {
      category: 'USE CASES',
      title: 'WHAT IS LANGSMITH TRACING? HERE\'S EVERYTHING YOU NEED TO KNOW',
      date: 'AUG 2024',
      featured: true,
    },
    {
      category: 'USE CASES',
      title: 'THE BIGGEST BREAKOUT AI TRENDS IN DOCUMENT PROCESSING',
      date: 'MAR 2024',
    },
    {
      category: 'USE CASES',
      title: 'HOW TO USE GEMINI API FOR DOCUMENT SUMMARIZATION, ACCORDING TO GOOGLE',
      date: 'MAR 2024',
    },
  ];

  const api = [
    {
      category: 'API',
      title: 'CONSIDERING DOCUMENT PROCESSING? WITH THESE 10 API ENDPOINTS, YOUR INTEGRATION BEGINS HERE.',
      date: 'AUG 2024',
      featured: true,
    },
    {
      category: 'API',
      title: 'THE ENTERPRISE SET CLAIMS THAT FASTAPI IS TRENDY FOR DOCUMENT SERVICES',
      date: 'AUG 2024',
    },
    {
      category: 'API',
      title: 'BROWSE 200+ API METHODS UNDER $300 FROM THE MOST RELIABLE DOCUMENT PROCESSING SERVICES',
      date: 'AUG 2024',
    },
    {
      category: 'API',
      title: 'BROWSE 80 DOCUMENT FEATURES THAT WON\'T GO OUT OF STYLE WITH THE CORE API',
      date: 'APR 2024',
    },
  ];

  return (
    <div className="min-h-screen bg-[#F5F1E8] text-[#2C3E2D]">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-[#F5F1E8] border-b border-[#2C3E2D]/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            <div className="flex items-center gap-8">
              <div className="text-2xl font-bold tracking-wider">DSA</div>
              <nav className="hidden md:flex items-center gap-6 text-sm uppercase tracking-wider">
                <a href="#documents" className="hover:underline">Documents</a>
                <a href="#summaries" className="hover:underline">Summaries</a>
                <a href="#api" className="hover:underline">API</a>
                <a href="#features" className="hover:underline">Features</a>
                <a href="#use-cases" className="hover:underline">Use Cases</a>
              </nav>
            </div>
            <div className="flex items-center gap-4">
              <button className="hidden md:block text-sm uppercase tracking-wider hover:underline">
                Cart
              </button>
              <button
                onClick={openSignup}
                className="px-6 py-2 bg-[#2C3E2D] text-[#F5F1E8] text-sm uppercase tracking-wider hover:bg-[#1a241b] transition-colors"
              >
                Subscribe
              </button>
              <button
                className="md:hidden p-2"
                onClick={() => setMobileOpen(!mobileOpen)}
              >
                {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>
      </header>

      <main>
        {/* STORIES Section */}
        <section className="bg-[#F5F1E8] py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-start gap-12">
              <div className="flex-shrink-0">
                <h1 className="text-8xl font-bold leading-none tracking-tight">STORIES</h1>
                <div className="flex flex-wrap gap-2 mt-6">
                  {filters.map((filter) => (
                    <button
                      key={filter}
                      onClick={() => setActiveFilter(filter)}
                      className={`px-4 py-2 text-xs uppercase tracking-wider border border-[#2C3E2D]/30 transition-colors ${
                        activeFilter === filter
                          ? 'bg-[#2C3E2D] text-[#F5F1E8]'
                          : 'bg-transparent text-[#2C3E2D] hover:bg-[#2C3E2D]/10'
                      }`}
                    >
                      {filter}
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex-1 grid grid-cols-3 gap-6">
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="space-y-6"
                >
                  <div className="aspect-[3/4] bg-[#2C3E2D]/10 rounded-lg flex items-center justify-center">
                    <FileText className="w-16 h-16 text-[#2C3E2D]/30" />
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-wider text-[#2C3E2D]/60 mb-2">
                      {stories[0].category} · {stories[0].date}
                    </p>
                    <h3 className="text-lg font-semibold leading-tight">{stories[0].title}</h3>
                  </div>
                </motion.div>

                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="col-span-2 space-y-6"
                >
                  <div className="aspect-[4/3] bg-[#2C3E2D]/10 rounded-lg flex items-center justify-center">
                    <Brain className="w-20 h-20 text-[#2C3E2D]/30" />
                  </div>
                  <div className="space-y-4">
                    <div>
                      <p className="text-xs uppercase tracking-wider text-[#2C3E2D]/60 mb-1">
                        {stories[1].category} · {stories[1].date}
                      </p>
                      <h3 className="text-xl font-semibold leading-tight">{stories[1].title}</h3>
                    </div>
                    <div>
                      <p className="text-xs uppercase tracking-wider text-[#2C3E2D]/60 mb-1">
                        {stories[2].category} · {stories[2].date}
                      </p>
                      <h3 className="text-xl font-semibold leading-tight">{stories[2].title}</h3>
                    </div>
                  </div>
                </motion.div>
              </div>
            </div>
          </div>
        </section>

        {/* DOCUMENTS Section */}
        <section id="documents" className="bg-[#2C3E2D] text-[#F5F1E8] py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between mb-12">
              <h2 className="text-8xl font-bold leading-none tracking-tight">DOCUMENTS</h2>
              <a href="#" className="text-sm uppercase tracking-wider hover:underline">VIEW ALL</a>
            </div>

            <div className="grid grid-cols-4 gap-6 mb-8">
              <div className="col-span-2">
                <div className="aspect-[4/3] bg-[#F5F1E8]/10 rounded-lg flex items-center justify-center mb-4">
                  <FileText className="w-24 h-24 text-[#F5F1E8]/30" />
                </div>
                <p className="text-xs uppercase tracking-wider text-[#F5F1E8]/60 mb-2">
                  {documents[0].category} · {documents[0].date}
                </p>
                <h3 className="text-2xl font-semibold leading-tight">{documents[0].title}</h3>
              </div>

              <div className="space-y-6">
                {documents.slice(1).map((doc, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 + idx * 0.1 }}
                  >
                    <div className="aspect-[3/4] bg-[#F5F1E8]/10 rounded-lg flex items-center justify-center mb-3">
                      <Database className="w-12 h-12 text-[#F5F1E8]/30" />
                    </div>
                    <p className="text-xs uppercase tracking-wider text-[#F5F1E8]/60 mb-1">
                      {doc.category} · {doc.date}
                    </p>
                    <h4 className="text-base font-semibold leading-tight">{doc.title}</h4>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* FEATURES Section */}
        <section id="features" className="bg-[#F5F1E8] py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between mb-12">
              <h2 className="text-8xl font-bold leading-none tracking-tight">FEATURES</h2>
              <a href="#" className="text-sm uppercase tracking-wider hover:underline">VIEW ALL</a>
            </div>

            <div className="grid grid-cols-3 gap-6 mb-8">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="col-span-2"
              >
                <p className="text-xs uppercase tracking-wider text-[#2C3E2D]/60 mb-2">
                  {features[0].category} · {features[0].date}
                </p>
                <h3 className="text-2xl font-semibold leading-tight mb-4">{features[0].title}</h3>
                <div className="aspect-[4/3] bg-[#2C3E2D]/10 rounded-lg flex items-center justify-center">
                  <Sparkles className="w-20 h-20 text-[#2C3E2D]/30" />
                </div>
                <p className="text-xs uppercase tracking-wider text-[#2C3E2D]/60 mt-4 mb-2">
                  {features[1].category} · {features[1].date}
                </p>
                <h4 className="text-xl font-semibold leading-tight">{features[1].title}</h4>
              </motion.div>

              <div className="space-y-6">
                {features.slice(2).map((feature, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 + idx * 0.1 }}
                  >
                    {feature.textOnly ? (
                      <>
                        <p className="text-xs uppercase tracking-wider text-[#2C3E2D]/60 mb-2">
                          {feature.category} · {feature.date}
                        </p>
                        <h4 className="text-lg font-semibold leading-tight">{feature.title}</h4>
                      </>
                    ) : (
                      <>
                        <div className="aspect-[3/4] bg-[#2C3E2D]/10 rounded-lg flex items-center justify-center mb-3">
                          <Zap className="w-12 h-12 text-[#2C3E2D]/30" />
                        </div>
                        <p className="text-xs uppercase tracking-wider text-[#2C3E2D]/60 mb-1">
                          {feature.category} · {feature.date}
                        </p>
                        <h4 className="text-base font-semibold leading-tight">{feature.title}</h4>
                      </>
                    )}
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* USE CASES Section */}
        <section id="use-cases" className="bg-[#F5F1E8] py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between mb-12">
              <h2 className="text-8xl font-bold leading-none tracking-tight">USE CASES</h2>
            </div>

            <div className="grid grid-cols-3 gap-6">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="col-span-2"
              >
                <div className="aspect-[4/3] bg-[#2C3E2D]/10 rounded-lg flex items-center justify-center mb-4">
                  <Workflow className="w-20 h-20 text-[#2C3E2D]/30" />
                </div>
                <p className="text-xs uppercase tracking-wider text-[#2C3E2D]/60 mb-2">
                  {useCases[0].category} · {useCases[0].date}
                </p>
                <h3 className="text-2xl font-semibold leading-tight">{useCases[0].title}</h3>
              </motion.div>

              <div className="space-y-6">
                {useCases.slice(1).map((useCase, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 + idx * 0.1 }}
                  >
                    <div className="aspect-[3/4] bg-[#2C3E2D]/10 rounded-lg flex items-center justify-center mb-3">
                      <Search className="w-12 h-12 text-[#2C3E2D]/30" />
                    </div>
                    <p className="text-xs uppercase tracking-wider text-[#2C3E2D]/60 mb-1">
                      {useCase.category} · {useCase.date}
                    </p>
                    <h4 className="text-base font-semibold leading-tight">{useCase.title}</h4>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* API Section */}
        <section id="api" className="bg-[#2C3E2D] text-[#F5F1E8] py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between mb-12">
              <h2 className="text-8xl font-bold leading-none tracking-tight">API</h2>
              <a href="#" className="text-sm uppercase tracking-wider hover:underline">VIEW ALL</a>
            </div>

            <div className="grid grid-cols-3 gap-6 mb-8">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="col-span-2"
              >
                <p className="text-xs uppercase tracking-wider text-[#F5F1E8]/60 mb-2">
                  {api[0].category} · {api[0].date}
                </p>
                <h3 className="text-2xl font-semibold leading-tight mb-4">{api[0].title}</h3>
                <div className="aspect-[4/3] bg-[#F5F1E8]/10 rounded-lg flex items-center justify-center">
                  <Code className="w-20 h-20 text-[#F5F1E8]/30" />
                </div>
                <p className="text-xs uppercase tracking-wider text-[#F5F1E8]/60 mt-4 mb-2">
                  {api[1].category} · {api[1].date}
                </p>
                <h4 className="text-xl font-semibold leading-tight">{api[1].title}</h4>
              </motion.div>

              <div className="space-y-6">
                {api.slice(2).map((item, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 + idx * 0.1 }}
                  >
                    <div className="aspect-[3/4] bg-[#F5F1E8]/10 rounded-lg flex items-center justify-center mb-3">
                      <Cloud className="w-12 h-12 text-[#F5F1E8]/30" />
                    </div>
                    <p className="text-xs uppercase tracking-wider text-[#F5F1E8]/60 mb-1">
                      {item.category} · {item.date}
                    </p>
                    <h4 className="text-base font-semibold leading-tight">{item.title}</h4>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Subscribe Section */}
        <section className="bg-[#F5F1E8] py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-3 gap-12 items-center">
              <div className="col-span-2">
                <h2 className="text-8xl font-bold leading-none tracking-tight mb-8">SUBSCRIBE NOW</h2>
                <div className="flex gap-4 max-w-md">
                  <input
                    type="email"
                    placeholder="E-MAIL ADDRESS"
                    className="flex-1 px-4 py-3 border border-[#2C3E2D]/30 bg-transparent text-[#2C3E2D] placeholder-[#2C3E2D]/50 uppercase text-sm tracking-wider focus:outline-none focus:border-[#2C3E2D]"
                  />
                  <button
                    onClick={openSignup}
                    className="px-8 py-3 bg-[#2C3E2D] text-[#F5F1E8] uppercase text-sm tracking-wider hover:bg-[#1a241b] transition-colors"
                  >
                    Subscribe
                  </button>
                </div>
              </div>
              <div className="aspect-[3/4] bg-[#2C3E2D]/10 rounded-lg flex items-center justify-center">
                <Globe className="w-24 h-24 text-[#2C3E2D]/30" />
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-[#F5F1E8] border-t border-[#2C3E2D]/10 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-4 gap-8 mb-8">
            <div>
              <div className="text-2xl font-bold tracking-wider mb-4">DSA</div>
              <p className="text-sm text-[#2C3E2D]/70">
                Document Summarizer Agent is an AI-native document intelligence platform powered by Gemini, LangChain, and LangSmith.
              </p>
            </div>
            <div>
              <h4 className="text-sm uppercase tracking-wider mb-4 font-semibold">MENU</h4>
              <ul className="space-y-2 text-sm text-[#2C3E2D]/70">
                <li><a href="#documents" className="hover:underline">Documents</a></li>
                <li><a href="#summaries" className="hover:underline">Summaries</a></li>
                <li><a href="#api" className="hover:underline">API</a></li>
                <li><a href="#features" className="hover:underline">Features</a></li>
                <li><a href="#use-cases" className="hover:underline">Use Cases</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-sm uppercase tracking-wider mb-4 font-semibold">ABOUT</h4>
              <ul className="space-y-2 text-sm text-[#2C3E2D]/70">
                <li><a href="#" className="hover:underline">Privacy Policy</a></li>
                <li><a href="#" className="hover:underline">FAQ</a></li>
                <li><a href="#" className="hover:underline">Documentation</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-sm uppercase tracking-wider mb-4 font-semibold">CONTACT</h4>
              <ul className="space-y-2 text-sm text-[#2C3E2D]/70">
                <li>api@docsummarizer.ai</li>
                <li>Enterprise Support</li>
                <li>Developer Portal</li>
              </ul>
            </div>
          </div>
          <div className="pt-8 border-t border-[#2C3E2D]/10 flex items-center justify-between text-xs text-[#2C3E2D]/60">
            <p>© 2024 Document Summarizer Agent. Powered by Gemini, LangChain & LangSmith.</p>
            <div className="flex gap-4">
              <a href="#" className="hover:underline">Privacy</a>
              <a href="#" className="hover:underline">Terms</a>
            </div>
          </div>
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
