# LDAP Groups

This directory describes a demo LDAP structure for data-access groups.

Production rule: LDAP group membership must be managed by an IDM workflow, not by manual administrator actions.

## Naming convention

```text
dl_<domain>_<dataset>_<level>
```

Examples:

```text
dl_sales_orders_ro
dl_sales_pii_masked
dl_finance_payments_ro
dl_marketing_events_rw
```

## Recommended OU structure

```text
ou=data-access,ou=groups,dc=example,dc=org
```

## Required metadata

Each group should have:

- business description;
- data owner;
- approver group;
- sensitivity label;
- expiration rules if access is temporary;
- mapping to Ranger policy names.
