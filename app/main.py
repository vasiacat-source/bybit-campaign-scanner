from fastapi import FastAPI
import httpx

app = FastAPI(title="Bybit Campaign Scanner", version="4.1-live")
BYBIT = "https://www.bybit.com"

@app.get("/")
async def root():
    return {"name":"Bybit Campaign Scanner","version":"4.1-live","status":"running","health":"/api/health","docs":"/docs"}

@app.get("/api/health")
async def health():
    return {"status":"ok","version":"4.1-live"}

@app.get("/api/campaign/{campaign_id}/{affiliate_id}")
async def campaign(campaign_id: int, affiliate_id: int):
    async with httpx.AsyncClient(timeout=20, headers={"Accept":"application/json","Content-Type":"application/json","User-Agent":"Mozilla/5.0"}) as client:
        r = await client.post(BYBIT + "/x-api/affiliate/v5/campaign_info", json={"campaign_id":campaign_id,"affiliate_id":affiliate_id})
        return {"http_status":r.status_code,"data":r.json()}

@app.get("/api/discovery")
async def discovery():
    async with httpx.AsyncClient(timeout=20, headers={"Accept":"application/json","Content-Type":"application/json","User-Agent":"Mozilla/5.0"}) as client:
        r = await client.post(BYBIT + "/x-api/v3/config/web", json={"project_name":"web.futures","keys":["airdropCampaignConfig"]})
        return {"http_status":r.status_code,"data":r.json()}
