from fastapi import FastAPI, HTTPException, Query
from scraper import scrape_nafdac_by_nrn

app = FastAPI(
    title="NAFDAC Greenbook Scraper API",
    description="An API to search for drugs in the NAFDAC Greenbook using their Registration Number.",
    version="1.0.0"
)

@app.get("/api/drugs")
def get_drug_by_nrn(nrn: str = Query(..., description="The NAFDAC Registration Number (e.g., 04-6969)")):
    """
    Search for a drug on the NAFDAC Greenbook by its NAFDAC Registration Number (NRN).
    
    Returns a list of matching drugs with their full details.
    """
    try:
        if not nrn or len(nrn.strip()) == 0:
            raise HTTPException(status_code=400, detail="NRN parameter cannot be empty")
        
        results = scrape_nafdac_by_nrn(nrn)
        return {
            "success": True,
            "count": len(results),
            "data": results
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    import os
    # Render assigns a PORT environment variable dynamically
    port = int(os.environ.get("PORT", 8000))
    # Run the API on Render's assigned port (or 8000 locally)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)