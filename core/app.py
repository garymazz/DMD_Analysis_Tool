from cement import App, Controller
from rich.console import Console
import sys

RICH_CONSOLE = Console()

class BaseController(Controller):
    class Meta:
        label = 'base'
        description = "DMD Analysis Tool v34 (Refactored)"
        arguments = [
            (['--help-detail'], {'help': 'Show detailed parameter registry', 'action': 'store_true'}),
        ]

    def _default(self):
        self.app.args.print_help()

class DMDFramework(App):
    class Meta:
        label = 'dmd_tool'
        handlers = [BaseController]
        exit_on_close = True

    def setup(self):
        super().setup()
        self.extend('console', RICH_CONSOLE)

    def run(self):
        if '--help-detail' in sys.argv:
            self._print_help_logic()
            sys.exit(0)
        super().run()

    def _print_help_logic(self):
        self.console.print("[bold underline]DMD Tool Operations Registry[/bold underline]\n")
        # We need to look for controllers that are stacked on base
        try: 
            # In Cement 3, handlers are registered by type. We want 'controller'.
            handlers = self.handler.list('controller')
        except: handlers = []

        for h in handlers:
            # Skip the base controller itself
            if h.Meta.label == 'base': continue

            label = getattr(h.Meta, 'label', 'Unknown')
            # Use 'description' as standard help
            std = getattr(h.Meta, 'description', 'No description')
            detailed = getattr(h.Meta, 'help_detailed', '')

            self.console.print(f"[bold cyan]{label}[/bold cyan]: {std}")
            if detailed:
                self.console.print(f"   [italic]{detailed}[/italic]")

            if hasattr(h.Meta, 'param_model') and h.Meta.param_model:
                try: schema = h.Meta.param_model.model_json_schema()['properties']
                except: 
                    try: schema = h.Meta.param_model.schema()['properties']
                    except: schema = {}

                if schema:
                    self.console.print("   [yellow]Parameters:[/yellow]")
                    for param, info in schema.items():
                        desc = info.get('description', 'No description.')
                        self.console.print(f"      --{param.replace('_', '-')}: {desc}")
            self.console.print("")
