from fastapi import FastAPI, Depends
from config.config import initiate_database
from routes.admin import router as AdminRouter
from routes.member_copay import router as MemberCopayRouter
from routes.mock_api import router as MockApi
from auth.jwt_bearer import JWTBearer

app = FastAPI()

token_listener = JWTBearer()

@app.on_event("startup")
async def start_database():
    await initiate_database()

@app.get("/", tags=["Root"])
async def read_root():
    return { "Hello": "World!" }

app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin",)
app.include_router(MemberCopayRouter, tags=["MemberCopay"], prefix="/membercopay", dependencies=[Depends(token_listener)],)
app.include_router(MockApi, tags=["MockApi"], prefix="/mockapi",)
