from cement import App, Controller
from rich.console import Console
import sys
from typing import Any

RICH_CONSOLE = Console()


class BaseController(Controller):
    class Meta:
        label = '--base'
        description = "DMD Analysis Tool v34 (Refactored)"
        arguments = [
            (['--help-detail'], {'help': 'Show detailed parameter registry', 'action': 'store_true'}),
        ]

    def _default(self):
        self.app.args.print_help()


class DMDFramework(App):
    class Meta:
        label = '--dmd_tool'
        handlers = [BaseController]
        exit_on_close = True

    def setup(self):
        super().setup()
        self.extend('console', RICH_CONSOLE)
        self._register_operation_arguments()

    def _register_operation_arguments(self):
        """Register operation flags via Cement's add_argument() API."""
        args_parser = getattr(self, 'args', None)
        if not args_parser or not hasattr(args_parser, 'add_argument'):
            return

        try:
            handlers = self.handler.list('controller')
        except Exception:
            handlers = []

        for handler in handlers:
            label = getattr(handler.Meta, 'label', None)
            if not label or label in {'--base', '--base_op'}:
                continue
            help_text = getattr(handler.Meta, 'description', f'Run {label}')
            try:
                args_parser.add_argument(label, help=help_text, action='store_true')
            except Exception:
                # Ignore parser conflicts from pre-registered arguments.
                pass

    def run(self):
        operation = self._requested_operation_label()
        if operation and self._is_help_requested():
            self._print_operation_help(operation)
            sys.exit(0)

        if '--help-detail' in sys.argv:
            self._print_help_logic()
            sys.exit(0)
        super().run()

    @staticmethod
    def _is_help_requested() -> bool:
        return any(flag in sys.argv for flag in {'-h', '--help'})

    def _requested_operation_label(self) -> str | None:
        known_labels = self._operation_labels()
        for token in sys.argv[1:]:
            if token in known_labels:
                return token
        return None

    def _operation_labels(self) -> set[str]:
        try:
            handlers = self.handler.list('controller')
        except Exception:
            handlers = []
        labels: set[str] = set()
        for handler in handlers:
            label = getattr(handler.Meta, 'label', None)
            if label and label not in {'--base', '--base_op'}:
                labels.add(label)
        return labels

        for token in sys.argv[1:]:
            if token.startswith('-'):
                continue
            return token
        return None

    def _find_operation_handler(self, label: str):
        try:
            handlers = self.handler.list('controller')
        except Exception:
            handlers = []
        for handler in handlers:
            if getattr(handler.Meta, 'label', None) == label:
                return handler
        return None

    def _print_operation_help(self, operation_label: str):
        operation = self._find_operation_handler(operation_label)
        if not operation:
            self.args.print_help()
            return

        default_argument_lines = [
            '--debug, -d         full application debug mode',
            '--quiet, -q         suppress all console output',
            f'--help, -h          show this help message for {operation_label}',
        ]
        app_defined_arguments = self._format_argument_lines(BaseController.Meta.arguments)
        op_defined_arguments = self._format_argument_lines(getattr(operation.Meta, 'arguments', []))

        self.console.print(f'usage: {sys.argv[0]} {operation_label} [OPTIONS]')
        description = getattr(operation.Meta, 'description', None)
        if description:
            self.console.print(f'\n{description}')

        self.console.print('\noptions:')
        for line in default_argument_lines + app_defined_arguments + op_defined_arguments:
            self.console.print(f'  {line}')

    @staticmethod
    def _format_argument_lines(arguments: list[tuple[list[str], dict[str, Any]]]) -> list[str]:
        lines: list[str] = []
        for flags, meta in arguments:
            if not flags:
                continue
            label = ', '.join(flags)
            description = meta.get('help', 'No description')
            details = []
            if meta.get('required'):
                details.append('required')
            if meta.get('default') not in {None, ...}:
                details.append(f"default: {meta['default']}")
            suffix = f" ({', '.join(details)})" if details else ''
            lines.append(f'{label:<20} {description}{suffix}')
        return lines

    def _print_help_logic(self):
        self.console.print("[bold underline]DMD Tool Operations Registry[/bold underline]\n")
        try:
            handlers = self.handler.list('controller')
        except Exception:
            handlers = []

        for h in handlers:
            if h.Meta.label in {'--base'}:
                continue

            label = getattr(h.Meta, 'label', 'Unknown')
            std = getattr(h.Meta, 'description', 'No description')
            detailed = getattr(h.Meta, 'help_detailed', '')

            self.console.print(f"[bold cyan]{label}[/bold cyan]: {std}")
            if detailed:
                self.console.print(f"   [italic]{detailed}[/italic]")

            if hasattr(h.Meta, 'param_model') and h.Meta.param_model:
                try:
                    schema = h.Meta.param_model.model_json_schema()['properties']
                except Exception:
                    try:
                        schema = h.Meta.param_model.schema()['properties']
                    except Exception:
                        schema = {}

                arguments = getattr(h.Meta, 'arguments', [])
                if arguments:
                    self.console.print("   [yellow]Options:[/yellow]")
                    for option_flags, option_meta in arguments:
                        option_label = ", ".join(option_flags)
                        desc = option_meta.get('help')
                        dest = option_meta.get('dest')
                        if not desc and schema and dest in schema:
                            desc = schema[dest].get('description')
                        if not desc:
                            desc = 'No description.'
                        details = []
                        if option_meta.get('required'):
                            details.append("required")
                        if option_meta.get('default') not in {None, ...}:
                            details.append(f"default: {option_meta['default']}")
                        if option_meta.get('action') in {'store_true', 'store_false'}:
                            details.append("flag")
                        suffix = f" ({', '.join(details)})" if details else ""
                        self.console.print(f"      {option_label}: {desc}{suffix}")
            self.console.print("")
