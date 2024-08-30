
## [Installation](https://docs.astral.sh/uv/getting-started/installation/)

- download
```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```
- apply
```zsh
source $HOME/.cargo/env
```
- update
```shell
uv self update
```
- auto auto completion
```shell
# Determine your shell (e.g., with `echo $SHELL`), then run one of:
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc
echo 'uv generate-shell-completion fish | source' >> ~/.config/fish/config.fish
echo 'eval (uv generate-shell-completion elvish | slurp)' >> ~/.elvish/rc.elv
```
- Uninstallation
```shell
uv cache clean
rm -r "$(uv python dir)"
rm -r "$(uv tool dir)"
rm ~/.cargo/bin/uv ~/.cargo/bin/uvx
```


## [python](https://docs.astral.sh/uv/concepts/python-versions/#installing-a-python-version)


- `uv` will [automatically fetch Python versions](https://docs.astral.sh/uv/guides/install-python/#automatic-python-downloads) as needed — you don't need to install Python to get started.
- also it can manange your python envs
- Once Python is installed, it will be used by `uv` commands automatically.


- [activate venv](https://docs.astral.sh/uv/guides/projects/#running-commands:~:text=uv%20sync%0A%24%20source%20.venv/bin/activate)
```shell
uv sync
source .venv/bin/activate
```
- [Finding a Python executable](https://docs.astral.sh/uv/concepts/python-versions/#finding-a-python-executable:~:text=To%20find%20a%20Python%20executable%2C%20use%20the%20uv%20python%20find%20command%3A)
```shell
uv python find
```