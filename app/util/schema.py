from pydantic._internal._model_construction import ModelMetaclass

class AllOptional(ModelMetaclass):
    def __new__(mcs, name, bases, namespaces, **kwargs):
        # Создаем класс с помощью базового метакласса Pydantic v2
        cls = super().__new__(mcs, name, bases, namespaces, **kwargs)
        
        # Обходим все определенные в модели поля Pydantic v2
        for field_info in cls.model_fields.values():
            # Если у поля не задано значение по умолчанию, делаем его None
            if field_info.default == field_info.default_factory:
                field_info.default = None
                
        # Пересобираем модель с учетом обновленных дефолтов
        cls.model_rebuild(force=True)
        return cls