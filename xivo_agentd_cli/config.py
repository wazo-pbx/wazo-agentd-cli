# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import argparse

from xivo.chain_map import ChainMap
from xivo.config_helper import read_config_file_hierarchy

_DEFAULT_CONFIG = {
    'config_file': '/etc/xivo-agentd-cli/config.yml',
    'extra_config_files': '/etc/xivo-agentd-cli/conf.d',
    'agent': {
        'host': 'localhost',
        'verify_certificate': '/usr/share/xivo-certs/server.crt',
    },
}


def load(argv):
    cli_config = _parse_cli_args(argv)
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    return ChainMap(cli_config, file_config, _DEFAULT_CONFIG)


def _parse_cli_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--command',
                        action='store',
                        help='Command to run.')
    parser.add_argument('--config-file',
                        action='store',
                        help="The path where is the config file.")
    parser.add_argument('--host',
                        action='store',
                        help='Hostname of the xivo-agentd server.')
    parser.add_argument('--port',
                        action='store',
                        type=int,
                        help='Port number of the xivo-agentd server.')
    parsed_args = parser.parse_args(argv)

    result = {'agent': {}}
    if parsed_args.command:
        result['command'] = parsed_args.command
    if parsed_args.config_file:
        result['config_file'] = parsed_args.config_file
    if parsed_args.host:
        result['agent']['host'] = parsed_args.host
    if parsed_args.port:
        result['agent']['port'] = parsed_args.port

    return result
