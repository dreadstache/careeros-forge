# CareerOS Forge

> Forge projects. Build careers.

CareerOS Forge is a Python project scaffolding tool for generating
professional repository structures from configuration files. It is intended to
turn a small `forge.json` manifest into a ready-to-open workspace with sensible
folders, starter documentation, and project hygiene files.

## Current Status

CareerOS Forge is in the `0.1.0` foundation phase. It includes a reliable base
generator plus automatic discovery of optional modules. The first working
module, `resume`, creates a truthful-data-first resume workspace.

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
- **Module expansion**: Use the `modules` list in `forge.json` to select
  automatically discovered scaffolds. The `resume` module is available now;
  GitHub workflows, backend, frontend, database, portfolio, analytics, GIS,
  games, and music remain planned.
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

### 2026-08-01

- Added a module registry that automatically discovers bundled Forge modules.
- Added a shared generation context and module interface.
- Added the always-on `base` module and the optional `resume` module, which
  generates a starter resume README and structured JSON data file when selected.
- Added CLI reporting for generated, skipped, and unknown module names.
- Added a packaged Jinja template layer and migrated the base and resume modules
  away from hard-coded generated content.
- Added packaged JSON Schemas for `forge.json` and resume data. Configuration is
  validated before generation, and rendered resume JSON is validated before it
  is written.
- Added typed experience, education, skill, and project records plus a
  print-friendly HTML resume generated from the same validated data.
- Added module-scoped input configuration so the resume module can generate its
  canonical JSON and HTML output from a populated, validated career-data file.

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
  ],
  "module_options": {
    "resume": {
      "data_file": "career-data.json"
    }
  }
}
```

### Configuration Fields

| Field | Required | Current behavior | Intended behavior |
| --- | --- | --- | --- |
| `project_name` | Yes | Names the generated project folder and starter README heading. | Continue serving as the canonical generated project name. |
| `output_directory` | No | Defaults to `./generated` when omitted. | Continue controlling where generated workspaces are written. |
| `modules` | No | Defaults to `["base"]`; `base` always runs and other discovered module names generate optional scaffolds. Unknown names are reported and ignored for forward compatibility. | Select optional template packs and feature-specific scaffolds. |
| `module_options` | No | Supplies module-scoped settings. `resume.data_file` points to validated career JSON relative to `forge.json`. | Configure modules without coupling their settings to the core generator. |

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

Selecting `resume` also creates:

```text
resume/
├── index.html
├── README.md
└── resume.json
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

Generate and open the populated example resume with one command:

```bash
careeros-forge --config examples/forge.example.json --preview
```

The example is derived from verified source-CV material and intentionally omits
street address, phone number, references, and unsupported platform claims.

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

- Add an example career-data file and preview command for a populated resume.
- Add more independently discoverable modules.
- Add richer generated documentation such as architecture, roadmap, and
  contribution guides.
- Add migration/versioning support as career-data schemas evolve.
