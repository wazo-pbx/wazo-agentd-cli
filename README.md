# xivo-agentctl

A small CLI program to interact with xivo-agentd servers.

## Usage

```
$ xivo-agentctl --host example.org
xivo-agentctl> status 1004
Agent/1004 (ID 4)
    logged: False
xivo-agentctl> login 1004 1004 default
xivo-agentctl> status 1004
Agent/1004 (ID 4)
     logged: True
     extension: 1004
     context: default
```
