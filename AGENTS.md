# Repository Agent Instructions

The original repository included a React/TypeScript frontend, but that code is no longer present. Only a minimal Node project remains along with some Python utilities.

When making changes, run the following check:

1. `python -m py_compile $(git ls-files '*.py')`

There is currently no frontend build step. `npm run build` is not required.

If this command fails due to missing dependencies or environment restrictions, mention it in the PR description.
