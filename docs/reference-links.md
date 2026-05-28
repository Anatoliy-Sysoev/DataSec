# Reference Links

## Official documentation and repositories

- Trino Ranger access control: https://trino.io/docs/current/security/ranger-access-control.html
- Trino OAuth2 authentication: https://trino.io/docs/current/security/oauth2.html
- Trino group mapping: https://trino.io/docs/current/security/group-mapping.html
- Trino repository: https://github.com/trinodb/trino
- Trino Helm charts: https://github.com/trinodb/charts
- Apache Ranger repository: https://github.com/apache/ranger
- Keycloak repository: https://github.com/keycloak/keycloak
- OpenLDAP: https://www.openldap.org/

## Useful open-source references

- Stackable Trino operator: https://github.com/stackabletech/trino-operator
- Canonical Ranger Kubernetes operator: https://github.com/canonical/ranger-k8s-operator
- Canonical Trino LDAP group provider plugin: https://github.com/canonical/trino-group-provider-ldap-plugin
- Trino Ranger demo by Aakash Nand: https://github.com/aakashnand/trino-ranger-demo

## Reading focus

When reviewing external repositories, check:

1. Trino version and Ranger version compatibility.
2. Whether `access-control.name=ranger` is used.
3. How groups are resolved: Trino group provider, Ranger UserSync, or OIDC claims.
4. How audit is stored and exported.
5. Whether the deployment is a demo or production-grade.
6. How secrets are stored.
7. Whether HA and monitoring are documented.
