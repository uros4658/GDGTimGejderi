from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
import os
API_KEY = os.getenv("API_KEY", "hackathon42")

def verify_api_key(request: Request):
    key = request.headers.get("X-API-KEY")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

class APIKeyRoute(APIRoute):
    def get_route_handler(self):
        original = super().get_route_handler()

        async def custom_route_handler(request: Request):
            verify_api_key(request)
            return await original(request)

        return custom_route_handler
