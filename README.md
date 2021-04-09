# wazo-agentd-cli

A small CLI program to interact with wazo-agentd.

## Usage

```
$ wazo-agentd-cli --host example.org
wazo-agentd-cli> status 1004
Agent/1004 (ID 4)
    logged: False
wazo-agentd-cli> login 1004 1004 default
wazo-agentd-cli> status 1004
Agent/1004 (ID 4)
     logged: True
     extension: 1004
     context: default
     state_interface: SIP/alice
```

