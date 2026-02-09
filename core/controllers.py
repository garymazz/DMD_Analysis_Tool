from cement import Controller
from pydantic import BaseModel
from typing import Type, Optional

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
