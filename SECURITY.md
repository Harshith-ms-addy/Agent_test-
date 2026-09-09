# Security Policy

Security is important to the Thinxsense project.

If you discover a security vulnerability, please report it responsibly rather than opening a public GitHub issue.

## Supported Versions

Security fixes are provided for the currently maintained version of Thinxsense.

| Version                    | Supported |
| -------------------------- | --------- |
| Latest release             | ✅         |
| Active development branch  | ✅         |
| Older unsupported releases | ❌         |

Support status may change as the project evolves.

---

## Reporting a Security Vulnerability

Please **do not create a public GitHub issue** for suspected security vulnerabilities.

Use GitHub Private Vulnerability Reporting if it is enabled for this repository.

If private vulnerability reporting is unavailable, contact the Thinxsense maintainers privately through the approved project security contact.

Do not publish vulnerability details publicly until the maintainers have had a reasonable opportunity to investigate and remediate the issue.

---

## What to Include

Please provide as much relevant information as possible.

Include:

* A clear description of the vulnerability
* The affected component or feature
* Affected version or commit
* Steps to reproduce
* Proof of concept, if available
* Expected behavior
* Actual behavior
* Potential security impact
* Required permissions or prerequisites
* Relevant logs or screenshots
* Suggested mitigation, if known

Please remove passwords, access tokens, API keys, private keys, customer information, or other sensitive data before submitting evidence.

---

## Example Vulnerability Report

A useful report should answer:

**Vulnerability**

What security issue did you discover?

**Affected Component**

Which endpoint, page, API, service, or component is affected?

**Steps to Reproduce**

1. Authenticate as the required user role.
2. Navigate to the affected functionality.
3. Send the relevant request or perform the relevant action.
4. Observe the unexpected security behavior.

**Expected Result**

Describe the secure behavior that should occur.

**Actual Result**

Describe what occurs instead.

**Impact**

Explain what an attacker may be able to access, modify, execute, disclose, or disrupt.

**Environment**

Include relevant information such as:

* Thinxsense version
* Commit SHA
* Browser
* Operating system
* API version
* Deployment environment

---

## Vulnerability Handling Process

After receiving a security report, the Thinxsense maintainers will attempt to:

1. Acknowledge the report.
2. Reproduce and validate the vulnerability.
3. Determine severity and affected components.
4. Identify the root cause.
5. Develop a remediation.
6. Add regression tests where practical.
7. Review related code for similar vulnerabilities.
8. Validate the fix.
9. Release or deploy the remediation.
10. Coordinate disclosure when appropriate.

A vulnerability should not be considered resolved solely because the reported exploit no longer works.

The underlying root cause should be addressed whenever practical.

---

## Severity

Security issues may be classified as:

### Critical

Examples include:

* Remote code execution
* Authentication bypass
* Administrative account compromise
* Exposure of production secrets
* Large-scale unauthorized access to sensitive information

Critical vulnerabilities require immediate investigation.

### High

Examples include:

* Significant authorization bypass
* Privilege escalation
* Sensitive information disclosure
* High-impact injection vulnerabilities

### Medium

Examples include:

* Limited unauthorized access
* Security weaknesses requiring specific conditions
* Significant security misconfiguration

### Low

Examples include:

* Minor information disclosure
* Defense-in-depth weaknesses
* Low-impact security configuration issues

Severity will be determined based on exploitability, privileges required, affected data, user impact, and system impact.

---

## Responsible Disclosure

We ask security researchers to:

* Report vulnerabilities privately.
* Avoid accessing data that does not belong to you.
* Avoid modifying or deleting user data.
* Avoid disrupting Thinxsense services.
* Avoid denial-of-service testing without explicit authorization.
* Avoid social engineering.
* Avoid publicly disclosing vulnerabilities before remediation coordination.
* Stop testing if you encounter sensitive user or production information.

Only perform security testing on systems and environments you are authorized to test.

---

## Secrets and Credentials

If you discover an exposed credential such as:

* API key
* password
* access token
* refresh token
* private key
* cloud credential
* database credential

report it immediately through the private security reporting process.

Do not use the credential beyond what is necessary to confirm that it appears valid.

Exposed credentials should be treated as compromised and rotated or revoked.

---

## Scope

Security reports may include vulnerabilities involving:

* Authentication
* Authorization
* Access control
* API security
* Cross-tenant access
* Sensitive data exposure
* SQL injection
* Command injection
* Cross-site scripting
* Cross-site request forgery
* Server-side request forgery
* Path traversal
* File upload vulnerabilities
* Session management
* Cryptography
* Secrets exposure
* Dependency vulnerabilities
* CI/CD security
* Infrastructure configuration
* Privilege escalation
* Business logic vulnerabilities

General bugs that do not have security impact should be reported through the normal GitHub issue process.

---

## Security Development Practices

Thinxsense aims to follow secure software development practices including:

* Least privilege
* Defense in depth
* Secure-by-default configuration
* Server-side authorization
* Input validation
* Dependency scanning
* Secret scanning
* Static security analysis
* Automated testing
* Pull request review
* Protected production branches
* Security regression testing

AI-generated code, including code produced by GitHub Copilot or other development agents, must meet the same security requirements as human-written code.

---

## Public Issues

Do not include the following in public GitHub issues:

* Exploitable vulnerability details
* Production credentials
* API keys
* Authentication tokens
* Private keys
* Customer information
* Sensitive infrastructure details
* Reproduction steps for an unpatched critical vulnerability

Use the private vulnerability reporting process instead.

---

## Security Updates

Security fixes may be released without publishing complete exploitation details immediately when doing so helps protect users while they update.

Additional vulnerability information may be disclosed after remediation when appropriate.

---

## Questions

For normal implementation questions, feature requests, and non-security bugs, use the project's standard GitHub issue process.

For anything that could represent a security vulnerability, use the private security reporting process.
