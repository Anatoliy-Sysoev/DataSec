# TO BE Architecture

The TO BE architecture connects identity lifecycle, access requests, LDAP groups, Ranger policies, Trino access control, and audit delivery.

## Target flow

```text
HR / employee source
  -> IDM / access workflow
  -> LDAP groups
  -> Ranger UserSync
  -> Ranger policies
  -> Trino Ranger access control
  -> data sources

User
  -> Keycloak SSO
  -> Trino

Ranger audit
  -> OpenSearch / Solr / log pipeline
  -> SIEM
```

## Target responsibilities

| Component | Responsibility |
|---|---|
| HR / employee source | Hire, transfer, dismissal events |
| IDM | Access catalog, approval workflow, access lifecycle |
| Keycloak | SSO authentication through OIDC/OAuth2 |
| LDAP / FreeIPA / AD | Groups used for data-access authorization |
| Apache Ranger | Fine-grained data authorization and audit |
| Trino | SQL access layer and policy enforcement point |
| OpenSearch / Solr | Audit search and retention backend |
| SIEM | Security monitoring and detection rules |
| Access reconciler | Regular comparison of IDM, LDAP, Ranger and audit facts |

## Core principles

1. Authentication is handled by Keycloak.
2. Authorization is handled by Ranger.
3. Group membership is controlled by IDM and stored in LDAP.
4. Ranger policies must use groups, not individual users.
5. Manual user management in Ranger is prohibited.
6. Service Desk is used only for exceptions and incidents.
7. Every Ranger service must have an owner, URL, API endpoint, audit destination, and lifecycle status.
8. Audit events must be exported to a security monitoring platform.

## Recommended versions

| Component | Recommendation |
|---|---|
| Trino | Use a version with native Ranger access control |
| Apache Ranger | 2.5.0+ because Trino service definition is included |
| Keycloak | Current supported release in your platform |
| LDAP | OpenLDAP / FreeIPA / AD with stable group schema |
| Audit backend | OpenSearch/Elasticsearch/Solr depending on approved stack |

## PlantUML

See: [`../plantuml/to-be-component.puml`](../plantuml/to-be-component.puml), [`../plantuml/to-be-process.puml`](../plantuml/to-be-process.puml), and [`../plantuml/use-cases.puml`](../plantuml/use-cases.puml).
