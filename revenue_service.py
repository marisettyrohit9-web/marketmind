from datetime import datetime, timedelta

class RevenueService:
    def simulate_revenue(self, data: dict):
        try:
            visitors = data.get("visitors", 0)
            conversion_rate = data.get("conversion_rate", 0)
            aov = data.get("average_order_value", 0)
            ad_spend = data.get("ad_spend", 0) or 1 # Avoid division by zero

            leads = visitors * (conversion_rate / 100)
            revenue = leads * aov
            roas = revenue / ad_spend if ad_spend > 0 else 0

            # 3 Month Projection (5% monthly growth)
            projections = []
            current_date = datetime.now()
            
            for i in range(3):
                growth_factor = (1.05) ** i
                proj_revenue = revenue * growth_factor
                proj_month = (current_date + timedelta(days=30*i)).strftime("%b %Y")
                
                projections.append({
                    "month": proj_month,
                    "revenue": round(proj_revenue, 2),
                    "growth": f"+{int((growth_factor - 1) * 100)}%" if i > 0 else "Base"
                })

            return {
                "current_performance": {
                    "leads": int(leads),
                    "revenue": round(revenue, 2),
                    "roas": round(roas, 2)
                },
                "projections": projections,
                "graph_data": {
                    "labels": [p["month"] for p in projections],
                    "datasets": [
                        {
                            "label": "Projected Revenue",
                            "data": [p["revenue"] for p in projections]
                        }
                    ]
                }
            }

        except Exception as e:
            return {"error": f"Display simulation failed: {str(e)}"}

revenue_service = RevenueService()
