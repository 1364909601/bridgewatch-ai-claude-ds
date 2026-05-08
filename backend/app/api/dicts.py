from fastapi import APIRouter, Depends

from app.schemas.dicts import DictItem
from app.services.dict_service import DictService
from app.utils.response import success_response

router = APIRouter()


@router.get("/{dict_type}")
async def get_dict(dict_type: str):
    """获取数据字典（按类型）"""
    data = DictService.get_dict(dict_type)
    return success_response(data)
