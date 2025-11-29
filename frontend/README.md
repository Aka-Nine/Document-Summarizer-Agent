# Document Intelligence Platform - Test Frontend

A simple, modern frontend for testing the Document Intelligence Platform API.

## Features

- ✅ User Registration & Login
- ✅ Document Upload (PDF, DOCX, TXT)
- ✅ Document List with Status
- ✅ RAG-based Document Querying
- ✅ Real-time Status Updates
- ✅ Beautiful, Responsive UI

## Quick Start

### Option 1: Open Directly in Browser

1. Make sure the backend is running:
   ```bash
   python run.py
   ```

2. Open `index.html` in your browser:
   - Double-click `index.html`, or
   - Right-click → Open with → Your browser

3. The frontend will connect to `http://localhost:8000`

### Option 2: Serve with Python HTTP Server

```bash
cd frontend
python -m http.server 8080
```

Then open: http://localhost:8080

### Option 3: Serve with FastAPI (Recommended)

The backend can serve static files. Add this to your FastAPI app:

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="frontend"), name="static")
```

Then access at: http://localhost:8000/static/index.html

## Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Upload Document**: Select a PDF, DOCX, or TXT file and upload
3. **View Documents**: See all your uploaded documents with their processing status
4. **Query Documents**: Ask questions about processed documents using RAG

## API Endpoints Used

- `POST /api/v1/register` - User registration
- `POST /api/v1/login` - User login
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents` - List documents
- `GET /api/v1/documents/{id}` - Get document details
- `POST /api/v1/documents/{id}/query` - Query document with RAG

## Configuration

To change the API URL, edit the `API_BASE` constant in `index.html`:

```javascript
const API_BASE = 'http://localhost:8000/api/v1';
```

## Browser Compatibility

- Chrome/Edge (Recommended)
- Firefox
- Safari
- Opera

## Notes

- Make sure CORS is enabled in your backend (already configured)
- The frontend stores the auth token in localStorage
- Documents must be processed (status: "completed") before querying
- RAG must be enabled for document querying to work

