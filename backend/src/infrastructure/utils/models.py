from dataclasses import dataclass
from typing import Optional, Type, Any, Tuple
from copy import deepcopy
import inspect

from fastapi import Form
from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


def partial_model(model: Type[BaseModel]):
    def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new
    return create_model(
        f'Partial{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        }
    )

def to_form(cls: type[BaseModel]) -> type:
    form_keys = inspect.signature(Form).parameters.keys()
    model = type('Model', (object,), {
        "__annotations__": cls.__annotations__,
        **{
            field: Form(
                **{slot: getattr(info, slot) for slot in info.__slots__ if slot in form_keys},
                **{
                    metadata.__slots__[0]: getattr(metadata, metadata.__slots__[0])
                    for metadata in info.metadata
                    if metadata.__slots__[0] in form_keys
                }
            )
            for field, info in cls.model_fields.items()
        }
    })
    return dataclass(model)