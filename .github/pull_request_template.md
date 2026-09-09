## Summary

<!-- In 2-4 sentences, explain what this PR changes and why. -->

## Related issue

Closes #

## Problem

<!-- Describe the user-visible or technical problem. -->

## Root cause

<!-- For bug fixes, explain why the defect occurred. For features, explain the relevant design/implementation context. -->

## Solution

<!-- Explain the approach taken and why it is the smallest safe solution. -->

## Changes made

- 
- 
- 

## Acceptance criteria

<!-- Copy the issue acceptance criteria and mark each one only after it has been verified. -->

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Testing

### Automated tests added or updated

- [ ] Regression test
- [ ] Unit tests
- [ ] Component tests
- [ ] Integration tests
- [ ] End-to-end tests
- [ ] Not applicable — explain below

Details:

<!-- Name the important test files, scenarios, and behaviors covered. -->

### Checks executed

- [ ] Lint
- [ ] Formatting check
- [ ] Type check
- [ ] Unit / component tests
- [ ] Integration tests
- [ ] Build
- [ ] End-to-end tests
- [ ] Relevant security checks

Commands / CI jobs run:

```text
# Example:
# npm run lint
# npm run typecheck
# npm test
# npm run build
```

## Manual QA

<!-- Record exactly what was manually verified. -->

- [ ] Reproduced the original defect before the fix, when practical
- [ ] Confirmed the reported defect is fixed
- [ ] Tested the happy path
- [ ] Tested relevant error / empty / loading states
- [ ] Tested relevant permissions / roles
- [ ] Tested responsive behavior where applicable

Manual QA notes:

## Screenshots / recordings

<!-- Required for meaningful UI changes when practical. Add before/after evidence. -->

| Before | After |
| --- | --- |
|  |  |

## API / database impact

- [ ] No API contract change
- [ ] API contract changed — documented below
- [ ] No database/schema change
- [ ] Database/schema changed — migration and rollback documented below

Details:

## Security / privacy impact

- [ ] No known security/privacy impact
- [ ] Authentication/authorization affected
- [ ] Sensitive data handling affected
- [ ] Input validation affected
- [ ] Security review recommended

Details:

## Regression risks

<!-- What existing behavior could be affected by this change? -->

- 

## Rollback plan

<!-- Explain how this change can be safely reverted or disabled if necessary. -->

## Copilot / author self-review

- [ ] The change fixes the root cause rather than only hiding the symptom
- [ ] No unrelated refactor is included
- [ ] Existing legitimate tests were not weakened to make CI pass
- [ ] New tests would fail if the defect were reintroduced
- [ ] Error handling is intentional
- [ ] Logs do not expose secrets or sensitive data
- [ ] Acceptance criteria are fully covered
- [ ] Known limitations and follow-up work are documented
