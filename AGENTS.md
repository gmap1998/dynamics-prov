# Repository Agent Instructions

This project mixes Python backend code and a React/TypeScript frontend.
While there are no automated tests, run basic checks after making changes:

1. `python -m py_compile $(git ls-files '*.py')`
2. `npm run build`

If these commands fail due to missing dependencies or network restrictions, mention it in the PR description.
