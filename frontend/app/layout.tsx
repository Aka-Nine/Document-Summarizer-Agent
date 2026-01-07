import type { Metadata } from 'next'
import './globals.css'
import { AuthProvider } from '@/context/AuthContext'

export const metadata: Metadata = {
  title: 'DocIntelligence — Creating the most efficient document intelligence platform',
  description: 'Autonomous AI systems for document intelligence. We design and operate platforms that optimize processing, analysis, and insights at every layer.',
  keywords: ['document intelligence', 'AI', 'RAG', 'document processing', 'autonomous AI'],
  authors: [{ name: 'DocIntelligence' }],
  openGraph: {
    title: 'DocIntelligence — Creating the most efficient document intelligence platform',
    description: 'Autonomous AI systems for document intelligence',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
