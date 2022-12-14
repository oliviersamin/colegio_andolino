from pylatex import Package
from pylatex.base_classes import Environment


class Form(Environment):
    """A class to wrap hyperref's form environment."""

    _latex_name = 'Form'

    packages = [Package('hyperref')]
    escape = False
    content_separator = "\n"

class TeXfile:
    def __init__(self) -> None:
        # Document Geometry Options
        self.geometry_options = {
            "head": "40pt",
            "margin": "0.5in",
            "bottom": "1.6in",
            "includeheadfoot": True
        }