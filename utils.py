import json
import os
import time
import requests

import aiohttp
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

COMMON_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://app.haiper.ai/",
    "Origin": "https://app.haiper.ai",
    "x-haiper-client": "webapp",
	"x-haiper-version": "v0.4.13-8-gc7be636c-20240502",
	"x-vision-env": "pro"
}


async def fetch(url, headers=None, data=None, method="POST"):
    if headers is None:
        headers = {}
    headers.update(COMMON_HEADERS)
    if not headers.get("Content-Type"):
        headers.update({"Content-Type": "application/json;charset=UTF-8"})
        if data is not None:
            data = json.dumps(data)

    print(data, method, headers, url)

    proxy = os.getenv("PROXY_ADDRESS") if int(os.getenv("REQUEST_USE_PROXY")) else None

    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                method=method, url=url, data=data, headers=headers, proxy=proxy
            ) as resp:
                resp.raise_for_status()
                if resp.content_length == 0 and resp.status == 200:
                    return
                return await resp.json()
        except Exception as e:
            return {f"An error occurred: {e}"}

#查询用户ID
async def get_user_id(token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/user/me"
    response = await fetch(api_url, headers, method="GET")
    return response

#查询用户配置信息
async def get_user_profile(token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/user/profile"
    response = await fetch(api_url, headers, method="GET")
    return response

#查询默认样式
async def get_styles(token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/jobs/styles"
    response = await fetch(api_url, headers, method="GET")
    return response

#查询用户作业列表
async def get_jobs(start, limit, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/jobs?start={start}&limit={limit}"
    response = await fetch(api_url, headers, method="GET")
    return response

#上传文件接口
'''
response:
{
    "status": "success",
    "value": {
        "url": "https://storage.googleapis.com/haiper_vb/u/662fd23eb66ade4501f0bd5b/2024-05-07T07-09-16-98a04634.png?GoogleAccessId=firebase-adminsdk-evjp9%40internal-testing-tool.iam.gserviceaccount.com&Expires=1715066357&Signature=AS%2FWhZ3XLeCxWVaCu5mAzvMNH8na37pqNjIBgHzIFm2XEnFzmKM768YDuOX0yl9sBU6jq1MGaCdA8dDRGKaLq7iCpsbrKIjK%2FtamaVCbuCdBVa8xleKtf%2B6rYPONNWRxwZubiSTeWYuwVplE2QXcukZbc5flNHijaGn4IJtvtO5rpRJBi9%2BVZgprM%2B0mpL3uivfuc%2BGQ2aWcAAIilnFf610B0HFmFpfMO196x3eUG27A3HGpWdLHu61lZO8JhOuFpaJyBMQpg46jSoePnrw29MxbfexHT6MNJUN3aXUFlGKkbSfskVDhhPAoBPXe4w28ak1YfdrwUB8xQgNwBTw3xw%3D%3D",
        "key": "gs://haiper_vb/u/662fd23eb66ade4501f0bd5b/2024-05-07T07-09-16-98a04634.png"
    }
}
'''
async def upload_url(param, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    api_url = f"{BASE_URL}/jobs/upload-url"
    response = await fetch(api_url, headers, data=param, method="POST")
    return response

#上传文件
async def upload_file(filename, content_type, upload_url, token):
    headers = {
        "Content-Type": content_type,
        "Authorization": f"Bearer {token}"
    }
    api_url = upload_url.get("value").get("url")
    with open(filename, 'rb') as f:
        data = f.read()
        response = await fetch(api_url, headers, data=data, method="PUT")
        return response

#查询生成状态
async def get_status(ids, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/jobs/{ids}/status"
    response = await fetch(api_url, headers, method="GET")
    return response

#查询生成的视频信息
async def get_video_detail(ids, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/creation/{ids}"
    response = await fetch(api_url, headers, method="GET")
    return response

#根据文本生成视频
async def generate_video_by_text(prompt, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/jobs/generation-v2"
    response = await fetch(api_url, headers, prompt)
    return response

#根据图像生成视频
async def generate_video_by_image(prompt, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/jobs/generation-v2"
    response = await fetch(api_url, headers, prompt)
    return response

#根据视频生成视频
async def generate_video_by_video(prompt, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/jobs/inpainting"
    response = await fetch(api_url, headers, prompt)
    return response

#下载视频
def download_video(video_url, destination_path):
    try:
        # 发送GET请求
        response = requests.get(video_url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        # 以二进制写入模式打开文件
        with open(destination_path, 'wb') as f:
            # 以块的形式写入文件，减少内存使用
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Video downloaded successfully to {destination_path}")
        return destination_path
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
    
    return None
