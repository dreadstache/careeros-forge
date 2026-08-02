import json
from copy import deepcopy
from pathlib import Path

from ..context import GenerationContext
from ..module import ForgeModule
from ..schema_validator import validate_json_text


class ResumeModule(ForgeModule):
    name = "resume"

    def generate(self, context: GenerationContext) -> None:
        resume_json, resume_data, source_name = self._load_data(context)
        context.render_template(
            "resume/README.md.j2",
            "resume/README.md",
            project_name=context.config.project_name,
            source_name=source_name,
        )
        context.write_text("resume/resume.json", resume_json)
        context.render_template(
            "resume/index.html.j2",
            "resume/index.html",
            resume=resume_data,
            profile_title=None,
        )
        self._generate_profiles(context, resume_data)

    def _generate_profiles(self, context: GenerationContext, resume_data: dict) -> None:
        options = context.config.module_options.get(self.name, {})
        profiles = options.get("profiles", [])
        if not isinstance(profiles, list):
            raise ValueError("resume profiles must be an array")
        for profile in profiles:
            if not isinstance(profile, dict):
                raise ValueError("each resume profile must be an object")
            slug = str(profile.get("slug", "")).strip()
            title = str(profile.get("title", "")).strip()
            if not slug or not title:
                raise ValueError("each resume profile requires slug and title")
            filtered = self._filter_profile(resume_data, profile)
            profile_json = json.dumps(filtered, indent=2, ensure_ascii=False) + "\n"
            context.write_text(f"resume/{slug}/resume.json", profile_json)
            context.render_template(
                "resume/index.html.j2",
                f"resume/{slug}/index.html",
                resume=filtered,
                profile_title=title,
            )

    @staticmethod
    def _filter_profile(resume_data: dict, profile: dict) -> dict:
        filtered = deepcopy(resume_data)
        basics = filtered.setdefault("basics", {})
        if profile.get("headline"):
            basics["headline"] = profile["headline"]
        if profile.get("summary"):
            basics["summary"] = profile["summary"]
        for section, option in (
            ("experience", "experience_ids"),
            ("skills", "skill_ids"),
            ("projects", "project_ids"),
        ):
            identifiers = profile.get(option)
            if identifiers is not None:
                allowed = set(identifiers)
                filtered[section] = [item for item in filtered.get(section, []) if item.get("id") in allowed]
        return filtered

    def _load_data(
        self, context: GenerationContext
    ) -> tuple[str, object, str | None]:
        options = context.config.module_options.get(self.name, {})
        configured_path = options.get("data_file")
        if configured_path is None:
            content = context.renderer.render("resume/resume.json.j2")
            return content, validate_json_text(content, "resume"), None

        source = Path(str(configured_path))
        if not source.is_absolute():
            source = context.config.config_directory / source
        if not source.is_file():
            raise ValueError(f"resume data file not found: {source}")

        content = source.read_text(encoding="utf-8")
        data = validate_json_text(content, "resume")
        canonical_content = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        return canonical_content, data, str(configured_path)


MODULE = ResumeModule()
