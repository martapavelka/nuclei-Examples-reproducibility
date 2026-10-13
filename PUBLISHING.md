# Maintaining this repository on GitHub

Target: https://github.com/martapavelka/nuclei-Examples-reproducibility

The remote repository already exists. Do not run `gh repo create` or create another repository.

## Update with Git

For later updates, clone the existing repository and work in the cloned directory.

```bash
git clone https://github.com/martapavelka/nuclei-Examples-reproducibility.git
cd nuclei-Examples-reproducibility
# Edit the files you want to update before continuing.
git add .
git commit -m "Update Examples reproducibility materials"
git push
```

This requires a local Git installation, a configured commit identity, and GitHub authentication (for example, an already authenticated GitHub CLI or Git Credential Manager). Do not paste passwords, access tokens, or private keys into ChatGPT. If GitHub has changes that are not in your local clone, pull and reconcile those changes before pushing; do not force-push.

For small documentation changes, use GitHub's web editor: open the file, click the pencil icon, make the change, and commit it. For larger updates, upload the changed files or use Git as shown above. Preserve the six package directories, `scripts/`, and the top-level dependency and documentation files. Do not upload a distribution ZIP in place of the extracted files.

## Verify after upload

At the repository root:

```bash
python3 scripts/quick_check.py
```

This checks hashes and quick deterministic verifiers; it does not repeat the costly exhaustive MILP and SAT searches.

Before final publication, the authors should confirm any licensing terms for their original programs and data and review redistribution terms for the bundled third-party `plantri` archive. No license has been assigned to the original work here.

For scholarly referencing, cite a fixed Git commit or release and add the paper's final bibliographic details to `README.md`. A Zenodo DOI may be useful for archival citation.
