# Quick Start Guide - Next.js Frontend

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

### Step 2: Configure Environment Variables

Create `.env.local` file:

```bash
cp .env.local.example .env.local
```

Edit `.env.local` and set your API URL:

```env
NEXT_PUBLIC_API_BASE=http://localhost:8000/api/v1
```

### Step 3: Start Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📋 Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Backend API running on `http://localhost:8000`

## 🎯 What You'll See

1. **Landing Page** - Beautiful animated landing page with feature showcase
2. **Authentication** - Click "Get Started" to register or "Sign In" to login
3. **Dashboard** - After login, you'll see:
   - Upload tab: Drag & drop document upload
   - My Documents tab: View all your documents
   - Query tab: Ask questions about your documents

## 🛠️ Available Scripts

- `npm run dev` - Start development server (port 3000)
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## 🐛 Troubleshooting

### Port Already in Use
If port 3000 is busy, Next.js will automatically use the next available port.

### API Connection Issues
- Make sure backend is running on `http://localhost:8000`
- Check CORS settings in backend
- Verify `NEXT_PUBLIC_API_BASE` in `.env.local` file

### Build Errors
- Clear `.next` directory: `rm -rf .next`
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check TypeScript errors: `npm run build`

### Module Not Found Errors
- Make sure all dependencies are installed: `npm install`
- Check that you're using the correct import paths (use `@/` prefix for absolute imports)

## 📚 Next Steps

- Read the full [README.md](./README.md) for detailed documentation
- Check out the component structure in `components/`
- Customize colors in `tailwind.config.js`
- Deploy to production using `npm run build`

## 🚀 Production Deployment

### Build for Production

```bash
npm run build
npm start
```

### Deploy to Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

The project is now ready for production deployment!
