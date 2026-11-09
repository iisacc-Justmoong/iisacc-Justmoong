# Language statistics

The profile chart uses GitHub's language-byte totals rather than a list of preferred languages. C++ and Python remain listed separately in the README as the languages I use.

## Scope and calculation

- Include repositories owned by `iisacc-Justmoong` that are public and not forks. Archived repositories are included.
- Exclude private repositories, organization/collaborator repositories, forks, and this profile repository. Excluding the profile prevents its chart generator from affecting the result.
- Count each repository ID once, then add each language's byte count from GitHub's [repository languages API](https://docs.github.com/en/rest/repos/repos#list-repository-languages). Each repository's current default branch is measured, not its history or all branches.
- Percentage = language bytes / total language bytes × 100. This is a code-size distribution, not time spent, proficiency, or personal authorship.
- GitHub uses [Linguist](https://github.com/github-linguist/linguist) and each repository's `.gitattributes` overrides. Generated, vendored, documentation, and other excluded files follow GitHub's classification. There is no separate source-file audit here, so unrecognized vendored/generated code can still affect the result.
- Copied code in separate non-fork repositories is counted in each repository. This does not deduplicate file contents across products and SDKs. Git submodule contents are not added separately by this script.
- Show the seven largest languages plus **Other** when there are more than eight languages. **Other** includes every remaining language. The complete byte totals and per-repository breakdown are in [assets/languages.json](assets/languages.json).
- Labels are rounded to one decimal place and can add up to slightly more or less than 100%. Bar widths use unrounded values.

## Updates and privacy

[Update language chart](https://github.com/iisacc-Justmoong/iisacc-Justmoong/actions/workflows/languages.yml) checks once daily at 03:37 UTC and can be run manually from the Actions tab. Changes to the generator, tests, or workflow also trigger a refresh. A commit is created only if the measured data or rendered chart changes. The date in the chart is the snapshot's last data change, not the last check.

The SVGs and public source data live in this repository. There is no third-party badge host, personal access token, or private-repository data. Actions uses its built-in, repository-scoped `GITHUB_TOKEN` to read GitHub's public data and commit the generated files. If any request fails, the existing chart is retained and the workflow fails instead of publishing a partial total.

GitHub language indexing and image caching can delay changes. Scheduled Actions may be delayed, and GitHub may disable schedules in public repositories after 60 days without activity. If that happens, re-enable the workflow in the Actions tab. Historical snapshots remain in this public repository's Git history.

## Local verification

Requires Python 3.10 or later and no third-party packages.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/update_languages.py
```

Without authentication, GitHub's public API rate limit is usually 60 requests per hour. The generator makes one paginated repository-list request per page plus one language request per eligible repository. An optional `GH_TOKEN` or `GITHUB_TOKEN` is sent only to `api.github.com`; never commit it.
