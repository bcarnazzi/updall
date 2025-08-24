import platform

import sh
from rich import print as richprint
from rich.console import Console


def main() -> None:
    console = Console()

    with console.status("") as status:
        match platform.system():
            case "Linux":
                status.update("Updating APT system packages...")
                print(sh.sudo.apt("update"))
                print(sh.sudo.apt("full-upgrade", "-y"))
            case "Darwin":
                status.update("Updating Homebrew packages...")
                print(sh.brew("update"))
                print(sh.brew("upgrade"))
            case _:
                console.log(
                    f":red_circle: Unsupported operating system: {platform.system()}"
                )
                return

        status.update("Updating mise-en-place packages...")
        print(sh.mise("self-update", "-y"))
        print(sh.mise("up", "-y"))

        status.update("Updating uv packages...")
        print(sh.uv("tool", "upgrade", "--all"))

        status.update("Updating neovim plugins...")
        sh.nvim(
            "--headless",
            "-c",
            "+lua MiniDeps.later(function() MiniDeps.update(nil, { force = true }); vim.cmd('TSUpdateSync'); vim.cmd('qa') end); vim.wait(30000)",
        )

    richprint(":white_check_mark: System is up-to-date")
