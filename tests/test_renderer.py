import pytest
from click.testing import CliRunner
from testfixtures import TempDirectory

from litestar_manage.cli import project
from litestar_manage.renderer import RenderingContext, _render_jinja_dir
from tests import TEMPLATE_DIR


@pytest.fixture
def rendering_context() -> RenderingContext:
    return RenderingContext(app_name="TestApp")


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_render_jinja_dir(rendering_context: RenderingContext, runner: CliRunner) -> None:
    with TempDirectory() as t:
        temp_path = t.as_path()
        _render_jinja_dir(TEMPLATE_DIR, temp_path, rendering_context)

        assert (temp_path / "src").exists()
        assert (temp_path / "tests").exists()
        assert (temp_path / "src" / "main.py").exists()

    result = runner.invoke(project, ["new", "--app-name", "TestApp"])
    assert result.exit_code == 0
