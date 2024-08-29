
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
