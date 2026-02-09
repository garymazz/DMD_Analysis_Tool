from cement import Controller
from pydantic import BaseModel
from typing import Type, Optional, Any, get_args, get_origin, Union

class BaseOperationController(Controller):
    """
    Base Controller for all DMD Operations.
    Inheriting from Controller ensures these appear as CLI sub-commands.
    """
    class Meta:
        # This is just a base class, not a registered handler itself
        label = 'base_op'
        stacked_on = 'base'
        stacked_type = 'nested'

        # Custom fields for our "registry" help
        help_detailed = "Detailed help"
        help_op_specific = "Op specific help"
        param_model: Optional[Type[BaseModel]] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        meta = getattr(cls, 'Meta', None)
        if not meta:
            return
        param_model = getattr(meta, 'param_model', None)
        if not param_model:
            return
        if getattr(meta, 'arguments', None):
            return
        meta.arguments = cls.arguments_from_model(param_model)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.console = kw.get('console')
        # In Cement controllers, we often access app.render or print directly.
        # But we'll stick to self.app.console if available or kw.

    def get_params(self):
        if not self.Meta.param_model: return None
        # Access arguments from self.app.pargs
        raw_args = self.app.pargs.__dict__
        try:
            fields = self.Meta.param_model.model_fields.keys()
        except AttributeError:
            fields = self.Meta.param_model.__fields__.keys()

        filtered = {k: v for k, v in raw_args.items() if k in fields}
        return self.Meta.param_model(**filtered)

    @staticmethod
    def arguments_from_model(param_model: Type[BaseModel]):
        fields = getattr(param_model, 'model_fields', None) or getattr(param_model, '__fields__', {})
        arguments = []
        for name, field in fields.items():
            arg_spec = BaseOperationController._build_argument_spec(name, field)
            if arg_spec:
                arguments.append(arg_spec)
        return arguments

    @staticmethod
    def _build_argument_spec(name: str, field: Any):
        alias = getattr(field, 'alias', None) or name
        flag = f"--{alias.replace('_', '-')}"
        description = BaseOperationController._field_description(field) or "No description"
        default = BaseOperationController._field_default(field)
        required = BaseOperationController._field_required(field)
        field_type = BaseOperationController._field_type(field)
        base_type = BaseOperationController._unwrap_optional(field_type)

        arg_config: dict[str, Any] = {'help': description, 'dest': name}
        if base_type is bool:
            arg_config['action'] = 'store_true' if not default else 'store_false'
        else:
            arg_config['action'] = 'store'
            if base_type in {int, float, str}:
                arg_config['type'] = base_type
            if required:
                arg_config['required'] = True
            if default not in {None, ...} and not BaseOperationController._is_undefined_default(default):
                arg_config['default'] = default

        return ([flag], arg_config)

    @staticmethod
    def _field_description(field: Any) -> Optional[str]:
        description = getattr(field, 'description', None)
        if description:
            return description
        field_info = getattr(field, 'field_info', None)
        if field_info:
            return getattr(field_info, 'description', None)
        return None

    @staticmethod
    def _field_default(field: Any):
        return getattr(field, 'default', None)

    @staticmethod
    def _field_required(field: Any) -> bool:
        if hasattr(field, 'is_required'):
            return field.is_required()
        return bool(getattr(field, 'required', False))

    @staticmethod
    def _field_type(field: Any):
        field_type = getattr(field, 'annotation', None)
        if field_type is not None:
            return field_type
        return getattr(field, 'outer_type_', None) or getattr(field, 'type_', None)

    @staticmethod
    def _unwrap_optional(field_type: Any):
        origin = get_origin(field_type)
        if origin is Union:
            args = [arg for arg in get_args(field_type) if arg is not type(None)]
            if len(args) == 1:
                return args[0]
        return field_type

    @staticmethod
    def _is_undefined_default(value: Any) -> bool:
        return type(value).__name__ in {'PydanticUndefinedType', 'UndefinedType'}
