# Document Intelligence Platform - Next.js Frontend

A production-ready Next.js 14 frontend with App Router, TypeScript, and Tailwind CSS for the Document Intelligence Platform.

## 🚀 Features

- ⚡ **Next.js 14** with App Router for optimal performance
- 🎨 **Beautiful UI** with Tailwind CSS and Framer Motion animations
- 📱 **Fully Responsive** design for all devices
- 🔐 **Authentication** with JWT token management
- 📄 **Document Management** - Upload, view, and manage documents
- 🤖 **AI Query Interface** - Chat-like RAG-based document querying
- 🎯 **Production Ready** - Optimized builds, SEO, and performance
- 🔒 **Type Safe** - Full TypeScript support

## 🛠️ Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **Axios** - HTTP client
- **Lucide React** - Icon library

## 📦 Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.local.example .env.local

# Edit .env.local and set your API URL
NEXT_PUBLIC_API_BASE=http://localhost:8000/api/v1
```

## 🏃 Development

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint
```

The application will be available at `http://localhost:3000`

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Landing page
│   ├── dashboard/         # Dashboard pages
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── LandingPage.tsx
│   ├── AuthModal.tsx
│   ├── Dashboard.tsx
│   ├── DocumentUpload.tsx
│   ├── DocumentList.tsx
│   └── DocumentQuery.tsx
├── context/               # React contexts
│   └── AuthContext.tsx
├── next.config.js         # Next.js configuration
├── tailwind.config.js     # Tailwind configuration
└── tsconfig.json          # TypeScript configuration
```

## 🎨 Features Overview

### Landing Page
- Animated hero section with gradient backgrounds
- Feature showcase with icons
- Smooth scroll animations
- Call-to-action buttons
- Responsive design

### Authentication
- Modal-based login/register
- Form validation
- Error handling
- Auto-login after registration
- JWT token management

### Document Upload
- Drag-and-drop interface
- File type validation
- File size checking
- Optional question input
- Upload progress feedback

### Document List
- Real-time status updates
- Document cards with metadata
- Status badges
- Auto-refresh every 5 seconds
- Quick navigation to query

### Document Query
- Chat-like interface
- Document selection
- Real-time AI responses
- Source citations
- Response time display
- Chat history

## 🔧 Configuration

### Environment Variables

Create `.env.local` file:

```env
NEXT_PUBLIC_API_BASE=http://localhost:8000/api/v1
```

### API Integration

The frontend integrates with the following API endpoints:

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/documents/upload` - Upload document
- `GET /api/v1/auth/documents` - List documents
- `GET /api/v1/auth/documents/{id}` - Get document details
- `POST /api/v1/auth/documents/{id}/query` - Query document

## 🚀 Production Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Deploy to Other Platforms

Next.js can be deployed to:
- Vercel (recommended)
- Netlify
- AWS Amplify
- Docker
- Any Node.js hosting

## 📊 Performance Optimizations

- ✅ Server-side rendering (SSR)
- ✅ Static site generation (SSG) where applicable
- ✅ Image optimization
- ✅ Code splitting
- ✅ Font optimization
- ✅ Compression enabled
- ✅ SWC minification

## 🔒 Security

- ✅ Environment variable protection
- ✅ XSS protection
- ✅ CSRF protection
- ✅ Secure headers
- ✅ JWT token storage in localStorage

## 📱 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Opera (latest)

## 📝 License

Part of the Document Intelligence Platform project.
