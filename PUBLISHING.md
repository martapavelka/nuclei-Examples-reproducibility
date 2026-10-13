# Publishing this repository on GitHub

Target: https://github.com/martapavelka/nuclei-Examples-reproducibility

The remote repository already exists. Do not run `gh repo create` or create another repository.

## Upload with Git

Extract the distribution archive and open a terminal inside its `nuclei-Examples-reproducibility` folder.

```bash
git init -b main
git add .
git commit -m "Publish Section 3 reproducibility materials"
git remote add origin https://github.com/martapavelka/nuclei-Examples-reproducibility.git
git push -u origin main
```

This requires a local Git installation, a configured commit identity, and GitHub authentication (for example, an already authenticated GitHub CLI or Git Credential Manager). Do not paste passwords, access tokens, or private keys into ChatGPT. If the remote repository already has a commit, do not force-push; reconcile its history first.

Alternatively, on GitHub, use `Add file` > `Upload files` and drag the **contents** of the extracted folder into the upload area. Preserve all six directories at the repository root, along with `README.md`, `PUBLISHING.md`, `requirements-recommended.txt`, `scripts/`, and `.gitignore`. Never upload just the single ZIP archive. Browser uploads are limited to 100 files at a time; this distribution contains fewer than 100.

## Verify after upload

At the repository root:

```bash
python3 scripts/quick_check.py
```

This checks hashes and quick deterministic verifiers; it does not repeat the costly exhaustive MILP and SAT searches.

Before final publication, the authors should confirm any licensing terms for their original programs and data and review redistribution terms for the bundled third-party `plantri` archive. No license has been assigned to the original work here.

For scholarly referencing, cite a fixed Git commit or release and add the paper's final bibliographic details to `README.md`. A Zenodo DOI may be useful for archival citation.
