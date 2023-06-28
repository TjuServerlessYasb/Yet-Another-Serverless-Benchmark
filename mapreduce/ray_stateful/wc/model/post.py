from pydantic import BaseModel


class PostStr(BaseModel):
    input_str: str

class PostBodyMap(BaseModel):
    input_name: str
    input_part: int
    reduce_num: int



class PostBodyReduce(BaseModel):
    input_name: str
    input_num: int
    reduce_part: int
