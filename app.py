# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import hira
import nhic

description = """
공동인증서 / 간편인증(네이버, 카카오)기반 건강보험공단 및 보건복지부 면허민원 스크래핑 API"""

app = FastAPI(
    title="건강보험공단 및 보건복지부 면허민원 API",
    description=description,
    version="0.0.1",
)

# app.include_router(mohw.router)
# mohw.exceptions.add_exception_handler(app)
app.include_router(hira.router)
hira.exceptions.add_exception_handler(app)

app.include_router(nhic.router)
# nhic.exceptions.add_exception_handler(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
