# Примеры конфигурации Apache Ranger

Каталог содержит примеры конфигурации Ranger для Trino service policies и Ranger Trino plugin.

## Ключевые файлы

| Файл | Назначение |
|---|---|
| `ranger-trino-security.xml.example` | URL Ranger Admin, service name и настройки policy cache |
| `ranger-trino-audit.xml.example` | Пример настройки audit destination |
| `policies/trino-base-policies.md` | Базовые политики, необходимые для работы Trino |

## Правила проектирования

1. Создавать политики на группы, а не на отдельных пользователей.
2. Использовать детерминированные service names: `trino-<environment>-<cluster>`.
3. Соблюдать единый стандарт именования политик.
4. Не хранить секреты в XML-файлах, закоммиченных в Git.
5. Использовать secret manager для LDAP bind credentials, Ranger admin credentials, keystore passwords и TLS-материалов.
