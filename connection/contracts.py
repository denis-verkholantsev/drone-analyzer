from pydantic import BaseModel
from caseconverter import camelcase
from fastapi import Body
from typing import Annotated
from uuid import UUID



class PostOrderRequest(BaseModel, alias_generator=camelcase, populate_by_name=True):
    dest: str
    task: str
    extra_info: dict[str, str]
    
    def to_order_info(self) -> "OrderInfo":
        return OrderInfo(dest=self.dest, task=self.task, extra_info=self.extra_info)


class OrderInfo(BaseModel):
    dest: str
    task: str
    extra_info: dict[str, str]

PostOrderRequestBody = Annotated[PostOrderRequest, Body()]


