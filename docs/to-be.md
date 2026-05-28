# TO BE-архитектура

TO BE-архитектура связывает жизненный цикл пользователя, заявки на доступ, LDAP-группы, политики Ranger, контроль доступа в Trino и доставку аудита.

## Целевой поток

```text
HR / источник сотрудников
  -> IDM / workflow доступа
  -> LDAP-группы
  -> Ranger UserSync
  -> политики Ranger
  -> Trino Ranger access control
  -> источники данных

Пользователь
  -> Keycloak SSO
  -> Trino

Ranger audit
  -> OpenSearch / Solr / log pipeline
  -> SIEM
```

## Ответственность компонентов

| Компонент | Ответственность |
|---|---|
| HR / источник сотрудников | События приема, перевода и увольнения |
| IDM | Каталог доступов, маршруты согласования, жизненный цикл доступов |
| Keycloak | SSO-аутентификация через OIDC/OAuth2 |
| LDAP / FreeIPA / AD | Группы, используемые для авторизации к данным |
| Apache Ranger | Fine-grained authorization и аудит |
| Trino | SQL-слой доступа и policy enforcement point |
| OpenSearch / Solr | Поиск и хранение audit-событий |
| SIEM | Мониторинг безопасности и detection rules |
| Access Reconciler | Регулярная сверка IDM, LDAP, Ranger и audit-фактов |

## Базовые принципы

1. Аутентификация выполняется через Keycloak.
2. Авторизация выполняется через Apache Ranger.
3. Членство в группах контролируется IDM и хранится в LDAP.
4. Политики Ranger должны строиться на группах, а не на отдельных пользователях.
5. Ручное управление пользователями в Ranger запрещено.
6. Service Desk используется только для исключений и инцидентов.
7. У каждого Ranger service должны быть владелец, URL, API endpoint, audit destination и lifecycle status.
8. Audit-события должны выгружаться в контур мониторинга безопасности.

## Рекомендуемые версии

| Компонент | Рекомендация |
|---|---|
| Trino | Версия с native Ranger access control |
| Apache Ranger | 2.5.0+, так как Trino service definition уже включен |
| Keycloak | Актуальная поддерживаемая версия в платформе |
| LDAP | OpenLDAP / FreeIPA / AD со стабильной групповой схемой |
| Audit backend | OpenSearch / Elasticsearch / Solr в зависимости от утвержденного стека |

## PlantUML

См. [`../plantuml/to-be-component.puml`](../plantuml/to-be-component.puml), [`../plantuml/to-be-process.puml`](../plantuml/to-be-process.puml), [`../plantuml/use-cases.puml`](../plantuml/use-cases.puml).
