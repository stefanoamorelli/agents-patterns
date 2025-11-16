"""Colorful logging utilities using Rich library."""

import logging

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

custom_theme = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "bold red",
        "critical": "bold white on red",
        "success": "bold green",
        "highlight": "bold magenta",
        "section": "bold blue",
        "data": "green",
    }
)

console = Console(theme=custom_theme)


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure rich colored logging for all examples.

    Args:
        level: Logging level (default: logging.INFO)
    """
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=console,
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                show_time=True,
                show_path=False,
            )
        ],
    )


def log_section(title: str, width: int = 80) -> None:
    """
    Log a section header with styling.

    Args:
        title: Section title
        width: Width of the section divider
    """
    console.print()
    console.rule(f"[section]{title}[/section]", style="section")
    console.print()


def log_success(message: str) -> None:
    """
    Log a success message.

    Args:
        message: Success message
    """
    console.print(f"[success]✓[/success] {message}")


def log_info(message: str) -> None:
    """
    Log an info message.

    Args:
        message: Info message
    """
    console.print(f"[info]ℹ[/info] {message}")


def log_warning(message: str) -> None:
    """
    Log a warning message.

    Args:
        message: Warning message
    """
    console.print(f"[warning]⚠[/warning] {message}")


def log_error(message: str) -> None:
    """
    Log an error message.

    Args:
        message: Error message
    """
    console.print(f"[error]✗[/error] {message}")


def log_data(label: str, value: any) -> None:
    """
    Log a data label-value pair.

    Args:
        label: Data label
        value: Data value
    """
    console.print(f"[data]{label}:[/data] {value}")


def print_panel(content: str, title: str = "", border_style: str = "blue") -> None:
    """
    Print content in a styled panel.

    Args:
        content: Panel content
        title: Panel title
        border_style: Border color/style
    """
    from rich.panel import Panel

    console.print(Panel(content, title=title, border_style=border_style))


def print_table(data: list[dict], title: str = "") -> None:
    """
    Print data as a formatted table.

    Args:
        data: List of dictionaries representing rows
        title: Table title
    """
    from rich.table import Table

    if not data:
        return

    table = Table(title=title, show_header=True, header_style="bold magenta")

    for key in data[0].keys():
        table.add_column(key, style="cyan")

    for row in data:
        table.add_row(*[str(v) for v in row.values()])

    console.print(table)
