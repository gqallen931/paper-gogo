# Public GitHub repository setup

This package is published as a public repository:

- URL: <https://github.com/gqallen931/paper-gogo>
- Visibility: **Public**

## Pre-publication checklist

Run these checks before publishing content to a public repository. This package passed all of them on the date of its public release.

1. Credential scan: no API keys, tokens, private keys, `.env` files, or credential files.
2. Identity scan: no author identifiers, personal email addresses, or affiliation leakage beyond public attribution.
3. Manuscript and data scan: no unpublished manuscripts, reviewer reports, embargoed data, or third-party confidential material.
4. License review: every bundled third-party skill must permit redistribution. Record the license and upstream source in `THIRD_PARTY_NOTICES.md`.
5. Encoding check: all text files must be valid UTF-8 with no mojibake.

## Publishing updates

If the repository is already initialized, push updates directly:

```powershell
git add -A
git commit -m "Describe the change"
git push
```

If you are publishing to a new repository:

```powershell
git init -b main
git add -A
git commit -m "Paper-gogo v2 public release"
gh repo create paper-gogo --public --source . --remote origin --push
```

## Before adding content

- Remove manuscript PDFs, unpublished data, reviewer reports, author identifiers, credentials, tokens, `.env` files, and private logs.
- Confirm the license of any newly added third-party skill before redistribution.
- Re-run the credential, identity, and encoding scans above.
- Use `Get-Content -Encoding UTF8` on Windows PowerShell when inspecting Chinese text; plain `Get-Content` can produce mojibake.

## Reverting to private

If private development is needed again, switch visibility back rather than forking the content:

```powershell
gh repo edit gqallen931/paper-gogo --visibility private --accept-visibility-change-consequences
```

Note that content already published may persist in forks, caches, and third-party indexes; making a repository private does not recall it.
