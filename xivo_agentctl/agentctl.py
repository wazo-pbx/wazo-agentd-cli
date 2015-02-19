# -*- coding: utf-8 -*-

# Copyright (C) 2012-2015 Avencall
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

from __future__ import print_function
from __future__ import unicode_literals

import argparse

from contextlib import contextmanager
from operator import attrgetter

from xivo.cli import BaseCommand, Interpreter, UsageError
from xivo_agent.ctl.client import AgentClient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--command',
                        help='run command')
    parser.add_argument('--no-fetch', action='store_true',
                        help="don't fetch response from server")

    parsed_args = parser.parse_args()

    fetch_response = not parsed_args.no_fetch

    with _agent_client(fetch_response) as agent_client:
        interpreter = Interpreter(prompt='xivo-agentctl> ',
                                  history_file='~/.xivoagentctl_history')
        interpreter.add_command('add', AddAgentToQueueCommand(agent_client))
        interpreter.add_command('remove', RemoveAgentFromQueueCommand(agent_client))
        interpreter.add_command('login', LoginCommand(agent_client))
        interpreter.add_command('logoff', LogoffCommand(agent_client))
        interpreter.add_command('relog all', RelogAllCommand(agent_client))
        interpreter.add_command('pause', PauseCommand(agent_client))
        interpreter.add_command('unpause', UnpauseCommand(agent_client))
        interpreter.add_command('status', StatusCommand(agent_client))

        if parsed_args.command:
            interpreter.execute_command_line(parsed_args.command)
        else:
            interpreter.loop()


@contextmanager
def _agent_client(fetch_response):
    agent_client = AgentClient(fetch_response=fetch_response)
    agent_client.connect()
    try:
        yield agent_client
    finally:
        agent_client.close()


class BaseAgentClientCommand(BaseCommand):

    def __init__(self, agent_client):
        BaseCommand.__init__(self)
        self._agent_client = agent_client

    def execute(self):
        raise NotImplementedError()


class AddAgentToQueueCommand(BaseAgentClientCommand):

    help = 'Add agent to queue'
    usage = '<agent_id> <queue_id>'

    def prepare(self, command_args):
        try:
            agent_id = int(command_args[0])
            queue_id = int(command_args[1])
            return (agent_id, queue_id)
        except Exception:
            raise UsageError()

    def execute(self, agent_id, queue_id):
        self._agent_client.add_agent_to_queue(agent_id, queue_id)


class RemoveAgentFromQueueCommand(BaseAgentClientCommand):

    help = 'Remove agent from queue'
    usage = '<agent_id> <queue_id>'

    def prepare(self, command_args):
        try:
            agent_id = int(command_args[0])
            queue_id = int(command_args[1])
            return (agent_id, queue_id)
        except Exception:
            raise UsageError()

    def execute(self, agent_id, queue_id):
        self._agent_client.remove_agent_from_queue(agent_id, queue_id)


class LoginCommand(BaseAgentClientCommand):

    help = 'Login agent'
    usage = '<agent_number> <extension> <context>'

    def prepare(self, command_args):
        try:
            agent_number = command_args[0]
            extension = command_args[1]
            context = command_args[2]
            return (agent_number, extension, context)
        except Exception:
            raise UsageError()

    def execute(self, agent_number, extension, context):
        self._agent_client.login_agent_by_number(agent_number, extension, context)


class LogoffCommand(BaseAgentClientCommand):

    help = 'Logoff agent'
    usage = '(<agent_number> | all)'

    def prepare(self, command_args):
        try:
            agent_number = command_args[0]
            return (agent_number,)
        except Exception:
            raise UsageError()

    def execute(self, agent_number):
        if agent_number == 'all':
            self._execute_all()
        else:
            self._execute(agent_number)

    def _execute_all(self):
        self._agent_client.logoff_all_agents()

    def _execute(self, agent_number):
        self._agent_client.logoff_agent_by_number(agent_number)


class RelogAllCommand(BaseAgentClientCommand):

    help = 'Relog all currently logged agents'
    usage = None

    def execute(self):
        self._agent_client.relog_all_agents()


class PauseCommand(BaseAgentClientCommand):

    help = 'Pause agent'
    usage = '<agent_number>'

    def prepare(self, command_args):
        try:
            agent_number = command_args[0]
            return (agent_number,)
        except Exception:
            raise UsageError()

    def execute(self, agent_number):
        self._agent_client.pause_agent_by_number(agent_number)


class UnpauseCommand(BaseAgentClientCommand):

    help = 'Unpause agent'
    usage = '<agent_number>'

    def prepare(self, command_args):
        try:
            agent_number = command_args[0]
            return (agent_number,)
        except Exception:
            raise UsageError()

    def execute(self, agent_number):
        self._agent_client.unpause_agent_by_number(agent_number)


class StatusCommand(BaseAgentClientCommand):

    help = 'Get status of agent'
    usage = '[<agent_number>]'

    def prepare(self, command_args):
        if command_args:
            agent_number = command_args[0]
        else:
            agent_number = None
        return (agent_number,)

    def execute(self, agent_number):
        if agent_number is None:
            self._execute_all()
        else:
            self._execute(agent_number)

    def _execute_all(self):
        agent_statuses = self._agent_client.get_agent_statuses()
        for agent_status in sorted(agent_statuses, key=attrgetter('number')):
            _print_agent_status(agent_status)

    def _execute(self, agent_number):
        agent_status = self._agent_client.get_agent_status_by_number(agent_number)
        _print_agent_status(agent_status)


def _print_agent_status(agent_status):
    print('Agent/{0.number} (ID {0.id})'.format(agent_status))
    print('    logged: {0.logged}'.format(agent_status))
    if agent_status.logged:
        print('    extension: {0.extension}'.format(agent_status))
        print('    context: {0.context}'.format(agent_status))


if __name__ == '__main__':
    main()
