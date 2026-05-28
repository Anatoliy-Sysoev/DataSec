# Kubernetes Blueprint

Каталог содержит референсный blueprint для Kubernetes-развертывания.

Это не полноценный production Helm chart. Каталог показывает необходимые конфигурационные поверхности и ожидаемую структуру Kubernetes-based DataSec stack.

## Рекомендуемое production-развертывание

- Trino: официальный Trino Helm chart или утвержденный платформенный chart.
- Ranger: утвержденный внутренний image, operator или custom Helm chart на базе Apache Ranger release artifacts.
- Keycloak: официальный Keycloak chart/operator или утвержденное платформенное развертывание.
- LDAP: managed OpenLDAP/FreeIPA/AD service.
- Audit backend: OpenSearch/Elasticsearch/Solr с retention и SIEM export.

## Применение примерных ресурсов

```bash
kubectl apply -f namespace.yaml
kubectl apply -f trino-configmap.yaml
```
