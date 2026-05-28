# Baseline Trino Policies in Apache Ranger

A Trino service in Ranger usually requires baseline policies before business data policies can work correctly.

## 1. Query execution policy

Resource:

```text
queryid = *
```

Access:

```text
execute
```

Subjects:

```text
{USER}
```

## 2. Self impersonation policy

Resource:

```text
Trino User = {USER}
```

Access:

```text
impersonate
```

Subjects:

```text
{USER}
```

## 3. Information schema policy

Allow read access to `information_schema` where required for metadata discovery.

## 4. Function execution policy

Allow execution of safe functions for baseline user groups.

## 5. Business data policies

Business policies should be created for LDAP groups:

```text
dl_sales_orders_ro -> catalog=sales, schema=public, table=orders, access=select
dl_sales_pii_masked -> column masking on sensitive columns
```

## Rule

Do not create long-term policies for individual users. Use groups managed by the access workflow.
