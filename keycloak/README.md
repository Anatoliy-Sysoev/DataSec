# Keycloak

Каталог содержит рекомендации по настройке Keycloak как SSO/OIDC-провайдера для Trino.

## Роль Keycloak в архитектуре

Keycloak отвечает за аутентификацию пользователя:

```text
Пользователь -> Keycloak SSO -> Trino
```

Keycloak не заменяет IDM и не заменяет Apache Ranger:

- IDM управляет заявками, согласованиями и жизненным циклом доступов;
- Keycloak подтверждает личность пользователя;
- LDAP хранит группы доступа к данным;
- Apache Ranger применяет политики доступа к данным в Trino.

## Минимальные настройки клиента Trino

Для production-контура необходимо определить:

- realm;
- client_id для Trino;
- redirect URI;
- client secret или другой допустимый способ доверия;
- scopes;
- claim с именем пользователя, например `preferred_username`;
- TLS для внешнего доступа к Trino.

## Официальная документация

- Trino OAuth2 authentication: https://trino.io/docs/current/security/oauth2.html
- Keycloak documentation: https://www.keycloak.org/documentation
