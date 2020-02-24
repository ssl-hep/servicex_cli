# ServiceX Command Line Tool
This is a tool for setting up the serviceX cluster. 

Its only function for now is to install your grid certs and passphrase
securely as kubernetes secrets.

## Installation
The tool is available on pypi so...
```bash
pip install servicex-cli
```

## Usage
To list the version of the servicex cli installed:
```bash
servicex version
```

### Install Certs
To install your grid certs
```bash
servicex init
```
By default, it will find certs in `.globus` in your home directory. You can 
override this by providing a `--cert-dir` command line option.

By default the secret will be created in the `default` namespace. You can
override this by providing a `--namespace` command line option.

When the script runs it will prompt you for your grid cert passphrase. This 
will not be echoed to the screen, but will be stored in the kubernetes secret.

### Remove Certs
If you want to remove the installed certs and passphrase from the cluster then
you can use:
```bash
servicex clear
```

It takes the same `--namespace` argument as the `init` command to remove the 
secret from that namespace.
 



