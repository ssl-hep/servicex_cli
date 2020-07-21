# ServiceX Command Line Tool
This is a tool for setting up the ServiceX cluster. 

Currently, its only function is to automatically create a
Kubernetes [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) 
to securely store your grid certs and passphrase, and to clear this Secret.

## Installation
The tool is available on pypi:
```bash
pip install servicex-cli
```

## Usage
To list the version of the servicex cli installed:
```bash
servicex version
```

### Initialization

The ServiceX CLI can be used to initialize ServiceX as follows:

```bash
servicex [--namespace <namespace>] init [certs|all] [--cert-dir <cert dir>]
```

Run `servicex init` to set up everything, or specify one or more components 
for partial setup (e.g. `servicex init certs`).
Certs are the only component currently supported.

#### Grid Certs

By default, the CLI will find certs in `.globus` in your home directory. You can 
override this by providing a `--cert-dir` command line option.

By default the secret will be created in the `default` namespace. You can
override this by providing a `--namespace` command line option 
(this must precede the `init` command). 

You will be prompted for your grid cert passphrase. This 
will not be echoed to the screen, but will be stored in the Kubernetes Secret.

### Removal

If you want to remove the installed Secrets from the cluster then
you can use:

```bash
servicex [--namespace <namespace>] clear [certs|all]
```

Run `servicex clear` to clear all Secrets, or specify one or more components 
(e.g. `servicex clear certs`).
Specify a `--namespace` argument which precedes the `clear` command to remove the 
Secrets from that namespace.

