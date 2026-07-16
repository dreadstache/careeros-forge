# CareerOS Forge

> Forge projects. Build careers.

CareerOS Forge is a Python project scaffolding tool for generating
professional repository structures from configuration files. It is intended to
turn a small `forge.json` manifest into a ready-to-open workspace with sensible
folders, starter documentation, and project hygiene files.

## Current Status

CareerOS Forge is in the `0.1.0` foundation phase. The current implementation
focuses on a reliable base generator that can be expanded with modular templates
for the wider CareerOS ecosystem.

## Intended Functions

CareerOS Forge is intended to provide the following functions as it grows:

- **Configuration loading**: Read a `forge.json` file that describes the project
  name, output directory, and requested modules.
- **Project root creation**: Create a new project directory under the configured
  output path.
- **Base folder scaffolding**: Generate a standard repository layout for common
  application areas, including backend, frontend, database, docs, templates,
  assets, scripts, and exports.
- **Starter documentation**: Create an initial project `README.md` so each
  generated workspace begins with a documented entry point.
- **Git hygiene setup**: Add a `.gitignore` with common Python, environment,
  database, and Node dependency exclusions.
- **Empty directory preservation**: Add `.gitkeep` files to scaffolded folders so
  empty directories can be tracked by Git.
- **Command-line execution**: Run from the command line with `python -m
  careeros_forge` or the installed `careeros-forge` script.
- **Module expansion**: Use the `modules` list in `forge.json` as the future
  extension point for optional scaffolds such as GitHub workflows, backend,
  frontend, database, portfolio, resume, analytics, GIS, games, and music
  project assets.
- **Template-driven generation**: Move starter files toward reusable templates so
  generated output can be customized without changing generator logic.
- **CareerOS ecosystem readiness**: Produce repositories that are ready for VS
  Code, documentation, version control, and future CareerOS-specific automation.

## Updated Functionality Notes

Use this section to record functionality changes as development proceeds. Each
entry should briefly explain what changed, where it changed, and how to verify
it.

### 2026-07-16

- Documented the current generator behavior and intended future module functions
  in this README.
- Confirmed that v0.1 currently creates the configured project root, standard
  base directories, `.gitkeep` files, a generated README, and a generated
  `.gitignore`.

## Configuration

CareerOS Forge expects a `forge.json` file in the directory where the command is
run. A typical configuration looks like this:

```json
{
  "project_name": "CareerOS",
  "output_directory": "../generated",
  "modules": [
    "base",
    "github",
    "backend",
    "frontend",
    "database",
    "portfolio",
    "resume",
    "analytics",
    "gis",
    "games",
    "music"
  ]
}
```

### Configuration Fields

| Field | Required | Current behavior | Intended behavior |
| --- | --- | --- | --- |
| `project_name` | Yes | Names the generated project folder and starter README heading. | Continue serving as the canonical generated project name. |
| `output_directory` | No | Defaults to `./generated` when omitted. | Continue controlling where generated workspaces are written. |
| `modules` | No | Defaults to `["base"]`; currently stored but not yet used to branch generation. | Select optional template packs and feature-specific scaffolds. |

## Generated Structure

The current generator creates the following structure:

```text
<output_directory>/<project_name>/
├── .gitignore
├── README.md
├── assets/
│   └── .gitkeep
├── backend/
│   └── .gitkeep
├── database/
│   └── .gitkeep
├── docs/
│   └── .gitkeep
├── exports/
│   └── .gitkeep
├── frontend/
│   └── .gitkeep
├── scripts/
│   └── .gitkeep
└── templates/
    └── .gitkeep
```

## Run

From the repository root:

```bash
python -m careeros_forge
```

If the package is installed, the console script can also be used:

```bash
careeros-forge
```

## Development

Install the project in editable mode before running local checks:

```bash
python -m pip install -e .
```

Run tests with:

```bash
pytest
```

## v0.1 Goal

- Read `forge.json`
- Create folders
- Generate README and `.gitignore`
- Leave a project ready for VS Code

## Roadmap

- Wire `modules` to actual template packs.
- Replace hard-coded starter content with packaged templates.
- Add richer generated documentation such as architecture, roadmap, and
  contribution guides.
- Add validation and clearer CLI feedback for malformed configuration files.
- Add tests for configuration defaults, missing configuration, and module-driven
  generation.
