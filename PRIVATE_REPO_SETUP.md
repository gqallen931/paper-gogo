# Private GitHub repository setup

This package is prepared for a private repository. Keep the repository private until all manuscript, data, reviewer, credential, and identity checks are complete.

## GitHub web route

1. Create a new repository on GitHub.
2. Set **Visibility** to **Private**.
3. Do not initialize it with a README, license, or `.gitignore` if you will upload this complete package.
4. Upload the extracted package contents, keeping `SKILL.md` at the repository root.
5. Confirm the repository still shows the **Private** badge before inviting collaborators.

## GitHub CLI route

Run these commands from the extracted `Paper-gogo-v2` directory:

```powershell
git init
git add .
git commit -m "Initial private Paper-gogo v2 package"
gh repo create Paper-gogo-v2 --private --source . --remote origin --push
```

## Before changing visibility

- Remove manuscript PDFs, unpublished data, reviewer reports, author identifiers, credentials, tokens, `.env` files, and private logs.
- Check third-party skill licenses before public redistribution.
- Re-run citation, privacy, and secret scans.
- Never make the repository public merely to simplify installation.

