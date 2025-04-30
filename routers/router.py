import json
from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Query, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.util import await_only
from starlette.responses import RedirectResponse

from depends.depends import ServiceDep

router = APIRouter(prefix="/file")
templates = Jinja2Templates(directory='../src/templates')


@router.get('/download', summary='Загрузка файла')
async def get_students_html(request: Request):
    return templates.TemplateResponse(name='form.html', context={'request': request})


@router.post("/table/{filename}/{page_num}", summary='Обработка файла')
async def download_file(request: Request, service: ServiceDep, filename: str, file: UploadFile = File(), page_num: int = 1):
    res = await service.download(file, filename)
    total_pages = (len(res) + 49) // 50
    if res:
        return templates.TemplateResponse(name='table.html',
                                          context={'request': request,
                                                   'data': res[0: 50],
                                                   "total_pages": total_pages,
                                                   "filename": filename,
                                                   "page_num": page_num
        })
    else:
        raise HTTPException(status_code=422, detail="Unprocessable Entity")


@router.get("/table/{filename}/{page_num}", summary='Обработка файла')
async def download_file(request: Request, service: ServiceDep, filename: str, page_num: int = 1):
    try:
        res = await service.read_file(filename, page_num)
        data = res['content']
        total_pages = res['total_pages']
        return templates.TemplateResponse(name='table.html',
                                          context={'request': request,
                                                   'data': data,
                                                   "total_pages": total_pages,
                                                   "filename": filename,
                                                   'page_num': page_num
        })
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")









