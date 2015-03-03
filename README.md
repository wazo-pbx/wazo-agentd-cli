# xivo-agentdctl

A small CLI program to interact with xivo-agentd servers.

## Usage

```
$ xivo-agentdctl --host example.org
xivo-agentdctl> status 1004
Agent/1004 (ID 4)
    logged: False
xivo-agentdctl> login 1004 1004 default
xivo-agentdctl> status 1004
Agent/1004 (ID 4)
     logged: True
     extension: 1004
     context: default
```
