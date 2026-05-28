# Apache Ranger Configuration Examples

This directory contains examples for Trino service policies and Ranger plugin configuration.

## Key files

| File | Purpose |
|---|---|
| `ranger-trino-security.xml.example` | Ranger Admin URL, service name and policy cache settings |
| `ranger-trino-audit.xml.example` | Audit destination example |
| `policies/trino-base-policies.md` | Required baseline policies for Trino |

## Design rules

1. Create policies for groups, not individual users.
2. Keep service names deterministic: `trino-<environment>-<cluster>`.
3. Use a common naming convention for policies.
4. Do not store secrets in XML files committed to Git.
5. Use a secret manager for LDAP bind credentials, Ranger admin credentials, keystore passwords and TLS material.
