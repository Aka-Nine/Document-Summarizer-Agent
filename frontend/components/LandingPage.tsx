'use client'

import { motion, useScroll, useTransform } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { useState, useRef } from 'react'
import { 
  FileText, 
  Brain, 
  Zap, 
  Shield, 
  Search, 
  Sparkles,
  ArrowRight,
  CheckCircle,
  BarChart3,
  Lock,
  GitBranch,
  Cloud,
  Database,
  Sparkle,
  Play,
  Code,
  TestTube,
  Rocket,
  ChevronDown,
  Menu,
  X
} from 'lucide-react'
import AuthModal from './AuthModal'

export default function LandingPage() {
  const router = useRouter()
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login')
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const heroRef = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({
    target: heroRef,
    offset: ['start start', 'end start']
  })
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0])
  const y = useTransform(scrollYProgress, [0, 0.5], [0, -100])

  const handleGetStarted = () => {
    setAuthMode('register')
    setShowAuthModal(true)
  }

  const handleTryNow = () => {
    setAuthMode('login')
    setShowAuthModal(true)
  }

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 bg-black/80 backdrop-blur-sm border-b border-white/5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-center space-x-2"
            >
              <span className="text-xl font-semibold tracking-tight">DocIntelligence</span>
            </motion.div>
            
            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              <button className="text-sm text-gray-400 hover:text-white transition-colors">AI Platform</button>
              <button className="text-sm text-gray-400 hover:text-white transition-colors">Infrastructure</button>
              <button className="text-sm text-gray-400 hover:text-white transition-colors">Research</button>
              <button className="text-sm text-gray-400 hover:text-white transition-colors">Company</button>
              <button
                onClick={handleTryNow}
                className="text-sm text-gray-400 hover:text-white transition-colors"
              >
                Sign In
              </button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleGetStarted}
                className="px-4 py-2 bg-white text-black text-sm font-medium rounded hover:bg-gray-100 transition-colors"
              >
                Sign Up
              </motion.button>
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden text-gray-400 hover:text-white"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden border-t border-white/5 bg-black/95 backdrop-blur-sm"
          >
            <div className="px-4 py-4 space-y-4">
              <button className="block text-sm text-gray-400 hover:text-white">AI Platform</button>
              <button className="block text-sm text-gray-400 hover:text-white">Infrastructure</button>
              <button className="block text-sm text-gray-400 hover:text-white">Research</button>
              <button className="block text-sm text-gray-400 hover:text-white">Company</button>
              <div className="pt-4 border-t border-white/5 space-y-2">
                <button
                  onClick={handleTryNow}
                  className="block w-full text-left text-sm text-gray-400 hover:text-white"
                >
                  Sign In
                </button>
                <button
                  onClick={handleGetStarted}
                  className="block w-full px-4 py-2 bg-white text-black text-sm font-medium rounded"
                >
                  Sign Up
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </nav>

      {/* Hero Section */}
      <motion.section
        ref={heroRef}
        style={{ opacity, y }}
        className="relative min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8 pt-20"
      >
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
            className="mb-8"
          >
            <h1 className="text-6xl md:text-8xl lg:text-9xl font-light tracking-tight mb-6 leading-[0.9]">
              <span className="block">Creating</span>
              <span className="block">the most</span>
              <span className="block font-medium">efficient</span>
              <span className="block">document</span>
              <span className="block font-medium">intelligence</span>
              <span className="block">platform.</span>
            </h1>
          </motion.div>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto mb-12 leading-relaxed"
          >
            We design and operate Document Intelligence Platforms — autonomous AI systems that optimize processing, 
            analysis, and insights at every layer of the stack.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleGetStarted}
              className="px-8 py-4 bg-white text-black text-lg font-medium rounded hover:bg-gray-100 transition-colors"
            >
              Get Started
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => {
                const featuresSection = document.getElementById('platform')
                featuresSection?.scrollIntoView({ behavior: 'smooth' })
              }}
              className="px-8 py-4 border border-white/20 text-white text-lg font-medium rounded hover:bg-white/5 transition-colors"
            >
              Learn More
            </motion.button>
          </motion.div>
        </div>

        {/* Scroll Indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, repeat: Infinity, repeatType: "reverse", duration: 2 }}
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        >
          <ChevronDown className="w-6 h-6 text-gray-500" />
        </motion.div>
      </motion.section>

      {/* Platform Section */}
      <section id="platform" className="min-h-screen py-32 px-4 sm:px-6 lg:px-8 border-t border-white/5">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="mb-20"
          >
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-5xl md:text-6xl font-light tracking-tight">
                <span className="font-medium">AI Platform</span>
              </h2>
              <p className="text-sm text-gray-400 max-w-md text-right">
                Access the platform built for what document intelligence actually needs: 
                processing power, reliability, performance and cost efficiency.
              </p>
            </div>
          </motion.div>

          {/* Platform Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-20">
            {[
              {
                title: 'Document Processing',
                subtitle: 'Advanced AI-powered extraction and analysis',
                features: ['PDF, DOCX, TXT, MD support', '50MB file limit', 'Batch processing'],
                gradient: 'from-blue-500/20 to-cyan-500/20'
              },
              {
                title: 'RAG Querying',
                subtitle: 'Intelligent document question-answering',
                features: ['Vector search', 'Context retrieval', 'Source citations'],
                gradient: 'from-purple-500/20 to-pink-500/20'
              },
              {
                title: 'Analytics & Insights',
                subtitle: 'Comprehensive document intelligence',
                features: ['Processing history', 'Performance metrics', 'Usage analytics'],
                gradient: 'from-green-500/20 to-emerald-500/20'
              }
            ].map((card, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, duration: 0.6 }}
                className="border border-white/10 rounded-lg p-8 hover:border-white/20 transition-colors bg-gradient-to-br from-white/5 to-transparent"
              >
                <h3 className="text-2xl font-medium mb-2">{card.title}</h3>
                <p className="text-gray-400 mb-6 text-sm">{card.subtitle}</p>
                <ul className="space-y-2">
                  {card.features.map((feature, idx) => (
                    <li key={idx} className="text-sm text-gray-500 flex items-center space-x-2">
                      <div className="w-1 h-1 bg-white rounded-full"></div>
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>

          {/* CTA */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleGetStarted}
              className="px-8 py-4 bg-white text-black text-lg font-medium rounded hover:bg-gray-100 transition-colors"
            >
              Deploy Now
            </motion.button>
          </motion.div>
        </div>
      </section>

      {/* Infrastructure Section */}
      <section className="min-h-screen py-32 px-4 sm:px-6 lg:px-8 border-t border-white/5">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="mb-20"
          >
            <h2 className="text-5xl md:text-6xl font-light tracking-tight mb-8">
              <span className="font-medium">Infrastructure</span>
            </h2>
            <p className="text-lg text-gray-400 max-w-2xl">
              Our platform is powered by uniquely efficient infrastructure. At the core of every deployment 
              is the Document Intelligence Engine: a modular system designed to run high-density AI processing 
              with lower power, cost, and complexity.
            </p>
          </motion.div>

          {/* Infrastructure Features */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mb-20">
            {[
              {
                title: 'Cloud-Native Architecture',
                description: 'Built for scale with containerized services, auto-scaling, and distributed processing.',
                icon: Cloud
              },
              {
                title: 'Multi-Provider Support',
                description: 'Seamlessly integrates with MongoDB, Chroma, Redis, AWS S3, and more.',
                icon: Database
              },
              {
                title: 'Enterprise Security',
                description: 'SOC 2 compliant with encrypted storage, secure connections, and audit logging.',
                icon: Shield
              },
              {
                title: 'Self-Hosted Options',
                description: 'Deploy in your own cloud or VPC with full control over infrastructure and data.',
                icon: Lock
              }
            ].map((item, index) => {
              const Icon = item.icon
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: index % 2 === 0 ? -30 : 30 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1, duration: 0.6 }}
                  className="space-y-4"
                >
                  <div className="w-12 h-12 border border-white/10 rounded-lg flex items-center justify-center">
                    <Icon className="w-6 h-6 text-gray-400" />
                  </div>
                  <h3 className="text-2xl font-medium">{item.title}</h3>
                  <p className="text-gray-400 leading-relaxed">{item.description}</p>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Principles Section */}
      <section className="py-32 px-4 sm:px-6 lg:px-8 border-t border-white/5">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-20"
          >
            <h2 className="text-5xl md:text-6xl font-light tracking-tight mb-4">
              Principles of <span className="font-medium">Efficiency</span>
            </h2>
            <p className="text-lg text-gray-400 max-w-2xl">
              Five rules that shape every Document Intelligence Platform
            </p>
          </motion.div>

          <div className="space-y-16">
            {[
              {
                number: '01',
                title: 'Systems at Scale',
                description: 'We design document intelligence not as applications but as scalable platforms. Our architecture is modular, highly available, and optimized for processing density.'
              },
              {
                number: '02',
                title: 'Efficiency by Design',
                description: 'We pursue transformative reductions in processing time and cost, enabled by optimized pipelines and infrastructure tuned for document processing.'
              },
              {
                number: '03',
                title: 'Ground-Up Engineering',
                description: 'We engineer platforms from the bottom up: AI-aware processing, infrastructure-aware design. Every layer is co-designed to maximize system-wide efficiency.'
              },
              {
                number: '04',
                title: 'Radical Transparency',
                description: 'Trust is built by visibility. We provide real-time processing metrics, performance data, and comprehensive logging.'
              },
              {
                number: '05',
                title: 'Long-Term Adaptability',
                description: 'Our designs anticipate AI model evolution. Platform architecture scales across multiple generations with redundancy models that evolve without retrofit.'
              }
            ].map((principle, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, duration: 0.6 }}
                className="flex flex-col md:flex-row gap-8 items-start"
              >
                <div className="flex-shrink-0">
                  <span className="text-6xl font-light text-gray-700">{principle.number}</span>
                </div>
                <div className="flex-1">
                  <h3 className="text-3xl font-medium mb-4">{principle.title}</h3>
                  <p className="text-lg text-gray-400 leading-relaxed max-w-3xl">
                    {principle.description}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Getting Started Section */}
      <section className="py-32 px-4 sm:px-6 lg:px-8 border-t border-white/5">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <h2 className="text-5xl md:text-6xl font-light tracking-tight mb-8">
              Getting started <span className="font-medium">is easy</span>
            </h2>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            {[
              {
                step: '1',
                title: 'Connect Data',
                description: 'Choose your storage: MongoDB, Chroma, Redis, AWS S3, or local filesystem. Configure access permissions.'
              },
              {
                step: '2',
                title: 'Upload Documents',
                description: 'Upload PDF, DOCX, TXT, or MD files. Our AI automatically processes and indexes content.'
              },
              {
                step: '3',
                title: 'Query & Analyze',
                description: 'Ask questions, get insights, and analyze your documents using RAG-powered intelligence.'
              }
            ].map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1, duration: 0.6 }}
                className="text-center"
              >
                <div className="w-16 h-16 border border-white/10 rounded-full flex items-center justify-center mx-auto mb-6 text-2xl font-light">
                  {item.step}
                </div>
                <h3 className="text-2xl font-medium mb-4">{item.title}</h3>
                <p className="text-gray-400 leading-relaxed">{item.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Security Section */}
      <section className="py-32 px-4 sm:px-6 lg:px-8 border-t border-white/5">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-20"
          >
            <h2 className="text-5xl md:text-6xl font-light tracking-tight mb-8">
              Built-in security <span className="font-medium">and compliance</span>
            </h2>
            <p className="text-lg text-gray-400 max-w-3xl">
              DocIntelligence secures every connection, pipeline, and runtime environment. 
              Credentials are managed securely and never stored in code or configuration files, 
              providing security and compliance from integration through deployment.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { title: 'Secure Connections', desc: 'Encrypted credentials, secure OAuth and token-based access' },
              { title: 'Compliance-Ready', desc: 'SOC 2 Type 2, GDPR compliant with audit logging' },
              { title: 'Isolated Environments', desc: 'Containerized runtime per task with full isolation' }
            ].map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="border border-white/10 rounded-lg p-8"
              >
                <h3 className="text-xl font-medium mb-3">{item.title}</h3>
                <p className="text-gray-400 text-sm">{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-32 px-4 sm:px-6 lg:px-8 border-t border-white/5">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-5xl md:text-6xl font-light tracking-tight mb-8">
              <span className="font-medium">Autonomous AI systems</span> for document intelligence
            </h2>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleGetStarted}
              className="px-8 py-4 bg-white text-black text-lg font-medium rounded hover:bg-gray-100 transition-colors inline-flex items-center space-x-2"
            >
              <span>Get Started</span>
              <ArrowRight className="w-5 h-5" />
            </motion.button>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <span className="text-sm font-semibold">DocIntelligence</span>
            </div>
            <div className="flex flex-wrap justify-center gap-8 text-sm text-gray-400">
              <button className="hover:text-white transition-colors">Privacy Policy</button>
              <button className="hover:text-white transition-colors">Terms of Use</button>
              <span>© 2024 Document Intelligence Platform</span>
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
