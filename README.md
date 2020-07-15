# ServiceX Command Line Tool
This is a tool for setting up the ServiceX cluster. 

Currently, its only function is to automatically create
Kubernetes [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) 
to securely store the following:
- Your grid certs and passphrase
- Slack webhook URL for new user registration

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

### Initialization

The ServiceX CLI can be used to initialize ServiceX as follows:

```bash
servicex init [certs|app|all] [--namespace <namespace>] [--cert-dir <cert dir>] [--webhook <webhook url>]
```

Run `servicex init all` to set up everything, 
or specify a single component for partial setup (e.g. `servicex init certs`).

For information on the available options for each component, see below.

#### Grid Certs

By default, the CLI will find certs in `.globus` in your home directory. You can 
override this by providing a `--cert-dir` command line option.

By default the secret will be created in the `default` namespace. You can
override this by providing a `--namespace` command line option.

You will be prompted for your grid cert passphrase. This 
will not be echoed to the screen, but will be stored in the Kubernetes Secret.

#### ServiceX App

If the `--webhook` option is provided with a Slack 
[incoming webhook](https://slack.com/help/articles/115005265063-Incoming-Webhooks-for-Slack) 
URL, ServiceX will post a message to the Slack channel of your choice 
upon each new user registration.

The CLI tool will provide environment variables to the ServiceX Flask app in 
a Secret (default name: `servicex-app-secret`).
You still must enter the name of this Secret in the `values.yaml` file:

```yaml
app:
  # Name of secret used to populate environment variables
  secret: servicex-app-secret
```

Now Helm will retrieve this URL and provide it to the ServiceX REST API server 
(Flask app) upon installation.

### Removal

If you want to remove the installed Secrets from the cluster then
you can use:

```bash
servicex clear [certs|app|all] [--namespace <namespace>]
```

Run `servicex clear all` to clear all Secrets, or specify a single component 
(e.g. `servicex clear certs`). This takes the same `--namespace` argument as the `init` command to remove the 
Secrets from that namespace.

