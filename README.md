# xivo-agentd-cli

## Deprecated

The xivo-agentd-cli is now deprecated in favor of the [wazo-agentd-cli](https://github.com/wazo-pbx/wazo-agentd-cli)

A small CLI program to interact with xivo-agentd.

## Usage

```
$ xivo-agentd-cli --host example.org
xivo-agentd-cli> status 1004
Agent/1004 (ID 4)
    logged: False
xivo-agentd-cli> login 1004 1004 default
xivo-agentd-cli> status 1004
Agent/1004 (ID 4)
     logged: True
     extension: 1004
     context: default
     state_interface: SIP/alice
```
