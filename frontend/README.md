# YouTube Trends Explorer - Frontend

A modern, interactive React-based frontend for the YouTube Trends Analysis Multi-Agent System.

## 🎨 Features

- **Beautiful Modern UI**: Built with React, TailwindCSS, and Framer Motion
- **Real-time Query Processing**: Interactive search with AI-powered responses
- **Smart Example Queries**: Pre-loaded examples to get started quickly
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Agent Transparency**: See which AI agents processed your query
- **Rich Results Display**: Beautiful cards with video statistics and metadata
- **System Monitoring**: Real-time health status and system information

## 🛠️ Tech Stack

- **Framework**: React 18 with Vite
- **Styling**: TailwindCSS with custom design system
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast
- **Charts**: Recharts (for future visualizations)

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running on `http://localhost:8000`

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
copy .env.example .env
```

4. Start the development server:
```bash
npm run dev
```

5. Open your browser to `http://localhost:5173`

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/              # Reusable UI components
│   │   │   ├── Card.jsx
│   │   │   ├── Button.jsx
│   │   │   ├── Badge.jsx
│   │   │   └── Input.jsx
│   │   ├── QueryInput.jsx   # Search input with examples
│   │   └── ResultsDisplay.jsx # Results visualization
│   ├── services/
│   │   └── api.js           # API client
│   ├── utils/
│   │   └── cn.js            # Utility functions
│   ├── App.jsx              # Main application
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles
├── public/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 🎯 Usage

### Basic Query

1. Type your question in the search bar
2. Click "Search" or press Enter
3. View AI-generated answer and detailed results

### Example Queries

The UI provides categorized example queries:

- **SQL/Analytical**: "Which category has the most trending videos?"
- **Vector/Semantic**: "Find videos about cooking tutorials"
- **Hybrid**: "Most popular gaming videos about Minecraft"

### System Information

Click the "System Info" button to view:
- Available AI agents
- System configuration
- Database connections
- LLM model details

## 🎨 Customization

### Theme Colors

Edit `tailwind.config.js` to customize the color scheme:

```js
theme: {
  extend: {
    colors: {
      primary: "hsl(221.2 83.2% 53.3%)",
      // ... other colors
    }
  }
}
```

### API Endpoint

Update `.env` to change the backend URL:

```env
VITE_API_URL=http://localhost:8000
```

## 📦 Build for Production

```bash
npm run build
```

The optimized build will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## 🔧 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Code Style

The project uses:
- ESLint for code quality
- Prettier-compatible formatting
- Tailwind CSS class ordering

## 🌐 API Integration

The frontend communicates with the backend via REST API:

### Endpoints Used

- `GET /health` - Health check
- `POST /query` - Process user query
- `GET /system/info` - Get system information
- `GET /examples` - Get example queries

### API Client

Located in `src/services/api.js`:

```javascript
import { apiService } from '@/services/api';

// Process a query
const response = await apiService.processQuery(query);

// Check health
const health = await apiService.checkHealth();
```

## 🎭 Components

### QueryInput

Search bar with example queries and loading states.

```jsx
<QueryInput
  onSubmit={handleQuery}
  isLoading={isLoading}
  examples={examples}
/>
```

### ResultsDisplay

Displays AI-generated answers and video results.

```jsx
<ResultsDisplay response={response} />
```

### UI Components

Reusable components following shadcn/ui patterns:
- `Card`, `CardHeader`, `CardTitle`, `CardContent`
- `Button` with variants (default, outline, ghost, etc.)
- `Badge` for labels and tags
- `Input` for form fields

## 🚨 Troubleshooting

### Backend Connection Issues

If you see "Failed to connect to backend":
1. Ensure backend is running on `http://localhost:8000`
2. Check CORS settings in backend
3. Verify `.env` file has correct API URL

### Build Errors

If you encounter build errors:
1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again
3. Clear Vite cache: `rm -rf node_modules/.vite`

### Styling Issues

The CSS warnings about `@tailwind` and `@apply` are expected - these are TailwindCSS directives that are processed by PostCSS during build time. They will work correctly when you run the app.

## 📄 License

MIT License - Same as parent project

## 🤝 Contributing

1. Follow the existing code style
2. Use meaningful component and variable names
3. Add comments for complex logic
4. Test on multiple screen sizes
5. Ensure accessibility (ARIA labels, keyboard navigation)

## 🔗 Related Documentation

- [Backend API Documentation](../README.md)
- [Multi-Agent System Guide](../MULTI_AGENT_SETUP.md)
- [Vite Documentation](https://vitejs.dev/)
- [TailwindCSS Documentation](https://tailwindcss.com/)
