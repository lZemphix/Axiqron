from dataclasses import dataclass
from typing import Any
from common.utils.struct import StatusCodesEnum


@dataclass
class Result:
    message: str = None
    result: Any = None
    status: StatusCodesEnum = StatusCodesEnum.OK
