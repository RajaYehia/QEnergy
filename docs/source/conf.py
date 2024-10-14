# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "qenergy"
copyright = "Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone"
author = "Raja Yehia, Yoann Piétri, Carlos Pascual García, Pascal Lefebvre, Federico Centrone"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx-prompt",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    "matplotlib.sphinxext.plot_directive",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

root_doc = "index"
autoclass_content = "both"
autodoc_member_order = "bysource"

latex_documents = [
    (
        root_doc,
        "qenergy.tex",
        "qenergy",
        author.replace(", ", "\\and ").replace(" and ", "\\and and "),
        "manual",
    ),
]

latex_elements = {
    "preamble": r"""
\DeclareUnicodeCharacter{2588}{~}
\DeclareUnicodeCharacter{2557}{~}
\DeclareUnicodeCharacter{2554}{~}
\DeclareUnicodeCharacter{2550}{~}
\DeclareUnicodeCharacter{255D}{~}
\DeclareUnicodeCharacter{255A}{~}
\DeclareUnicodeCharacter{2551}{~}
\DeclareUnicodeCharacter{2584}{~}
\DeclareUnicodeCharacter{2580}{~}
"""
}
