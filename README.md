# shellexeclist

List all executables called by a shell script.
Take this tool as a package maintainer's knife to check if all needed 3rd binaries are referenced

## Usage

```shell
usage: shelllistexec [-h] [--forceshell FORCESHELL] files [files ...]

a tool to list executables called by a shell script

positional arguments:
  files                 Files to analyze

optional arguments:
  -h, --help            show this help message and exit
  --forceshell FORCESHELL
                        Force to interpret as shell x
```

By default the used shell is guessed by the shebang, to override that decision pass `--forceshell=<the shell of your choice>` to CLI.

## Currently supported shells

- bash
- sh (POSIX shell)
- ksh
- zsh

if a not supported shell is found interpretation will fall back to *POSIX shell*

## Example

```shell
shellexeclist testfiles/K01speech-dispatcher
```

returns

```shell
[
dirname
echo
exit
install
ln
log_daemon_msg
log_end_msg
set
sh
sleep
start-stop-daemon
test
```

meaning that this particular script calls all of the mentioned executables in some way

## Note

There's is no way to tell if a script is gracefully handling missing executables - this process still requires manual inspection of the sources

## License

As this tool incorporates code from [bitbake](https://git.openembedded.org/bitbake) it's licensed under `GPL-2.0-only`

Detailed licensing information on the incorporated code can be also found [here](shellexeclist/bb/LICENSE)

## Contribute

Feel free to open issues and PRs.
All contributed code has to apply to the HEAD of the `master` branch and needs to pass `pytest` (with the current project configuration)
