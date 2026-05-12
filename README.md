# NAFDAC Greenbook Scraper API

A FastAPI-based web scraper for querying the NAFDAC Greenbook drug registry by Registration Number.

## Local Development

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository and navigate to the project folder**
   ```bash
   cd web-scrape
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server locally**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`
   - **API Docs**: http://localhost:8000/docs
   - **Alternative Docs**: http://localhost:8000/redoc

## API Endpoint

### GET `/api/drugs`

**Query Parameters:**
- `nrn` (required): NAFDAC Registration Number (e.g., `04-6969`)

**Example Request:**
```bash
curl "http://localhost:8000/api/drugs?nrn=04-6969"
```

**Response:**
```json
{
  "success": true,
  "count": 1,
  "data": [
    {
      "Product Name": "Funbact-A Cream",
      "Active Ingredients": "Betamethasone; Clotrimazole; Neomycin sulfate",
      "Product Category": "Drugs",
      "NAFDAC Reg No": "04-6969",
      "Form": "Cream",
      "Route of Administration": "Topical",
      "Strengths": "0.1%; 1%; 5%",
      "Applicant Name": "Bliss GVS Pharma Limited",
      "Approval Date": "2024-05-15",
      "Status": "Active"
    }
  ]
}
```

## Deploying to Render

### Step 1: Push to GitHub
1. Initialize a git repository in your project folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: NAFDAC Scraper API"
   git remote add origin https://github.com/YOUR_USERNAME/nafdac-scraper.git
   git push -u origin main
   ```

### Step 2: Create a Render Account
1. Go to [https://render.com](https://render.com)
2. Sign up with your GitHub account or email
3. Authorize Render to access your GitHub repositories

### Step 3: Create a New Web Service
1. Click **"+ New"** and select **"Web Service"**
2. Connect your GitHub repository containing this code
3. Configure the service:
   - **Name**: `nafdac-scraper` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Build Command**: `bash build.sh`
   - **Start Command**: `python main.py`
4. Click **"Create Web Service"**

### Step 4: Monitor Deployment
- Render will build and deploy your service automatically
- You'll get a public URL like: `https://nafdac-scraper.onrender.com`
- Monitor logs in the Render dashboard

### Step 5: Test Your Deployment
Once deployed, test your API:
```bash
curl "https://nafdac-scraper.onrender.com/api/drugs?nrn=04-6969"
```

**Important Note on Cold Starts:**
- Free tier Render services spin down after 15 minutes of inactivity
- The first request after spin-down may take 30-60 seconds to respond
- Upgrade to a paid plan for always-on services

## Using the API from Your Project

### JavaScript/Fetch
```javascript
async function getDrug(nrn) {
  const response = await fetch(`https://nafdac-scraper.onrender.com/api/drugs?nrn=${nrn}`);
  return await response.json();
}

getDrug("04-6969").then(console.log);
```

### Python/Requests
```python
import requests

response = requests.get("https://nafdac-scraper.onrender.com/api/drugs", params={"nrn": "04-6969"})
data = response.json()
print(data)
```

### cURL
```bash
curl "https://nafdac-scraper.onrender.com/api/drugs?nrn=04-6969"
```

## Troubleshooting

### "Build failed" error
- Check that `requirements.txt` exists in the root directory
- Ensure `build.sh` has Unix line endings (not Windows CRLF)

### Service keeps spinning down
- Upgrade to a paid Render plan for persistent hosting
- Or add a uptime monitor using services like Kping.io

### Chrome driver issues on Render
- The `webdriver-manager` package should handle driver downloads automatically
- If issues persist, ensure sufficient free disk space in your Render instance

## License
MIT