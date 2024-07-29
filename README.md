# k8s-pod-watcher

A CLI tool that fetches &amp; displays pods and related information.

⚠️ `kubectl` tool is required for using this script.

## Usage

- Fetching pods: `python3 main.py fetch ...args`
- Configuration: `python3 main.py config`

For easier usage, a bash function that drives this script can be created. In order to do that below bash function can be added at the end of `~/.bashrc` file (`~/.zshrc` in MACOS):

```bash
function pods() {
    python3 <<<path-to-main.py>>> "$@"
}
```

Then terminal session can be closed or following command can be executed: `source ~/.bashrc`. After these operations script can be run via below commands:

- Fetching pods: `pods fetch ...args`
- Configuration: `pods config`


## Arguments for fetch command

### `patterns`

Takes array of patterns for filtering pods.

### `-d` or `--detailed` flag

Shows pods with detailed information such as age, restart count, cpu &amp; memory usage etc.

### `-p` or `--prod` flag

Shows pods in production environment. (By default it shows pods in development environment).

### `-w` or `--watch` flag

Refreshes pod details periodically.

### `-n` or `--namespace` option

Shows pods that are in given namespace. (If not given, the default namespace in the `config.json` file will be used).
