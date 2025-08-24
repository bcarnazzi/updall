import platform

import sh
import click
from rich import print as richprint
from rich.console import Console


def create_live_runner():
    class Runner:
        def __getattr__(self, name):
            command = getattr(sh, name)

            def runner(*args, **kwargs):
                for line in command(*args, _iter=True, **kwargs):
                    print(line, end="")

            return runner

    return Runner()


@click.command
@click.option("--nvim", is_flag=True, help="Include neovim plugins updates")
def main(nvim: bool) -> None:
    run = create_live_runner()
    console = Console()

    with console.status("") as status:
        match platform.system():
            case "Linux":
                status.update("Updating APT system packages...")
                run.sudo("apt", "update")
                run.sudo("apt", "full-upgrade", "-y")
                status.update("Updating flatpaks...")
                run.flatpak("update", "-y")
            case "Darwin":
                status.update("Updating Homebrew packages...")
                run.brew("update")
                run.brew("upgrade")
            case _:
                console.log(
                    f":red_circle: Unsupported operating system: {platform.system()}"
                )
                return

        status.update("Updating mise-en-place packages...")
        run.mise("self-update", "-y")
        run.mise("up", "-y")

        status.update("Updating uv packages...")
        run.uv("tool", "upgrade", "--all")

        if nvim:
            status.update("Updating neovim plugins...")
            run.nvim(
                "--headless",
                "-c",
                "+lua MiniDeps.later(function() MiniDeps.update(nil, { force = true }); vim.cmd('TSUpdateSync'); vim.cmd('qa') end); vim.wait(30000)",
            )

    richprint(":white_check_mark: System is up-to-date")
