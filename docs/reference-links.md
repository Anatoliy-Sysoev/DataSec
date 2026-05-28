# Ссылки и внешние референсы

## Официальная документация и репозитории

- Trino Ranger access control: https://trino.io/docs/current/security/ranger-access-control.html
- Trino OAuth2 authentication: https://trino.io/docs/current/security/oauth2.html
- Trino group mapping: https://trino.io/docs/current/security/group-mapping.html
- Trino repository: https://github.com/trinodb/trino
- Trino Helm charts: https://github.com/trinodb/charts
- Apache Ranger repository: https://github.com/apache/ranger
- Keycloak repository: https://github.com/keycloak/keycloak
- OpenLDAP: https://www.openldap.org/

## Полезные open-source референсы

- Stackable Trino operator: https://github.com/stackabletech/trino-operator
- Canonical Ranger Kubernetes operator: https://github.com/canonical/ranger-k8s-operator
- Canonical Trino LDAP group provider plugin: https://github.com/canonical/trino-group-provider-ldap-plugin
- Trino Ranger demo by Aakash Nand: https://github.com/aakashnand/trino-ranger-demo

## На что смотреть при разборе внешних решений

1. Совместимость версий Trino и Ranger.
2. Используется ли `access-control.name=ranger`.
3. Где разрешаются группы: Trino group provider, Ranger UserSync или OIDC claims.
4. Как хранится и выгружается аудит.
5. Это demo-проект или production-grade реализация.
6. Где хранятся секреты.
7. Описаны ли HA, мониторинг и эксплуатационные ограничения.
