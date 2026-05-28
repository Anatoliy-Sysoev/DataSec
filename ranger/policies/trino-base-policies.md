# Базовые политики Trino в Apache Ranger

Для Trino service в Ranger обычно нужны базовые политики, без которых бизнес-политики доступа к данным могут работать некорректно.

## 1. Политика выполнения запросов

Ресурс:

```text
queryid = *
```

Доступ:

```text
execute
```

Субъекты:

```text
{USER}
```

## 2. Политика self impersonation

Ресурс:

```text
Trino User = {USER}
```

Доступ:

```text
impersonate
```

Субъекты:

```text
{USER}
```

## 3. Политика information_schema

Разрешить read-доступ к `information_schema`, если это требуется для просмотра метаданных.

## 4. Политика выполнения функций

Разрешить выполнение безопасных функций для базовых пользовательских групп.

## 5. Бизнес-политики доступа к данным

Бизнес-политики должны создаваться на LDAP-группы:

```text
dl_sales_orders_ro -> catalog=sales, schema=public, table=orders, access=select
dl_sales_pii_masked -> column masking on sensitive columns
```

## Правило

Не создавать долгосрочные политики на отдельных пользователей. Использовать группы, управляемые через access workflow.
