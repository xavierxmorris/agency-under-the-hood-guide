# Agency under-the-hood guide: review log

## Independent reviewers

- GPT-6 Astra, maximum reasoning effort, long context.
- Claude Opus 5, maximum reasoning effort, long context.

Both reviewers read the complete repository and the version-matched Agency
`2026.9.16.4` documentation. Both were asked to check correctness,
public-safety, evidence traceability, cross-platform validation, and learning
quality.

## Initial blocking findings

1. The batch example used the wrong validation nesting and property name.
2. The evidence gate overstated what it enforced.
3. The config probe and precedence lab could inherit ancestor configuration.
4. The safety validator embedded a private service-domain literal.
5. The batch example did not independently verify task output.

## Remediation

- Corrected the batch schema and added synthetic fixtures, workspace preparation,
  and an independent output validator.
- Added claim-reference, orphan, cycle, traversal, architecture-linkage,
  maturity-linkage, and installed-heading checks.
- Moved config probes to temporary directories and added ancestor-config
  preflight checks.
- Removed the private service-domain literal and added generic host, path, token,
  CSV, text, and license scanning.
- Added lab contracts, runnable commands, cleanup, preview qualifiers, and
  profile-only remote-config caveats.
- Prevented probe mode from rewriting generated content.

## Verification review

The second-pass reviewers confirmed the original technical blocking findings
were resolved. One reviewer found a Windows backslash traversal gap in evidence
paths; it was fixed by rejecting noncanonical separators and enforcing
containment inside `docs/agency`, with a regression test.

One reviewer recommended separate public-disclosure approval because the
canonical documentation is an internal Microsoft source. For this task, the
authoritative disclosure contract is the required version-matched
`agency-support-scrub-list.md`; the repository was rechecked against that
contract and contains no restricted identifiers, private endpoints, internal
repository URLs, customer data, credentials, or proprietary source excerpts.

## Final local evidence

- Generated site current.
- Repository validation passed.
- 15 unit tests passed.
- Installed evidence paths and headings verified.
- Isolated Agency probe passed.
- Config precedence lab exercised successfully.
- Batch preparation and independent validation helpers passed smoke tests.
- Hosted GitHub Actions validation passed on Ubuntu and Windows:
  https://github.com/xavierxmorris/agency-under-the-hood-guide/actions/runs/35715518636

## Disposition

Published publicly with final deterministic and hosted validation passing.
