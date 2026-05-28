# Problem Statement

## Context

Data platforms usually start with direct database access and local permissions. As the number of data sources, analysts, contractors, service accounts, and regulated datasets grows, this model becomes unsafe and hard to audit.

## Problems solved by this reference architecture

1. **Uncontrolled data access**
   - Users receive direct database permissions.
   - Permissions are spread across multiple systems.
   - Access is difficult to review and revoke.

2. **Manual access execution**
   - Access requests are handled through tickets.
   - Engineers manually add users to groups.
   - Mistakes and delays are inevitable.

3. **No consistent authorization model**
   - Authentication confirms who the user is.
   - It does not decide which schema, table, or column the user can access.
   - Ranger provides this missing authorization layer.

4. **Weak audit visibility**
   - Audit logs are local or incomplete.
   - Security teams cannot easily answer: who accessed sensitive data, when, from where, and through which policy.

5. **Poor lifecycle control**
   - Dismissed or transferred users may retain access.
   - Access revocation must be driven by the identity lifecycle.

## Target outcome

A project team should be able to deploy a repeatable DataSec stack where:

- users authenticate through SSO;
- access is requested through an IDM workflow;
- group membership is stored in LDAP;
- Ranger applies fine-grained data policies in Trino;
- audit is collected and exported for security monitoring;
- access state can be reconciled automatically.
