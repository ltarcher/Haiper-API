# -*- coding:utf-8 -*-

import json

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

import schemas
from deps import get_token
from utils import generate_video_by_text, get_status, get_video_detail,get_styles, get_user_profile, get_jobs, get_user_id
from utils import upload_url, upload_file, download_video, generate_video_by_image, generate_video_by_video

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_root():
    return schemas.Response()

@app.get("/user/me")
async def api_get_user_id(token: str = Depends(get_token)):
    try:
        resp = await get_user_id(token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.get("/user/profile")
async def api_user_profile(token: str = Depends(get_token)):
    try:
        resp = await get_user_profile(token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.get("/jobs/styles")
async def api_get_styles(token: str = Depends(get_token)):
    try:
        resp = await get_styles(token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.get("/jobs")
async def api_get_generate_jobs(start: str, limit: int, token: str = Depends(get_token)):
    try:
        resp = await get_jobs(start, limit, token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.post("/jobs/upload_url")
async def api_upload_url(param: schemas.UploadParam, token: str = Depends(get_token)):
    try:
        resp = await upload_url(param.dict(), token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.put("/jobs/upload_file")
async def api_upload_file(filename: str, content_type: str, upload_url: schemas.UploadResponse,  token: str = Depends(get_token)):
    try:
        resp = await upload_file(filename, content_type, upload_url.dict(), token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@app.get("/jobs/download_file")
async def api_download_file(url: str, destpath: str):
    try:
        resp = await download_video(url, destpath)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.get("/{vid}/status")
async def api_generate_status(vid: str, token: str = Depends(get_token)):
    try:
        resp = await get_status(vid, token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.get("/{vid}/detail")
async def api_generate_detail(vid: str, token: str = Depends(get_token)):
    try:
        resp = await get_video_detail(vid, token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.post("/generate/video_by_text")
async def api_generate_video_by_text(data: schemas.DescriptionTextGenerateParam, request: Request, token: str = Depends(get_token)):
    req = await request.json()
    prompt = req.get("prompt")
    if prompt is None:
        raise HTTPException(
            detail="prompt is required", status_code=status.HTTP_400_BAD_REQUEST
        )

    try:
        resp = await generate_video_by_text(data.dict(), token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.post("/generate/video_by_image")
async def api_generate_video_by_image(data: schemas.DescriptionImageGenerateParam, request: Request, token: str = Depends(get_token)):
    req = await request.json()
    prompt = req.get("prompt")
    if prompt is None:
        raise HTTPException(
            detail="prompt is required", status_code=status.HTTP_400_BAD_REQUEST
        )

    try:
        resp = await generate_video_by_image(data.dict(), token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@app.post("/generate/video_by_video")
async def api_generate_video_by_video(data: schemas.DescriptionVideoGenerateParam, request: Request, token: str = Depends(get_token)):
    req = await request.json()
    prompt = req.get("prompt")
    if prompt is None:
        raise HTTPException(
            detail="prompt is required", status_code=status.HTTP_400_BAD_REQUEST
        )

    try:
        resp = await generate_video_by_video(data.dict(), token)
        return resp
    except Exception as e:
        raise HTTPException(
            detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )