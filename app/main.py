from fastapi import FastAPI
import httpx

app = FastAPI(title="Bybit Campaign Scanner", version="4.2-diagnostic")
BYBIT = "https://www.bybit.com"

@app.get("/")
async def root():
    return {"name":"Bybit Campaign Scanner","version":"4.2-diagnostic","status":"running","health":"/api/health","docs":"/docs"}

@app.get("/api/health")
async def health():
    return {"status":"ok","version":"4.2-diagnostic"}

async def bybit_post(path: str, payload: dict):
    try:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True, headers={"Accept":"application/json, text/plain, */*","Content-Type":"application/json","User-Agent":"Mozilla/5.0"}) as client:
            r = await client.post(BYBIT + path, json=payload)
            content_type = r.headers.get("content-type", "")
            body = r.text[:4000]
            if "application/json" in content_type:
                try:
                    body = r.json()
                except Exception:
                    pass
            return {"ok": r.is_success, "http_status": r.status_code, "content_type": content_type, "final_url": str(r.url), "body": body}
    except Exception as exc:
        return {"ok": False, "error_type": type(exc).__name__, "error": str(exc)}

@app.get("/api/campaign/{campaign_id}/{affiliate_id}")
async def campaign(campaign_id: int, affiliate_id: int):
    return await bybit_post("/x-api/affiliate/v5/campaign_info", {"campaign_id": campaign_id, "affiliate_id": affiliate_id})

@app.get("/api/discovery")
async def discovery():
    return await bybit_post("/x-api/v3/config/web", {"project_name":"web.futures","keys":["airdropCampaignConfig"]})
