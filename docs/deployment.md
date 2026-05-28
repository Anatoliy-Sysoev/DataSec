# Руководство по развертыванию

Документ описывает два режима развертывания:

1. Docker Compose lab для локальной проверки.
2. Kubernetes blueprint для production-like окружений.

## Docker lab

Docker lab предназначен для быстрой проверки архитектуры и конфигураций.

```bash
cd docker
cp .env.example .env
docker compose up -d
```

Lab-контур поднимает:

- OpenLDAP;
- Keycloak;
- PostgreSQL;
- OpenSearch;
- Trino.

Apache Ranger намеренно не привязан к случайному неофициальному Docker-образу. Для production-команд корректный подход: собрать Ranger из официальных Apache release artifacts или использовать утвержденный operator/chart/image.

## Kubernetes blueprint

```bash
kubectl create namespace datasec
kubectl apply -n datasec -f k8s/base/
```

Kubernetes blueprint содержит:

- независимые от namespace примеры конфигураций;
- ConfigMap для Trino и конфигурации Ranger plugin;
- placeholder-структуру для deployment;
- предположения по ingress/TLS, зафиксированные в документации, но не зашитые в манифесты.

## Production-требования

| Область | Требование |
|---|---|
| TLS | Обязателен для Keycloak/OIDC и внешнего доступа к Trino |
| Секреты | Хранить в Vault, Kubernetes Secrets или другом утвержденном secret manager |
| Ranger DB | Использовать HA PostgreSQL/MySQL, не embedded database |
| Ranger Admin | Минимум два инстанса за балансировщиком |
| Ranger UserSync | Один активный экземпляр |
| Audit backend | OpenSearch/Elasticsearch/Solr/S3/Log4J в зависимости от утвержденного стека |
| Monitoring | Prometheus/Grafana для Trino, Ranger, UserSync и audit backend |
| SIEM | Выгружать audit-события Ranger в централизованный контур ИБ |

## Официальные источники

- Trino Ranger access control: https://trino.io/docs/current/security/ranger-access-control.html
- Trino OAuth2: https://trino.io/docs/current/security/oauth2.html
- Apache Ranger: https://github.com/apache/ranger
- Trino Helm charts: https://github.com/trinodb/charts
