from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
import os
import logging

from config import logger, REPORTS_DIR
from excel_service import create_excel_report
from data_service import get_total
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://bank.ocean00.com","http://bank.ocean00.com"],  # Allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


class ReportRequest(BaseModel):
    start_date: str = None  # Format: YYYY-MM-DD
    end_date: str = None    # Format: YYYY-MM-DD
    
    def get_date_range(self):
        """Convert date strings to proper datetime format with time"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Use provided dates or default to today
        start = self.start_date or today
        end = self.end_date or today
        
        # Add time component
        start_datetime = f"{start} 00:00:00"
        end_datetime = f"{end} 23:59:59"
        
        return (start_datetime, end_datetime)

@app.post("/generate-excel")
async def generate_excel(request: ReportRequest, background_tasks: BackgroundTasks):
    try:
        report_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        date_range = request.get_date_range()
        
        # Check if data exists for the date range by getting the totals
        try:
            totals = get_total(date_range)
            
            # If all totals are 0, there's no data for the report
            if totals["grand_total"] == 0:
                return {
                    "status": "no_data",
                    "message": "No transaction data available for the selected date range",
                    "date_range": {
                        "start_date": request.start_date or datetime.now().strftime('%Y-%m-%d'),
                        "end_date": request.end_date or datetime.now().strftime('%Y-%m-%d')
                    }
                }
        except Exception as e:
            logger.error(f"Error checking data existence: {str(e)}")
            # Continue with report generation if we can't verify data existence
            
        logger.info(f"Starting background task for report_id: {report_id} with date range: {date_range}")
        background_tasks.add_task(create_excel_report, report_id, date_range)
        
        return {
            "status": "processing",
            "report_id": report_id,
            "message": "Report generation started",
            "date_range": {
                "start_date": request.start_date or datetime.now().strftime('%Y-%m-%d'),
                "end_date": request.end_date or datetime.now().strftime('%Y-%m-%d')
            }
        }
    except Exception as e:
        logger.error(f"Error in generate-excel endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report-status/{report_id}")
async def check_status(report_id: str):
    try:
        filepath = os.path.join(REPORTS_DIR, f"financial_report_{report_id}.xlsx")
        
        if os.path.exists(filepath):
            return {
                "status": "completed",
                "filename": f"financial_report_{report_id}.xlsx",
                "download_url": f"/reports/financial_report_{report_id}.xlsx"
            }
        return {
            "status": "processing"
        }
    except Exception as e:
        logger.error(f"Error checking report status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Optional: Add an endpoint to serve the reports
@app.get("/reports/{filename}")
async def get_report(filename: str):
    filepath = os.path.join(REPORTS_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Return the file as a downloadable attachment
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)