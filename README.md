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

To set up ServiceX

```bash
servicex init [--namespace <namespace>] [--cert-dir <cert dir>] [--webhook <webhook url>]
```

#### Installing Certs

By default, it will find certs in `.globus` in your home directory. You can 
override this by providing a `--cert-dir` command line option.

By default the secret will be created in the `default` namespace. You can
override this by providing a `--namespace` command line option.

When the script runs it will prompt you for your grid cert passphrase. This 
will not be echoed to the screen, but will be stored in the Kubernetes Secret.

#### Configuring Registration Webhook

If the `--webhook` option is provided with a Slack 
[incoming webhook](https://slack.com/help/articles/115005265063-Incoming-Webhooks-for-Slack) 
URL, ServiceX will post a message to the Slack channel of your choice upon each new user registration.
The CLI tool will store the URL in a Secret (default name: `servicex-app-secret`), 
but you still must enter the name of this Secret in the `values.yaml` file:

```yaml
app:
  # Name of secret used to populate environment variables
  secret: servicex-app-secret
```

Now Helm will retrieve this URL and provide it to the ServiceX REST API server (Flask app) upon installation.

### Removal

If you want to remove the installed Secrets from the cluster then
you can use:

```bash
servicex clear [--namespace <namespace>]
```

This takes the same `--namespace` argument as the `init` command to remove the 
Secrets from that namespace.
 



