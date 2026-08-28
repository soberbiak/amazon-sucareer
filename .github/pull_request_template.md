## Problem

Describe the problem this PR solves.

## Change

Summarize the implementation and affected files.

## Validation

- [ ] `python3 skills/amazon-ops-evidence/scripts/validate_ledger.py examples/fictional-experienced/claim-ledger.json`
- [ ] `python3 skills/amazon-ops-profile/scripts/validate_profile.py examples/fictional-experienced/profile.json examples/fictional-experienced/claim-ledger.json`
- [ ] `python3 skills/amazon-ops-resume/scripts/build_resume.py examples/fictional-experienced/resume.json /tmp/experienced-resume.html`
- [ ] `python3 skills/amazon-ops-interview/scripts/score_session.py examples/fictional-interview/session.json`
- [ ] `python3 -m unittest discover -s tests -p 'test_*.py'`

## Privacy / evidence review

- [ ] No real resumes, contact details, employer/store/brand names, ASIN/SKU, internal business data, screenshots, credentials, or lightly anonymized source material are included.
- [ ] New examples are synthetic and marked `fictional: true` where applicable.
- [ ] The change does not strengthen Ownership, causality, metrics, or claims beyond available evidence.

## Notes

Add limitations, follow-up work, or compatibility notes here.
