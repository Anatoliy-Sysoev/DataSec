# Deployment Guide

This guide describes two deployment modes:

1. Docker Compose lab for local validation.
2. Kubernetes blueprint for production-like environments.

## Docker lab

The Docker lab is designed for fast architecture validation.

```bash
cd docker
cp .env.example .env
docker compose up -d
```

The lab starts:

- OpenLDAP;
- Keycloak;
- PostgreSQL;
- OpenSearch;
- Trino.

Apache Ranger is intentionally not pinned to an unofficial Docker image. Production teams should build Ranger from approved artifacts or use an approved operator/chart/image.

## Kubernetes blueprint

```bash
kubectl create namespace datasec
kubectl apply -n datasec -f k8s/base/
```

The Kubernetes blueprint contains:

- namespace-independent config samples;
- ConfigMaps for Trino and Ranger plugin configuration;
- deployment placeholders;
- ingress/TLS assumptions documented but not hardcoded.

## Production requirements

| Area | Requirement |
|---|---|
| TLS | Mandatory for Keycloak/OIDC and external Trino access |
| Secrets | Store in Vault, Kubernetes Secrets, or another approved secret manager |
| Ranger DB | Use HA PostgreSQL/MySQL, not an embedded database |
| Ranger Admin | Use at least two instances behind a load balancer |
| Ranger UserSync | Run as a single active instance |
| Audit backend | OpenSearch/Elasticsearch/Solr/S3/Log4J depending on approved stack |
| Monitoring | Prometheus/Grafana for Trino, Ranger, UserSync, audit backend |
| SIEM | Export Ranger audit events to central security monitoring |

## Official sources

- Trino Ranger access control: https://trino.io/docs/current/security/ranger-access-control.html
- Trino OAuth2: https://trino.io/docs/current/security/oauth2.html
- Apache Ranger: https://github.com/apache/ranger
- Trino Helm charts: https://github.com/trinodb/charts
