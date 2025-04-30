from typing import Annotated

from fastapi import Depends

from services.service import FileService



async def get_service() -> FileService:
    return FileService()

ServiceDep = Annotated[FileService, Depends(get_service)]
