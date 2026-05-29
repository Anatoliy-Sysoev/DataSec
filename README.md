# DataSec Reference Architecture

**Язык:** Русский | [English](README.en.md)

Открытая референсная архитектура и демонстрационный контур для безопасного доступа к аналитическим данным.

Решение показывает, как связать **Trino**, **Apache Ranger**, **Keycloak**, **OpenLDAP / FreeIPA / AD** и контур аудита для построения управляемой DataSec-платформы:

- SSO-аутентификация пользователей через Keycloak;
- централизованные заявки на доступ через IDM-процесс;
- LDAP-группы как управляемый источник ролей доступа к данным;
- fine-grained authorization в Trino через Apache Ranger;
- аудит действий пользователей и передача событий в SIEM;
- локальный Docker lab и Kubernetes blueprint для развертывания.

В репозитории нет названий работодателей, внутренних доменов, хостов, учетных данных и корпоративных идентификаторов. Все примеры обезличены и используют демонстрационные значения.

---

## Какую проблему решаем

Аналитические платформы часто развиваются в разрозненную модель доступа:

- пользователи запрашивают доступ через заявки без нормального каталога ролей;
- инженеры вручную добавляют пользователей в LDAP-группы;
- доступ после увольнения или перевода может оставаться активным;
- Trino-кластеры работают без единого слоя авторизации;
- Ranger-инстансы не инвентаризируются и не аудируются централизованно;
- audit logs лежат локально и не коррелируются командами ИБ/SOC.

Целевая модель связывает жизненный цикл пользователя, заявку на доступ, LDAP-группы, политики Ranger, выполнение SQL-запросов в Trino и аудит в один контролируемый процесс.

Подробнее: [`docs/problem-statement.md`](docs/problem-statement.md).

---

## Целевая архитектура

```text
HR / источник сотрудников
        |
        v
IDM / workflow заявок на доступ
        |
        v
OpenLDAP / FreeIPA / AD группы
        |
        v
Apache Ranger UserSync
        |
        v
Apache Ranger Admin + Trino service policies
        |
        v
Trino Ranger Access Control
        |
        v
Источники данных

Пользователь -> Keycloak SSO -> Trino
Trino/Ranger Audit -> OpenSearch/Solr/Log pipeline -> SIEM
```

---

## Структура репозитория

```text
docs/                 Архитектура, AS IS / TO BE, ADR, IDM-интеграция
plantuml/             Исходники PlantUML-диаграмм
mermaid/              Исходники Mermaid-диаграмм для GitHub preview
docker/               Docker Compose lab scaffold
k8s/                  Kubernetes manifests и Helm-oriented blueprint
ranger/               Примеры конфигурации Ranger и базовых политик
trino/                Примеры конфигурации Trino
ldap/                 Нейминг LDAP-групп, структура каталога и bootstrap.ldif
keycloak/             Примечания по realm/client/OIDC
examples/             Обезличенные входные данные для scripts/reconcile_access.py
scripts/              Скрипты проверки, reconciliation и рендера диаграмм
.github/workflows/    CI-проверки Markdown, PlantUML и рендера диаграмм
```

`images/` не хранится в Git как обязательный исходный каталог. PNG/SVG-диаграммы генерируются CI или локально через `scripts/render_diagrams.sh`.

---

## Быстрый запуск: Docker lab

```bash
git clone https://github.com/Anatoliy-Sysoev/DataSec.git
cd DataSec/docker
cp .env.example .env
docker compose up -d
```

Docker-профиль предназначен для проверки архитектуры, демонстрации конфигураций и локальных экспериментов. Для production используйте Kubernetes blueprint и замените демонстрационные образы, секреты и хранилища на утвержденные платформенные компоненты.

---

## Быстрый запуск: Kubernetes blueprint

```bash
kubectl create namespace datasec
kubectl apply -n datasec -f k8s/base/
```

Каталог `k8s/` содержит референсные манифесты и конфигурационные паттерны. В реальной среде должны использоваться утвержденные Helm charts / operators, secret manager, ingress, TLS issuer, HA PostgreSQL и корпоративное audit-хранилище.

---

## Ключевые архитектурные решения

| Область | Решение |
|---|---|
| Аутентификация | Keycloak / OIDC / SSO |
| Авторизация | Apache Ranger access control для Trino |
| Группы | LDAP / FreeIPA / AD группы, управляемые через IDM-процесс |
| Заявки на доступ | IDM workflow, а не ручное исполнение через Service Desk |
| Политики доступа | Политики на группы, не на отдельных пользователей |
| Аудит | Ranger audit + опционально Trino event listener |
| SIEM | Через OpenSearch/Solr/log shipper/Kafka в зависимости от контура |
| Развертывание | Docker для lab, Kubernetes для целевой схемы |

Подробнее: [`docs/architecture-decisions.md`](docs/architecture-decisions.md).

---

## Диаграммы

| Диаграмма | Исходник |
|---|---|
| AS IS компоненты | [`plantuml/as-is-component.puml`](plantuml/as-is-component.puml) |
| AS IS процесс | [`plantuml/as-is-process.puml`](plantuml/as-is-process.puml) |
| TO BE компоненты | [`plantuml/to-be-component.puml`](plantuml/to-be-component.puml) |
| TO BE процесс | [`plantuml/to-be-process.puml`](plantuml/to-be-process.puml) |
| Use Case | [`plantuml/use-cases.puml`](plantuml/use-cases.puml) |
| Mermaid overview | [`mermaid/to-be-overview.mmd`](mermaid/to-be-overview.mmd) |

PNG/SVG-версии создаются GitHub Actions и скриптом `scripts/render_diagrams.sh`.

---

## Официальные источники

- Trino Ranger access control: https://trino.io/docs/current/security/ranger-access-control.html
- Trino OAuth2 authentication: https://trino.io/docs/current/security/oauth2.html
- Trino group mapping: https://trino.io/docs/current/security/group-mapping.html
- Apache Ranger: https://github.com/apache/ranger
- Trino: https://github.com/trinodb/trino
- Trino Helm charts: https://github.com/trinodb/charts
- Keycloak: https://github.com/keycloak/keycloak
- OpenLDAP: https://www.openldap.org/
- Stackable Trino operator: https://github.com/stackabletech/trino-operator
- Canonical Ranger operator: https://github.com/canonical/ranger-k8s-operator

Полный список: [`docs/reference-links.md`](docs/reference-links.md).

---

## Статус

Репозиторий является **reference solution / implementation blueprint**. Это не привязка к конкретному работодателю и не копия внутренней инфраструктуры. Все примеры используют обезличенные имена, демонстрационные домены и открытые технологические паттерны.
