from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.core.config import configs
from app.core.exceptions import DuplicatedError, NotFoundError
from app.util.query_builder import dict_to_sqlalchemy_filter_options


class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], model) -> None:
        self.session_factory = session_factory
        self.model = model

    def read_by_options(self, schema, eager=False):
        with self.session_factory() as session:
            schema_as_dict = schema.model_dump(exclude_none=True)
            ordering = schema_as_dict.get("ordering", configs.ORDERING)
            order_query = (
                getattr(self.model, ordering[1:]).desc()
                if ordering.startswith("-")
                else getattr(self.model, ordering).asc()
            )
            page = int(schema_as_dict.get("page") or configs.PAGE)
            page_size_raw = schema_as_dict.get("page_size") or configs.PAGE_SIZE
            page_size = page_size_raw if page_size_raw == "all" else int(page_size_raw)
            filter_options = dict_to_sqlalchemy_filter_options(self.model, schema.model_dump(exclude_none=True))
            query = session.query(self.model)
            
            if eager:
                for eager in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager)))
            
            filtered_query = query.filter(filter_options)
            query = filtered_query.order_by(order_query)
            
            if page_size == "all":
                query = query.all()
            else:
                query = query.limit(page_size).offset((page - 1) * page_size).all()
            
            total_count = filtered_query.count()
            return {
                "founds": query,
                "search_options": {
                    "page": page,
                    "page_size": page_size,
                    "ordering": ordering,
                    "total_count": total_count,
                },
            }

    def read_by_id(self, id: int, eager=False):
        with self.session_factory() as session:
            query = session.query(self.model)
            if eager:
                for eager in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager)))
            query = query.filter(self.model.id == id).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {id}")
            return query

    def create(self, schema):
        with self.session_factory() as session:
            new_object = self.model(**schema.model_dump(exclude_none=True)) # Распаковываем схему в модель БД
            try:
                session.add(new_object)
                session.commit()
                session.refresh(new_object) # Обновляем объект, чтобы у него появился id из базы
            except IntegrityError as e:
                raise DuplicatedError(detail="Record with this unique attribute already exists.")
            return new_object

    def update(self, id: int, schema):
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update(schema.dict(exclude_none=True))
            session.commit()
            return self.read_by_id(id)

    def update_attr(self, id: int, column: str, value):
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update({column: value})
            session.commit()
            return self.read_by_id(id)

    def whole_update(self, id: int, schema):
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update(schema.dict())
            session.commit()
            return self.read_by_id(id)

    def delete_by_id(self, id: int):
        with self.session_factory() as session:
            object = session.query(self.model).filter(self.model.id == id).first()
            if not object:
                raise NotFoundError(detail=f"not found id : {id}")
            try:
                session.delete(object)
                session.commit()
            except IntegrityError:
                session.rollback()
                raise DuplicatedError(detail="Cannot delete: record is referenced by other data. Remove related records first.")
