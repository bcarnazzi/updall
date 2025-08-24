import sh
from rich.console import Console
from rich import print as richprint


def main() -> None:
    console = Console()

    with console.status("Updating APT system packages...") as status:
        print(sh.sudo.apt("update"))
        print(sh.sudo.apt("full-upgrade", "-y"))

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
