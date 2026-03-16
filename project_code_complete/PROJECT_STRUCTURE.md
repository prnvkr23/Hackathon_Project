# Smart Complaint Portal - Complete Project Structure

## 📁 Directory Structure

```
project_code_complete/
│
├── README.md                          # Complete project documentation
├── PROJECT_STRUCTURE.md               # This file - detailed structure
│
├── backend/                           # FastAPI Backend
│   ├── server.py                      # Main API server with all endpoints
│   ├── requirements.txt               # Python dependencies
│   └── .env.example                   # Environment variables template
│
└── frontend/                          # React Frontend
    ├── package.json                   # Node dependencies
    ├── tailwind.config.js            # Tailwind CSS configuration
    ├── .env.example                   # Frontend env variables template
    │
    └── src/
        ├── App.js                     # Main app with routing
        ├── App.css                    # Global app styles
        ├── index.css                  # Tailwind & global CSS
        │
        ├── components/
        │   └── Sidebar.js             # Navigation sidebar with layout
        │
        ├── contexts/
        │   └── AuthContext.js         # Authentication context & hooks
        │
        ├── pages/
        │   ├── LoginPage.js           # Login/Register page
        │   ├── StudentDashboard.js    # Student complaint submission & history
        │   └── AdminDashboard.js      # Admin complaint management & analytics
        │
        └── lib/
            └── utils.js               # Utility functions (cn helper)
```

## 📄 File Descriptions

### Backend Files

#### `backend/server.py`
**Main FastAPI application with:**
- **Authentication System**: JWT-based auth with bcrypt password hashing
- **Database Models**: User, Complaint, Analytics using Pydantic
- **AI Integration**: Gemini 3 Flash for complaint analysis
- **API Endpoints**:
  - Auth: `/api/auth/register`, `/api/auth/login`, `/api/auth/me`
  - Complaints: `/api/complaints` (CRUD operations)
  - Analytics: `/api/analytics` (admin only)
  - Duplicates: `/api/complaints/{id}/duplicates`
- **Features**:
  - Automatic complaint categorization
  - Priority detection (Low/Medium/High)
  - Summary generation
  - Duplicate complaint detection
  - Role-based access control

#### `backend/requirements.txt`
**Python dependencies:**
- `fastapi==0.110.1` - Web framework
- `motor==3.3.1` - Async MongoDB driver
- `pyjwt>=2.10.1` - JWT token handling
- `passlib>=1.7.4` & `bcrypt==4.1.3` - Password hashing
- `emergentintegrations==0.1.0` - Gemini AI integration

#### `backend/.env.example`
**Environment variables template:**
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=test_database
CORS_ORIGINS=*
EMERGENT_LLM_KEY=your-key-here
JWT_SECRET=your-secret-here
```

### Frontend Files

#### `frontend/src/App.js`
**Main application component:**
- React Router setup with protected routes
- Authentication provider wrapper
- Route definitions:
  - `/` - Login page (redirects if authenticated)
  - `/dashboard` - Student dashboard
  - `/admin` - Admin dashboard
  - `/admin/complaints` - Admin complaints view
  - `/admin/analytics` - Admin analytics
- Sonner toast notifications

#### `frontend/src/index.css`
**Global styles:**
- Google Fonts import (Manrope, Inter)
- Tailwind CSS directives
- CSS custom properties for theming
- Warm beige background (#F9F9F7)
- Gold accent colors (#D4A373)

#### `frontend/src/App.css`
**App-specific styles:**
- Basic layout styles
- Header styling
- Link colors

#### `frontend/tailwind.config.js`
**Tailwind configuration:**
- Custom color palette (sidebar, warm-bg, gold)
- Font families (Inter, Manrope, JetBrains Mono)
- Border radius values
- Extended theme colors

#### `frontend/package.json`
**Dependencies:**
- `react@^19.0.0` & `react-dom@^19.0.0`
- `react-router-dom@^7.5.1` - Routing
- `axios@^1.8.4` - HTTP client
- `recharts@^3.6.0` - Charts
- `sonner@^2.0.3` - Toast notifications
- `lucide-react@^0.507.0` - Icons
- `@radix-ui/*` - UI primitives
- `date-fns@^4.1.0` - Date formatting

### Component Files

#### `frontend/src/components/Sidebar.js`
**Navigation sidebar with:**
- Fixed sidebar layout (desktop)
- Drawer sidebar (mobile)
- User profile display
- Role-based navigation (student vs admin)
- Logout functionality
- Active route highlighting

#### `frontend/src/contexts/AuthContext.js`
**Authentication context providing:**
- `useAuth()` hook
- `login()` function
- `register()` function
- `logout()` function
- Current user state
- Token management (localStorage)
- Axios default headers setup

### Page Files

#### `frontend/src/pages/LoginPage.js`
**Split-screen login/register page:**
- **Left side**: Form with tabs (Login/Register)
- **Right side**: Background image with overlay
- Features:
  - Email/password validation
  - Role selection (student/admin)
  - Error handling with toast notifications
  - Automatic navigation after auth
  - Responsive design

#### `frontend/src/pages/StudentDashboard.js`
**Student complaint portal:**
- **Stats cards**: Total, Pending, In Progress, Resolved
- **Complaint form**: 
  - Student name, category (optional), location, description
  - AI auto-categorization
  - Form toggle
- **Complaint list**:
  - Complaint history
  - Status badges
  - Priority badges
  - AI summary display
  - Timestamps
- Features:
  - Real-time complaint submission
  - AI analysis feedback
  - Filtered view (only user's complaints)

#### `frontend/src/pages/AdminDashboard.js`
**Admin management portal:**
- **Analytics stats**: Total, Pending, In Progress, Resolved
- **Charts**:
  - Bar chart: Complaints by category
  - Pie chart: Priority distribution
- **Complaints table**:
  - All complaints from all students
  - Sortable columns
  - Status dropdown (Pending/In Progress/Resolved)
  - Inline status updates
  - Student name, location, category display
- Features:
  - Real-time status updates
  - Comprehensive analytics
  - Role-based access (admin only)

#### `frontend/src/lib/utils.js`
**Utility functions:**
- `cn()` - Tailwind class merge utility using `clsx` and `tailwind-merge`
- Used throughout components for conditional styling

## 🎨 Design System

### Color Palette
- **Sidebar**: `#0F1115` (Dark Charcoal)
- **Main Background**: `#F9F9F7` (Warm Beige)
- **Primary/Gold**: `#D4A373`
- **Card Background**: `#FFFFFF`

### Status Colors
- **Pending**: Yellow (#FEF3C7 bg, #92400E text)
- **In Progress**: Blue (#DBEAFE bg, #1E40AF text)
- **Resolved**: Green (#DCFCE7 bg, #166534 text)

### Priority Colors
- **Low**: Gray
- **Medium**: Blue
- **High**: Red (#FEE2E2 bg, #991B1B text)

### Typography
- **Headings**: Manrope (600 weight)
- **Body**: Inter (400 weight)
- **Code**: JetBrains Mono

### Layout Principles
- Generous spacing (p-6, p-8, p-10)
- Rounded cards (rounded-xl)
- Soft shadows (shadow-sm, hover:shadow-md)
- Smooth transitions (duration-200, duration-300)

## 🔐 Authentication Flow

1. **Registration**:
   - User submits name, email, password, role
   - Backend hashes password with bcrypt
   - Creates user in MongoDB
   - Returns JWT token
   - Frontend stores token in localStorage
   - Redirects to appropriate dashboard

2. **Login**:
   - User submits email, password
   - Backend verifies credentials
   - Returns JWT token
   - Frontend stores token
   - Sets Axios default Authorization header
   - Redirects to dashboard

3. **Protected Routes**:
   - Frontend checks for token
   - Sends token in Authorization header
   - Backend validates JWT
   - Returns user data or 401

4. **Logout**:
   - Clears token from localStorage
   - Removes Authorization header
   - Redirects to login page

## 🤖 AI Integration Flow

1. **Complaint Submission**:
   - Student submits complaint
   - Backend receives description

2. **AI Analysis**:
   - Backend calls Gemini 3 Flash
   - Prompt: Analyze complaint for category, priority, summary
   - AI returns structured JSON

3. **Data Processing**:
   - Backend parses AI response
   - Stores AI analysis fields:
     - `ai_category`
     - `priority`
     - `summary`
   - Saves complaint to MongoDB

4. **Frontend Display**:
   - Shows AI-detected category
   - Displays priority badge
   - Shows AI-generated summary
   - Color-coded by priority

## 📊 Analytics System

### Admin Dashboard Analytics
1. **Status Breakdown**:
   - Count: Pending, In Progress, Resolved
   - Displayed in stat cards

2. **Category Analysis**:
   - Group complaints by AI category
   - Display in bar chart
   - Categories: Electrical, Cleaning, Internet, Maintenance, Other

3. **Priority Distribution**:
   - Count by priority level
   - Display in pie chart
   - Colors: Blue (Low), Orange (Medium), Red (High)

4. **Location Tracking**:
   - Track most problematic locations
   - Show top 5 locations
   - Display complaint count per location

## 🔄 State Management

### Global State (AuthContext)
- User authentication state
- Token management
- Login/logout functions

### Component State
- Form inputs
- Loading states
- Complaint lists
- Analytics data
- UI toggles (sidebar, forms)

## 🎯 Key Features Implemented

✅ Role-based authentication (Student/Admin)
✅ AI-powered complaint categorization
✅ Automatic priority detection
✅ Summary generation
✅ Status tracking (Pending/In Progress/Resolved)
✅ Admin complaint management
✅ Real-time analytics with charts
✅ Duplicate complaint detection
✅ Responsive design (mobile & desktop)
✅ Toast notifications
✅ Modern UI with warm aesthetic
✅ Protected routes
✅ JWT authentication
✅ MongoDB integration

## 🚀 Quick Start

1. **Setup Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your values
   uvicorn server:app --reload
   ```

2. **Setup Frontend**:
   ```bash
   cd frontend
   yarn install
   cp .env.example .env
   # Edit .env with your backend URL
   yarn start
   ```

3. **Access Application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8001
   - API Docs: http://localhost:8001/docs

## 📝 Testing

### Test Accounts
- **Student**: student@test.com / test123
- **Admin**: admin@test.com / admin123

### Test Scenarios
1. Register new accounts (both roles)
2. Submit complaints as student
3. Verify AI categorization
4. Login as admin
5. View all complaints
6. Update complaint status
7. Check analytics dashboard

## 🛠️ Technologies Used

**Backend:**
- FastAPI - Modern async Python web framework
- MongoDB - NoSQL database
- Motor - Async MongoDB driver
- Pydantic - Data validation
- JWT - Token authentication
- Gemini 3 Flash - AI analysis

**Frontend:**
- React 19 - UI library
- React Router - Navigation
- Tailwind CSS - Styling
- Shadcn UI - Component library
- Recharts - Data visualization
- Axios - HTTP client
- Sonner - Toast notifications

## 📦 Complete File List

```
✓ README.md
✓ PROJECT_STRUCTURE.md
✓ backend/server.py
✓ backend/requirements.txt
✓ backend/.env.example
✓ frontend/src/App.js
✓ frontend/src/App.css
✓ frontend/src/index.css
✓ frontend/tailwind.config.js
✓ frontend/package.json
✓ frontend/.env.example
✓ frontend/src/components/Sidebar.js
✓ frontend/src/contexts/AuthContext.js
✓ frontend/src/pages/LoginPage.js
✓ frontend/src/pages/StudentDashboard.js
✓ frontend/src/pages/AdminDashboard.js
✓ frontend/src/lib/utils.js
```

All files are ready to use! 🎉
