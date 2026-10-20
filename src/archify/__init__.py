"""
archify: Zero-dependency Interactive SVG and HTML Architecture Visualizer for Software Projects.
"""

__version__ = "0.1.0"

from .scanner import scan_architecture
from .renderers import generate_html, generate_svg

__all__ = ["scan_architecture", "generate_html", "generate_svg", "__version__"]
