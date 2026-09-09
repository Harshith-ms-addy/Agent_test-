# Project Secure Development & Application Security Standard

**Version:** 1.0
**Classification:** Internal Engineering Standard
**Applies to:** All Thinxsense applications, APIs, services, infrastructure, CI/CD workflows, repositories, scripts, integrations, and deployment environments.

---

# 1. Purpose

The purpose of this standard is to ensure that Thinxsense software is designed, developed, tested, deployed, and maintained using secure engineering practices.

Security is a mandatory engineering requirement and must be considered throughout the complete software development lifecycle.

Security controls must not depend solely on frontend validation, developer behavior, secrecy of implementation, or manual testing.

---

# 2. Security Standards

Thinxsense security practices should align with:

* OWASP Application Security Verification Standard — ASVS 5.0
* OWASP Top 10:2025
* NIST Secure Software Development Framework — SP 800-218
* Principle of Least Privilege
* Defense in Depth
* Zero Trust principles
* Secure-by-Default design
* Secure-by-Design engineering
* Software supply-chain security practices

Unless a stronger requirement has been established, internet-facing Thinxsense applications should target **OWASP ASVS Level 2**.

Components handling particularly sensitive, privileged, high-impact, or security-critical operations should be evaluated for stronger controls, including applicable ASVS Level 3 requirements.

---

# 3. Core Security Principles

Every Thinxsense system must follow these principles.

## 3.1 Deny by Default

Access must be denied unless explicitly permitted.

## 3.2 Least Privilege

Users, services, APIs, databases, CI jobs, cloud identities, and developers must receive only the permissions required for their tasks.

## 3.3 Defense in Depth

Security must not depend on a single control.

Sensitive operations should be protected through multiple independent controls where appropriate.

## 3.4 Secure by Default

New components must start from a secure configuration.

Developers should not need to manually enable fundamental security protections.

## 3.5 Server-Side Enforcement

Authentication, authorization, business rules, permissions, validation, and security controls must be enforced by trusted backend systems.

Frontend restrictions are not security controls.

## 3.6 Minimize Attack Surface

Unused:

* APIs
* ports
* services
* dependencies
* permissions
* routes
* debugging interfaces
* administrative interfaces

must be removed or disabled.

---

# 4. Authentication

Authentication mechanisms must use established, well-maintained libraries and protocols.

Custom cryptographic authentication systems must not be created unless explicitly reviewed by qualified security personnel.

Requirements:

* Passwords must never be stored in plaintext.
* Passwords must be stored using an approved password hashing algorithm such as Argon2id or an appropriately configured bcrypt implementation.
* Authentication responses must not expose whether sensitive account information exists unless required.
* Login endpoints must implement reasonable protection against brute-force and credential-stuffing attacks.
* Authentication tokens must use appropriate expiration.
* Refresh tokens must be protected appropriately.
* Sensitive authentication changes should require reauthentication where appropriate.
* MFA should be available for privileged accounts.
* MFA should be required for production administrators whenever supported.
* Session identifiers must be unpredictable.
* Session identifiers must not be placed in URLs.
* Logout must invalidate or terminate the relevant session where technically possible.

Default passwords must never be deployed to production.

---

# 5. Authorization and Access Control

Authorization must be validated on the server for every protected operation.

Never assume:

> authenticated = authorized

Requirements:

* Every sensitive API endpoint must perform authorization.
* Object-level authorization must be verified.
* Role-level authorization must be verified.
* Tenant boundaries must be enforced server-side.
* User-provided identifiers must not grant access by themselves.
* Administrative functionality must require explicit administrative authorization.
* Privileged operations should be logged.
* Authorization failures must fail closed.
* Client-side route guards must not be considered sufficient protection.

Changing identifiers, URLs, API parameters, request bodies, or object IDs must never allow unauthorized access to another user's or tenant's resources.

---

# 6. API Security

All APIs must validate:

* authentication
* authorization
* input
* content type
* request size
* expected fields
* data types
* allowed values

APIs must reject unexpected or malformed input safely.

Mass assignment must be prevented.

Sensitive fields must not automatically bind directly from arbitrary user-controlled request bodies.

Rate limiting should be implemented for endpoints vulnerable to:

* brute force
* enumeration
* abuse
* resource exhaustion
* expensive computation

API errors must not reveal:

* stack traces
* database details
* filesystem paths
* secrets
* internal service credentials
* infrastructure details

Production APIs must use encrypted transport.

---

# 7. Input Validation

All untrusted data must be treated as potentially malicious.

This includes data originating from:

* users
* APIs
* files
* databases
* browsers
* third-party integrations
* AI systems
* message queues
* webhooks
* URL parameters
* HTTP headers

Input should be validated against an explicit expected structure.

Prefer allowlists over blocklists.

Validation should include where appropriate:

* type
* format
* allowed values
* length
* minimum
* maximum
* encoding
* structure

Never rely solely on frontend validation.

---

# 8. Injection Prevention

User-controlled input must never be directly concatenated into executable commands.

This includes:

* SQL
* shell commands
* operating-system commands
* LDAP queries
* templates
* expressions
* interpreters

Use:

* parameterized database queries
* prepared statements
* safe ORM APIs
* safe templating mechanisms
* structured APIs

Shell execution should be avoided where practical.

User input must never become a command without strict validation and safe argument handling.

---

# 9. Cross-Site Scripting and Browser Security

User-controlled content must not be inserted into executable HTML or JavaScript contexts without appropriate protection.

Requirements:

* Prefer framework-native escaping.
* Avoid raw HTML rendering.
* Avoid unsafe DOM APIs.
* Sanitize HTML when HTML input is intentionally supported.
* Do not disable framework escaping mechanisms without documented security review.

Appropriate browser security controls should be configured, including where applicable:

* Content Security Policy
* frame protection
* MIME sniffing protection
* secure referrer policy
* secure cookie attributes

---

# 10. CSRF Protection

State-changing browser requests relying on cookie-based authentication must receive appropriate CSRF protection.

Cookies containing authentication or sensitive session information should use appropriate:

* Secure
* HttpOnly
* SameSite

attributes.

GET requests must not perform sensitive state-changing operations.

---

# 11. Cryptography

Do not design custom cryptographic algorithms or protocols.

Use established cryptographic libraries.

Sensitive network communications must use modern TLS.

TLS 1.3 should be preferred where supported.

TLS 1.2 may be supported when compatibility requires it and it is configured securely.

Deprecated SSL/TLS versions must not be enabled.

Sensitive data should be encrypted at rest where required by its risk classification.

Cryptographic keys must:

* not be hardcoded
* not be committed to source control
* be stored in an approved secret/key-management system
* have controlled access
* be rotated when compromise is suspected
* be separated between environments

Encryption keys must not be stored beside encrypted data when that defeats the security objective.

---

# 12. Secrets Management

The following must never be committed to source control:

* passwords
* API keys
* private keys
* database credentials
* production tokens
* OAuth client secrets
* cloud credentials
* signing keys
* encryption keys
* session secrets

Secrets must be stored using approved mechanisms such as:

* GitHub Secrets
* cloud secret managers
* dedicated vault systems
* protected deployment environment secrets

`.env` files containing secrets must not be committed.

Repositories should include:

```text
.env
.env.*
*.pem
*.key
```

in appropriate `.gitignore` rules where applicable.

Example environment files may contain variable names but must contain only safe placeholder values.

If a secret is accidentally committed:

1. Treat the secret as compromised.
2. Revoke or rotate it immediately.
3. Remove exposure where appropriate.
4. Investigate usage.
5. Document the incident.

Deleting the commit alone is not sufficient because the secret may already have been copied.

---

# 13. Data Protection

Data must be classified according to sensitivity.

Suggested categories:

## Public

Information intentionally available publicly.

## Internal

Information intended only for Thinxsense personnel or authorized systems.

## Confidential

Business-sensitive or customer-sensitive information.

## Restricted

Highly sensitive information such as:

* authentication credentials
* security keys
* sensitive personal information
* high-impact operational information

Collection of sensitive information must be minimized.

Applications must not collect data simply because it may become useful later.

Sensitive data must not unnecessarily appear in:

* URLs
* query strings
* logs
* analytics
* browser storage
* error messages

Production data should not be copied into development or testing environments unless appropriately protected and explicitly authorized.

---

# 14. Logging and Monitoring

Security-relevant events must be logged where appropriate.

Examples include:

* successful authentication
* failed authentication
* administrative operations
* permission changes
* account security changes
* suspicious authorization failures
* security configuration changes
* sensitive data exports
* privileged operations

Logs must not contain:

* passwords
* session tokens
* access tokens
* refresh tokens
* private keys
* API secrets
* complete payment credentials
* unnecessary sensitive personal information

Security logs should provide sufficient context for investigation without exposing secrets.

Production security events should be monitorable and capable of generating alerts for significant threats.

---

# 15. Error Handling

Production systems must fail safely.

Application errors must not expose:

* stack traces
* SQL statements
* internal paths
* source code
* credentials
* keys
* infrastructure secrets
* unnecessary internal architecture details

Detailed debugging information should be available only in controlled development environments or secure internal observability systems.

Security errors must fail closed.

---

# 16. File Upload Security

When file uploads are supported:

* allow only necessary file types
* validate actual content where possible
* enforce size limits
* generate safe storage names
* prevent directory traversal
* avoid direct execution of uploaded files
* store files outside executable application paths where applicable
* enforce authorization when retrieving private files

Original filenames must not be trusted as filesystem paths.

Additional malware scanning should be considered for untrusted files depending on risk.

---

# 17. Third-Party Dependencies

Every dependency introduces supply-chain risk.

Requirements:

* Add dependencies only when necessary.
* Prefer actively maintained packages.
* Avoid unknown or abandoned packages.
* Review security implications of major dependencies.
* Use lock files.
* Commit lock files.
* Review dependency changes in pull requests.
* Monitor known vulnerabilities.
* Remove unused dependencies.

Dependencies with known critical vulnerabilities must not knowingly be deployed without documented risk acceptance and mitigating controls.

Automated dependency scanning should be enabled.

---

# 18. Software Supply-Chain Security

The build and deployment pipeline must be protected as a security-critical system.

Requirements:

* CI/CD permissions must use least privilege.
* Production secrets must not be exposed to untrusted pull requests.
* Third-party CI actions must be trusted and reviewed.
* High-risk third-party actions should be pinned to immutable versions or commit SHAs where practical.
* Build artifacts must originate from controlled pipelines.
* Deployment credentials must not be shared manually.
* Production deployments must be auditable.
* Protected deployment environments should be used.
* Long-lived cloud credentials should be avoided where workload identity/OIDC is available.

A Software Bill of Materials should be generated for production releases where practical.

Software provenance and stronger SLSA-aligned controls should be adopted as the delivery pipeline matures.

---

# 19. GitHub Repository Security

Production repositories must use protected branches or repository rulesets.

The default branch must not accept uncontrolled direct pushes.

Pull requests should be required for production code changes.

Required checks should include where applicable:

```text
Lint
Type Check
Unit Tests
Integration Tests
Build
E2E Tests
Dependency Scan
Secret Scan
Static Security Analysis
```

Security-sensitive changes should require appropriate review.

Recommended security-sensitive areas include:

```text
authentication/
authorization/
middleware/
security/
crypto/
payments/
.github/workflows/
infrastructure/
database/migrations/
```

CODEOWNERS should be configured for highly sensitive components when appropriate.

Pull requests must not be merged while required security or CI checks are failing.

---

# 20. Secret Scanning

Secret scanning must be enabled where available.

Push protection should be enabled where supported.

If CI detects an exposed credential, the build must fail.

Detected credentials must be considered potentially compromised and handled according to the Secrets Management section.

---

# 21. Static Application Security Testing

Static application security testing should run automatically as part of CI or repository security scanning.

Security findings must be evaluated rather than blindly suppressed.

Security warnings must not be disabled merely to obtain a successful build.

False positives may be suppressed only when:

* the finding has been reviewed
* the reason is documented
* the suppression is narrowly scoped

---

# 22. Dependency and Vulnerability Scanning

Dependencies must be automatically monitored for known vulnerabilities.

Pull requests introducing dependencies should be reviewed for:

* package reputation
* maintenance status
* vulnerability history
* necessity
* transitive dependency impact
* licensing where applicable

Automated dependency update tooling should be enabled where practical.

---

# 23. Infrastructure Security

Infrastructure configuration must follow least privilege.

Requirements include where applicable:

* databases must not be publicly accessible without explicit need
* administrative interfaces must be restricted
* unnecessary ports must remain closed
* production services must require authentication
* cloud IAM permissions must be minimal
* infrastructure changes must be reviewed
* development credentials must not provide production access
* production and development environments must be logically separated

Infrastructure-as-Code should be used where practical so changes are reviewable and auditable.

---

# 24. Database Security

Databases must:

* require authentication
* use least-privilege application accounts
* avoid shared administrative credentials
* restrict network exposure
* use encrypted transport where appropriate
* maintain backups according to business requirements

Application database accounts must not normally operate as database administrators.

SQL queries must use parameterized operations.

Sensitive database operations should be auditable.

---

# 25. Environment Separation

At minimum, environments should be separated into:

```text
development
staging/testing
production
```

Credentials must be separate between environments.

Production secrets must never be used for local development.

Developers should not require unrestricted production database access for normal development activities.

Production debugging must not require disabling security controls.

---

# 26. Secure Coding Requirements

Developers must not:

* hardcode credentials
* disable TLS verification without explicit justification
* bypass authentication
* bypass authorization
* concatenate untrusted SQL
* evaluate arbitrary user-controlled code
* expose secrets through logging
* disable security controls to solve functionality problems
* suppress security warnings without review
* expose debug endpoints in production
* trust frontend authorization
* use insecure random generators for security-sensitive values
* implement custom cryptography unnecessarily

Security problems must be fixed at their root cause rather than hidden with UI restrictions.

---

# 27. Pull Request Security Requirements

Every pull request affecting production behavior must answer:

### Security Impact

* Does this change authentication?
* Does this change authorization?
* Does this change data access?
* Does this handle user-controlled input?
* Does this add an API endpoint?
* Does this expose new information?
* Does this add a dependency?
* Does this modify infrastructure?
* Does this modify secrets or credentials?
* Does this modify CI/CD?
* Does this change logging?
* Does this process uploaded files?
* Does this change tenant isolation?

If the answer to any relevant question is yes, the security impact must be reviewed.

---

# 28. Security Testing

Security tests must be risk-based.

Testing should include where applicable:

## Authentication

* invalid credentials
* expired sessions
* revoked sessions
* brute-force protection

## Authorization

* unauthorized users
* incorrect roles
* another user's object identifier
* another tenant's resource identifier
* administrative routes

## Input Validation

* null
* empty
* unexpected type
* extreme length
* malformed values
* encoded input

## Injection

* SQL injection
* command injection
* template injection
* script injection

## API

* missing authentication
* malformed tokens
* unauthorized resource IDs
* unexpected request fields
* rate limits
* large requests

## Browser

* XSS
* CSRF
* security headers
* cookie configuration
* unsafe redirects

Regression tests must be created for security vulnerabilities whenever practical.

---

# 29. Security Testing Before Release

Before production release, the relevant pipeline should confirm:

```text
[ ] Lint successful
[ ] Type checking successful
[ ] Unit tests successful
[ ] Integration tests successful
[ ] Build successful
[ ] E2E tests successful
[ ] Dependency scan reviewed
[ ] Static security scan reviewed
[ ] Secret scan successful
[ ] No unresolved Critical vulnerabilities
[ ] No unresolved unauthorized security bypass
```

High-risk releases may require additional manual security review or penetration testing.

---

# 30. Vulnerability Severity

Security vulnerabilities should be classified using impact and exploitability.

Suggested categories:

## Critical

Examples:

* remote code execution
* major authentication bypass
* unrestricted administrative access
* active compromise
* mass exposure of restricted data
* exposed production master credentials

Target:

Immediate triage and containment.

Remediation should be prioritized ahead of ordinary development work.

## High

Examples:

* significant authorization bypass
* sensitive data exposure
* high-impact injection vulnerability
* privilege escalation

Target remediation:

As soon as practical, normally within 14 days.

## Medium

Examples:

* meaningful weakness requiring specific conditions
* limited information disclosure
* defense-in-depth weaknesses with realistic exploitation paths

Target remediation:

Normally within 30 days.

## Low

Examples:

* minor hardening gaps
* low-impact information exposure
* weaknesses with limited practical impact

Target remediation:

Normally within 90 days or according to the regular security backlog.

Risk may require shorter timelines regardless of category.

---

# 31. Security Incident Handling

Suspected security incidents must be escalated.

Initial response should include:

1. Identify the affected system.
2. Preserve relevant evidence.
3. Contain ongoing exposure.
4. Revoke or rotate compromised credentials.
5. Determine affected users/data/systems.
6. Fix the root cause.
7. Validate the fix.
8. Monitor for continued exploitation.
9. Document lessons learned.
10. Create preventive controls where appropriate.

Do not destroy evidence during incident response.

---

# 32. AI-Assisted Development Security

Code generated by AI assistants, including GitHub Copilot, must be treated as untrusted code until reviewed and tested.

AI-generated code must meet the same requirements as human-written code.

AI agents must never be given:

* production passwords
* private encryption keys
* unrestricted production credentials
* unnecessary sensitive customer data

Developers must review AI-generated:

* authentication logic
* authorization logic
* cryptographic operations
* SQL/database operations
* infrastructure configuration
* CI/CD workflows
* input-validation logic
* security configuration

AI-generated code must not bypass tests, suppress security warnings, or weaken existing controls simply to make a task pass.

The AI agent that generates a change must not be considered the sole security reviewer for that change.

---

# 33. GitHub Copilot Security Instructions

When implementing code, Copilot should follow this sequence:

1. Understand the security impact.
2. Identify trust boundaries.
3. Identify untrusted input.
4. Identify authentication requirements.
5. Identify authorization requirements.
6. Implement using existing security controls.
7. Add tests.
8. Test negative cases.
9. Run security-related checks.
10. Report remaining risks.

Copilot must not:

* invent credentials
* expose environment secrets
* weaken authentication
* weaken authorization
* disable validation
* disable TLS
* disable security scanning
* remove failing security tests without explanation
* add insecure dependencies simply for convenience

When uncertain about a security-sensitive implementation, the change should be highlighted for human review.

---

# 34. Threat Modeling

New high-risk features should undergo lightweight threat modeling before implementation.

At minimum identify:

### Assets

What needs protection?

### Actors

Who interacts with the system?

### Trust Boundaries

Where does data cross between trust levels?

### Entry Points

How can data enter the system?

### Threats

How could confidentiality, integrity, availability, or authorization be compromised?

### Controls

How will each significant risk be reduced?

Threat modeling is particularly important for:

* authentication
* authorization
* tenant isolation
* external integrations
* file uploads
* payment systems
* AI agents
* administrative interfaces
* new public APIs
* sensitive operational data

---

# 35. Security Exceptions

Security requirements may not be bypassed silently.

Any exception must document:

* requirement being bypassed
* business reason
* technical reason
* security risk
* mitigating controls
* responsible owner
* expiration/review date

Temporary exceptions must have a defined expiration date.

---

# 36. Definition of Done — Security

A feature is not considered complete until applicable security requirements have been addressed.

Before completion:

```text
[ ] Authentication verified
[ ] Authorization verified
[ ] Inputs validated
[ ] Outputs safely handled
[ ] Sensitive data protected
[ ] Secrets not exposed
[ ] Logging reviewed
[ ] Error handling reviewed
[ ] Dependencies reviewed
[ ] Tests added
[ ] Negative cases tested
[ ] Security scans reviewed
[ ] CI successful
```

---

# 37. Security Ownership

Security is a shared engineering responsibility.

Developers are responsible for secure implementation.

Reviewers are responsible for evaluating security impact.

Repository administrators are responsible for enforcing repository protections.

Infrastructure owners are responsible for secure runtime configuration.

Security-sensitive changes must receive appropriate review before deployment.

---

# 38. Review of This Standard

This document should be reviewed:

* at least annually
* following a significant security incident
* following a major architecture change
* when applicable security standards materially change
* when major new threat categories become relevant

Updates to this policy must be version controlled and reviewed through the normal pull-request process.

---

# Security Rule

When security and convenience conflict, the implementation must not silently weaken security.

Any necessary security trade-off must be explicit, documented, reviewed, tested, and approved.
