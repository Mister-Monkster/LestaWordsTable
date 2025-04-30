import json
from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Query
from fastapi.templating import Jinja2Templates


from depends.depends import ServiceDep

router = APIRouter(prefix="/file")
templates = Jinja2Templates(directory='../src/templates')


@router.get('/download', summary='Загрузка файла')
async def get_students_html(request: Request):
    return templates.TemplateResponse(name='form.html', context={'request': request})


@router.post("/table/{page_num}", summary='Обработка файла')
async def download_file(request: Request, service: ServiceDep, file: UploadFile = File()):
    res = await service.download(file)
    if res:
        return templates.TemplateResponse(name='table.html',
                                          context={'request': request,
                                                   'data': res})
    else:
        raise HTTPException(status_code=422, detail="Unprocessable Entity")







