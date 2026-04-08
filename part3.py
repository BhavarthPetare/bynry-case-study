from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta

app = FastAPI()

class SupplierInfo(BaseModel):
    id: int
    name: str
    contact_email: EmailStr

class LowStockAlert(BaseModel):
    product_id: int
    product_name: str
    sku: str
    warehouse_id: int
    warehouse_name: str
    current_stock: int
    threshold: int
    days_until_stockout: Optional[int]
    supplier: SupplierInfo

class AlertResponse(BaseModel):
    alerts: List[LowStockAlert]
    total_alerts: int

@app.get("/api/companies/{company_id}/alerts/low-stock", response_model=AlertResponse)
async def get_low_stock_alerts(company_id: int = Path(..., gt=0)):
    """
    Retrieves low-stock alerts based on warehouse inventory, 
    product-specific thresholds, and recent sales activity.
    """
    recently_active_products = [123, 124] 

    alerts = []
    mock_data = [
        {
            "product_id": 123,
            "product_name": "Widget A",
            "sku": "WID-001",
            "warehouse_id": 456,
            "warehouse_name": "Main Warehouse",
            "current_stock": 5,
            "threshold": 20,
            "daily_sales_velocity": 0.4, 
            "supplier": {
                "id": 789,
                "name": "Supplier Corp",
                "contact_email": "orders@supplier.com"
            }
        }
    ]

    for item in mock_data:
        if item["current_stock"] < item["threshold"] and item["product_id"] in recently_active_products:
            
            days_left = int(item["current_stock"] / item["daily_sales_velocity"]) if item["daily_sales_velocity"] > 0 else None
            
            alerts.append(LowStockAlert(
                product_id=item["product_id"],
                product_name=item["product_name"],
                sku=item["sku"],
                warehouse_id=item["warehouse_id"],
                warehouse_name=item["warehouse_name"],
                current_stock=item["current_stock"],
                threshold=item["threshold"],
                days_until_stockout=days_left,
                supplier=SupplierInfo(**item["supplier"])
            ))

    return AlertResponse(alerts=alerts, total_alerts=len(alerts))
