from pydantic import BaseModel
from caseconverter import camelcase
from fastapi import Body
from typing import Annotated
from dataclasses import dataclass
from uuid import UUID



class PostOrderRequest(BaseModel, alias_generator=camelcase, populate_by_name=True):
    source: str
    dest: str
    extra_info: dict[str, str]

    
    def to_order_info(self) -> "OrderInfo":
        return OrderInfo(source=self.source, dest=self.dest, extra_info=self.extra_info)



class OrderInfo(BaseModel):
    source: str
    dest: str
    extra_info: dict[str, str]

PostOrderRequestBody = Annotated[PostOrderRequest, Body()]


