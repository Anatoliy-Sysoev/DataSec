# AS IS Architecture

This page describes a typical fragmented data-access model that the DataSec reference architecture is designed to improve.

## Current state

```text
User -> Service Desk ticket -> manual approval -> LDAP admin manually adds user to LDAP group
User -> Keycloak SSO -> Trino
LDAP -> Ranger UserSync -> Ranger policies -> Trino Ranger plugin
Ranger audit -> local audit store / partial export
```

## Characteristics

| Area | AS IS behavior | Risk |
|---|---|---|
| Access request | Service Desk ticket | No structured access catalog |
| Execution | Manual LDAP group update | Human error and delay |
| Revocation | Manual or delayed | Excessive access after transfer/dismissal |
| SSO | Keycloak used for login | SSO does not equal data authorization |
| Authorization | Ranger may use LDAP groups | Depends on manual group hygiene |
| Audit | Stored locally or inconsistently exported | Weak security monitoring |
| Governance | No unified Ranger inventory | Difficult audit across projects |

## Main pain points

1. Manual LDAP updates do not scale.
2. Service Desk is not a full identity lifecycle system.
3. Keycloak authentication and LDAP-based authorization can drift.
4. Ranger policies become hard to audit without standard naming and ownership.
5. Security teams need API-based inventory and audit, not manual UI checks.
6. Dismissal and department transfer must trigger automatic access revocation.

## PlantUML

See: [`../plantuml/as-is-component.puml`](../plantuml/as-is-component.puml) and [`../plantuml/as-is-process.puml`](../plantuml/as-is-process.puml).
