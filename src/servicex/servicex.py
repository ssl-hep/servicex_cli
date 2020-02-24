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

import kubernetes
import pkg_resources
from kubernetes import client
import base64
import os.path
import os
import getpass

parser = argparse.ArgumentParser("ServiceX Command Line Interface")
parser.add_argument("command", choices=["init", "version", "clear"])
parser.add_argument("--cert-dir",
                    default="~/.globus",
                    help="Directory where your grid certs are located")
parser.add_argument("--namespace", "-n",
                    default='default',
                    help="Namespace where secret should be created")


def init_cluster(cert_dir, secret_name, namespace):
    passphrase = getpass.getpass("Enter passphrase for certs: ")

    try:
        client.CoreV1Api().delete_namespaced_secret(namespace=namespace, name=secret_name)
        print("Existing secret cleared")
    except kubernetes.client.rest.ApiException:
        print("Empty Cluster. Creating secrets for the first time")

    data = {'passphrase': base64.b64encode(passphrase.encode()).decode("ascii")}

    with open(os.path.expanduser(os.path.join(cert_dir, 'usercert.pem')), 'rb') as usercert_file:
        data['usercert.pem'] = base64.b64encode(usercert_file.read()).decode("ascii")

    with open(os.path.expanduser(os.path.join(cert_dir, 'userkey.pem')), 'rb') as userkey_file:
        data['userkey.pem'] = base64.b64encode(userkey_file.read()).decode("ascii")

    secret = client.V1Secret(data=data,
                             kind='Secret',
                             type='Opaque',
                             metadata=client.V1ObjectMeta(name=secret_name))

    client.CoreV1Api().create_namespaced_secret(namespace=namespace, body=secret)


def clear_cluster(secret_name, namespace):
    try:
        client.CoreV1Api().delete_namespaced_secret(namespace=namespace, name=secret_name)
        print("Secret cleared")
    except kubernetes.client.rest.ApiException:
        print("Empty Cluster. Nothing to do....")


def main():
    kubernetes.config.load_kube_config()
    args = parser.parse_args()

    if args.command == 'init':
        init_cluster(args.cert_dir, "grid-certs-secret", args.namespace)

    elif args.command == 'clear':
        clear_cluster("grid-certs-secret", args.namespace)

    elif args.command == 'version':
        print("ServiceX CLI Version " + pkg_resources.get_distribution('servicex-cli').version)


if __name__ == "__main__":
    # execute only if run as a script
    main()
