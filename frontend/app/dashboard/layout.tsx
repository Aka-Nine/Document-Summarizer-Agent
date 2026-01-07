import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Dashboard - Document Intelligence Platform',
  description: 'Manage your documents and interact with AI-powered analysis',
}

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <>{children}</>
}
