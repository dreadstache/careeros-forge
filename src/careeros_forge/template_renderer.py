from jinja2 import Environment, PackageLoader, StrictUndefined, TemplateNotFound


class TemplateRenderer:
    """Render templates shipped inside the CareerOS Forge package."""

    def __init__(self) -> None:
        self._environment = Environment(
            loader=PackageLoader("careeros_forge", "templates"),
            undefined=StrictUndefined,
            autoescape=False,
            keep_trailing_newline=True,
        )

    def render(self, template_name: str, **values: object) -> str:
        try:
            template = self._environment.get_template(template_name)
        except TemplateNotFound as error:
            raise ValueError(f"template not found: {template_name}") from error
        return template.render(**values)
