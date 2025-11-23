# PRIYA MCP Server

MCP (Model Context Protocol) server for PRIYA voice agent. Serves 14 JSON modules containing conversation logic, behavioral protocols, and property data.

## 🚀 Quick Start

This server is designed to deploy automatically to Railway from GitHub.

### Prerequisites

- GitHub account
- Railway account (https://railway.app)
- Git installed locally

### Deployment

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - PRIYA MCP Server"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/priya-mcp-server.git
   git push -u origin main
   ```

2. **Deploy to Railway:**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `priya-mcp-server` repository
   - Railway will auto-detect Python and deploy
   - Your server will be live at: `https://your-app.railway.app`

3. **Configure Voice Agent:**
   - Set your voice agent's MCP base URL to: `https://your-app.railway.app`

## 📁 Repository Structure

```
priya-mcp-server/
├── server.py                           # Main MCP server application
├── requirements.txt                    # Python dependencies
├── Procfile                           # Railway deployment config
├── railway.json                       # Railway settings
├── .gitignore                         # Git ignore rules
├── README.md                          # This file
└── modules/                           # MCP JSON modules (14 files)
    ├── priya_r_module_tenant_inquiry.json          # CRITICAL: Emergency path
    ├── priya_r_module_vendor_inquiry.json
    ├── priya_r_module_landlord_inquiry.json
    ├── priya_r_module_tradesperson_inquiry.json
    ├── priya_r_module_professional_inquiry.json
    ├── priya_behavioral_protocols.json
    ├── priya_reactive_modules.json
    ├── priya_interruption_patterns.json
    ├── priya_frustration_patterns.json
    ├── priya_sales_listings.json
    ├── priya_rental_listings.json
    ├── priya_knowledge_base.json
    ├── speech_enhancement.json
    └── australian_patterns.json
```

## 🔌 API Endpoints

### `GET /`
API documentation and server info

### `GET /health`
Health check endpoint
```json
{
  "status": "healthy",
  "timestamp": "2025-11-23T...",
  "modules_available": 14
}
```

### `GET /modules`
List all available modules
```json
{
  "modules": ["priya_r_module_tenant_inquiry.json", ...],
  "count": 14
}
```

### `GET /module/<module_name>`
Get a specific module (with or without .json extension)

Example: `/module/priya_r_module_tenant_inquiry`

### `GET /module/<module_name>/content`
Get just the content field from a module

Example: `/module/priya_r_module_tenant_inquiry/content`

### `POST /reload`
Clear cache and reload modules from disk

## 🧪 Testing

After deployment, test your server:

```bash
# Health check
curl https://your-app.railway.app/health

# List modules
curl https://your-app.railway.app/modules

# Get tenant module (CRITICAL - contains emergency path)
curl https://your-app.railway.app/module/priya_r_module_tenant_inquiry
```

## 🚨 Critical Module

**`priya_r_module_tenant_inquiry.json`** contains the life-critical emergency path for:
- Gas leaks
- Floods
- Electrical hazards
- Other tenant emergencies

This module MUST be tested thoroughly before production use.

## 📊 Module Details

- **R-Modules (5):** Caller-type specific conversation flows
- **Behavioral (4):** Conversation protocols and patterns
- **Data (5):** Property listings and knowledge base

Total: 14 modules

## 🔧 Local Development

To run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python server.py

# Test locally
curl http://localhost:8080/health
```

## 🔒 Security

- Directory traversal protection enabled
- CORS enabled for voice agent access
- Input validation on all endpoints
- Comprehensive error handling

## 📝 Updating Modules

To update a module:

1. Edit the JSON file in `modules/` directory
2. Commit and push to GitHub
3. Railway auto-deploys the changes
4. Call `/reload` endpoint to clear cache (optional)

## 🌐 Environment Variables

Railway automatically sets:
- `PORT` - Server port (Railway managed)
- `RAILWAY_ENVIRONMENT` - Deployment environment

No manual configuration needed.

## 📈 Monitoring

- Health check: `GET /health`
- Module count: Check `modules_available` in health response
- Logs: View in Railway dashboard

## 🆘 Troubleshooting

**Modules not loading:**
- Check that all 14 JSON files are in `modules/` directory
- Verify file names (no `__3_` or `__2___2_` suffixes)
- Check Railway deployment logs

**500 errors:**
- Check Railway logs for stack traces
- Verify JSON file validity
- Call `/reload` to clear cache

## 📄 License

Proprietary - MK Group of Properties

## 👥 Contact

For support or questions about PRIYA voice agent deployment.

---

**Version:** 1.0.0  
**Last Updated:** November 23, 2025  
**Status:** Production Ready
