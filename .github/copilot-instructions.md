# all projects Copilot Instructions

## General
- Understand the existing implementation before modifying code.
- Do not refactor unrelated code while fixing bugs.
- Prefer small, reviewable changes.
- Do not change public APIs unless explicitly required.

## Bug Fixing
For every bug:
1. Reproduce the reported behavior.
2. Identify the root cause.
3. Add a regression test that reproduces the bug.
4. Confirm the regression test fails before the fix.
5. Implement the smallest reasonable fix.
6. Confirm the regression test passes.
7. Run related tests.
8. Run the complete test suite if practical.
9. Report exactly what was tested.

Never mark a bug fixed only because the code looks correct.

## Testing
For every code change consider:
- Happy path
- Negative cases
- Boundary cases
- Empty/null values
- Invalid inputs
- Permission/access-control behavior
- Loading states
- Error states
- API failures
- Network failures where applicable
- Regression tests
- Existing functionality that might be affected

Prefer unit tests for business logic.
Use integration tests for API/database/service interactions.
Use E2E tests for critical user journeys.

Do not create tests that simply duplicate the implementation.

## UI Changes
For UI bugs verify:
- Desktop layout
- Mobile/responsive layout
- Loading state
- Empty state
- Error state
- Disabled state where applicable
- Form validation
- Keyboard interaction where applicable

## Before completing a task
Run:
- lint
- type checking
- relevant unit tests
- relevant integration tests
- relevant E2E tests

Do not ignore failing tests.

## Pull Requests
PR descriptions must contain:
- Problem
- Root cause
- Solution
- Files changed
- Tests added
- Tests executed
- Risks / possible regressions
