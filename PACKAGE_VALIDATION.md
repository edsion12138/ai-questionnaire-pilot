# Package validation

Version: 1.0.0

Checks performed before packaging:
- `plugin.json` uses the portable Agent Plugins schema URL and includes stable kebab-case name, version, and description.
- All five skill folders include required `SKILL.md` front matter with `name` and `description`.
- Python scripts pass `py_compile`.
- Example silicon-sample generator and psychometric pipeline were executed end-to-end on the bundled example configs.
- End-to-end smoke test generated N=800, complete-case N=762, parallel-analysis factor count=3, KMO≈0.852.
- Spreadsheet template was created with artifact_tool, inspected for formula errors, and visually rendered.
- Word revision-report template was rendered to four pages and every page was visually inspected.

Note: The plugin contains no MCP server and no external account connection. It is a skills-only workflow package.
