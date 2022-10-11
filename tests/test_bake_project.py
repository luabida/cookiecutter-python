from pathlib import Path

import pytest


@pytest.fixture
def context():
    return {
        "author_full_name": "Sir Example",
        "author_email": "example@ex.ex",
        "project_name": "Example",
        "project_slug": "example",
        "project_short_description": "This is an example",
        "project_url": "example.com",
        "project_version": "0.1.0",
        "documentation_engine": "sphinx",
    }

@pytest.fixture
def mkdocs():
    return {
        "documentation_engine": "mkdocs",
    }

@pytest.fixture
def jupyter():
    return {
        "documentation_engine": "jupyter-book",
    }


def test_bake_project(cookies):
    result = cookies.bake()
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "osl-python-package"
    assert result.project_path.is_dir()


def test_project_generation_with_example_context(cookies, context):
    result = cookies.bake(extra_context={**context})
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()


def test_if_documentation_engine_is_sphinx_with_example_context(
    cookies, context
):
    result = cookies.bake(extra_context={**context})
    assert result.exit_code == 0
    assert result.exception is None
    SPHINX_CONF_PATH = Path(result.project_path) / "docs" / "conf.py"
    sphinx_file_exists = Path.is_file(SPHINX_CONF_PATH)
    assert sphinx_file_exists


def test_project_name_with_example_context(cookies, context):
    result = cookies.bake(extra_context={**context})
    assert result.exit_code == 0
    assert result.exception is None
    README_FILE = Path(result.project_path) / "README.md"
    with open(README_FILE) as f:
        title = f.readline().rstrip()
        assert title == "# Example"


def test_documentations_generation_with_mkdocs(cookies, mkdocs):
    result = cookies.bake(extra_context={**mkdocs})
    assert result.exit_code == 0
    assert result.exception is None
    MKDOCS_CONF_PATH = Path(result.project_path) / 'mkdocs.yaml'
    mkdocs_file_exists = Path.is_file(MKDOCS_CONF_PATH)
    assert mkdocs_file_exists


def test_documentations_generation_with_jupyter_book(cookies, jupyter):
    result = cookies.bake(extra_context={**jupyter})
    assert result.exit_code == 0
    assert result.exception is None
    JUPYTER_CONF_PATH = Path(result.project_path) / 'docs' / '_config.yaml'
    jupyter_file_exists = Path.is_file(JUPYTER_CONF_PATH)
    assert jupyter_file_exists
