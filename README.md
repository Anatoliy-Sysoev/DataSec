# DataSec Reference Architecture

Open reference architecture and deployable lab for a secure analytical data access platform.

The project demonstrates how to combine **Trino**, **Apache Ranger**, **Keycloak**, **OpenLDAP**, and an audit pipeline to solve enterprise data-access governance problems:

- SSO authentication for analysts and service users;
- centralized access requests through an IDM-like process;
- LDAP groups as a controlled source for data-access roles;
- fine-grained authorization in Trino through Apache Ranger;
- audit collection for security monitoring and SIEM integration;
- Docker lab and Kubernetes deployment blueprint.

No company-specific names, domains, hosts, credentials, or internal identifiers are used.

---

## Problem

Analytical platforms often evolve into a fragmented access model:

- users request database access through tickets;
- engineers manually add users to LDAP groups;
- access revocation after dismissal or department transfer is delayed;
- Trino clusters are deployed without a unified authorization layer;
- Ranger instances are not inventoried and audited consistently;
- audit logs are stored locally and not correlated by security teams.

This repository describes a target model where identity lifecycle, access requests, authorization policies, and audit are connected into one controllable DataSec flow.

---

## Target architecture

```text
HR / Employee Source
        |
        v
IDM / Access Request Workflow
        |
        v
OpenLDAP / FreeIPA / AD groups
        |
        v
Apache Ranger UserSync
        |
        v
Apache Ranger Admin + Trino Service Policies
        |
        v
Trino Ranger Access Control
        |
        v
Data Sources

User -> Keycloak SSO -> Trino
Trino/Ranger Audit -> OpenSearch/Solr/Log pipeline -> SIEM
```

---

## Repository structure

```text
docs/                 Architecture, AS IS / TO BE, use cases, decisions
plantuml/             Component, sequence, use-case and deployment diagrams
docker/               Docker Compose lab scaffold
k8s/                  Kubernetes manifests and Helm-oriented deployment blueprint
ranger/               Ranger service and policy examples
trino/                Trino configuration examples
ldap/                 LDAP LDIF examples and naming convention
keycloak/             Keycloak realm/client notes
scripts/              Helper scripts for validation and reconciliation
```

---

## Quick start: Docker lab

```bash
git clone https://github.com/Anatoliy-Sysoev/DataSec.git
cd DataSec/docker
cp .env.example .env
docker compose up -d
```

The Docker profile is a lab scaffold. It is intended for architecture validation, configuration review, and demo scenarios. For production, use the Kubernetes blueprint and replace demo images, secrets, and storage with approved platform components.

---

## Quick start: Kubernetes blueprint

```bash
kubectl create namespace datasec
kubectl apply -n datasec -f k8s/base/
```

The Kubernetes directory contains reference manifests and config patterns. In a real platform, use your organization-approved Helm charts, secret manager, ingress, TLS issuer, PostgreSQL HA, and audit backend.

---

## Core design decisions

| Area | Decision |
|---|---|
| Authentication | Keycloak / OIDC / SSO |
| Authorization | Apache Ranger access control for Trino |
| Groups | LDAP/FreeIPA/AD groups managed by IDM process |
| Access requests | IDM workflow, not manual Service Desk execution |
| Data access policies | Group-based policies, not direct user policies |
| Audit | Ranger audit + optional Trino event listener |
| SIEM | Via OpenSearch/Solr/log shipper/Kafka depending on environment |
| Deployment | Docker for lab, Kubernetes for target blueprint |

---

## Official references

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

---

## Status

This repository is a reference solution and implementation blueprint. It is not tied to any employer or internal infrastructure. All examples use anonymized names and demo domains.
