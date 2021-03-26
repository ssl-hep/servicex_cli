# Copyright (c) 2019, IRIS-HEP
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import sys
import json

import kubernetes
import pkg_resources
from kubernetes import client
import base64
import os.path
import os
import getpass
from OpenSSL.crypto import FILETYPE_PEM, load_privatekey, Error

parser = argparse.ArgumentParser("servicex")
parser.add_argument('--namespace', "-n",
                    default="default",
                    help="Namespace where secrets should be created")
subparsers = parser.add_subparsers(dest="command")
subparsers.required = True

# Init command
init_parser = subparsers.add_parser("init", help="Initialize secret(s)")
init_parser.add_argument('secrets',
                         default=["all"],
                         nargs='*',
                         help="Secret which should be initialized")
init_parser.add_argument("--cert-dir",
                         default="~/.globus",
                         help="Directory where your grid certs are located")

# Clear command
clear_parser = subparsers.add_parser('clear', help="Clear secret(s)")
clear_parser.add_argument("secrets",
                          default=["all"],
                          nargs='*',
                          help="Name of secret which should be cleared")

# Version command
version_parser = subparsers.add_parser("version")


def init_cluster(args):
    namespace, secrets = args.namespace, args.secrets
    if "certs" in secrets or "all" in secrets:
        create_certs_secret(namespace, "grid-certs-secret", args.cert_dir)


def create_certs_secret(namespace, secret_name, cert_dir):
    clear_secret(namespace, secret_name)
    passphrase = getpass.getpass("Enter passphrase for certs: ")
    data = {'passphrase': base64.b64encode(passphrase.encode()).decode("ascii")}

    expanded_cert_dir = os.path.expanduser(cert_dir)
    if not os.path.isdir(expanded_cert_dir):
      sys.stderr.write(f"Can't locate {expanded_cert_dir}, exiting.\n")
      sys.exit(-1)

    for fname in ['usercert.pem', 'userkey.pem']:
      cert_filename = os.path.join(expanded_cert_dir, fname)
      if not os.path.isfile(cert_filename):
        sys.stderr.write(f"Can't locate {cert_filename}, exiting.\n")
        sys.exit(-1)
      with open(os.path.join(expanded_cert_dir, fname), 'rb') as cert_file:
        data[fname] = base64.b64encode(cert_file.read()).decode("ascii")

    try:
        _ = load_privatekey(FILETYPE_PEM,
                              base64.b64decode(data['userkey.pem']),
                              passphrase=passphrase.encode('utf8'))
    except Error:
        sys.stderr.write("Passphrase does not unlock key file. Please correct and try again.\n")
        sys.exit(-1)

    secret = client.V1Secret(data=data,
                             kind='Secret',
                             type='Opaque',
                             metadata=client.V1ObjectMeta(name=secret_name))
    try:
      client.CoreV1Api().create_namespaced_secret(namespace=namespace, body=secret)
    except kubernetes.client.exceptions.ApiException as e:
      resp = json.loads(e.body)
      sys.stderr.write(f"Got an error while creating secret on kubernetes cluster: {resp['message']}\n")
      sys.exit(-1)
    except Error:
      sys.stderr.write(f"Got an error while creating secret on kubernetes cluster\n")
      sys.exit(-1)
    print(f"Successfully created {secret_name}.")


def clear_cluster(args):
    namespace, secrets = args.namespace, args.secrets
    if "certs" in secrets or "all" in secrets:
        clear_secret(namespace, "grid-certs-secret")


def clear_secret(namespace, secret_name):
    try:
        client.CoreV1Api().delete_namespaced_secret(namespace=namespace, name=secret_name)
        print(f"Cleared {secret_name}.")
    except kubernetes.client.rest.ApiException:
        print(f"No existing {secret_name} to clear.")


def main():
    kubernetes.config.load_kube_config()
    args = parser.parse_args()

    if args.command == 'init':
        init_cluster(args)

    elif args.command == 'clear':
        clear_cluster(args)

    elif args.command == 'version':
        print("ServiceX CLI Version " + pkg_resources.get_distribution('servicex-cli').version)


if __name__ == "__main__":
    # execute only if run as a script
    main()
