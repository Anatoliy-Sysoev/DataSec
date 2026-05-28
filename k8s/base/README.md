# Kubernetes Blueprint

This directory contains a reference deployment blueprint.

It is not a complete production Helm chart. It shows the required configuration surfaces and the expected structure for a Kubernetes-based DataSec stack.

## Recommended production deployment

- Trino: official Trino Helm chart or platform-approved chart.
- Ranger: approved internal image, operator, or custom Helm chart based on Apache Ranger release artifacts.
- Keycloak: official Keycloak chart/operator or platform-approved deployment.
- LDAP: managed OpenLDAP/FreeIPA/AD service.
- Audit backend: OpenSearch/Elasticsearch/Solr with retention and SIEM export.

## Apply sample resources

```bash
kubectl apply -f namespace.yaml
kubectl apply -f trino-configmap.yaml
```
