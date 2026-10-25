#!/usr/bin/env python3
"""
New Project Bootstrap Wizard with Framework Presets
Initializes a new software project created from this meta-generator template.
Supports framework architecture presets (Web, Backend, Game, CLI, Library)
and external directory target bootstrapping.
"""
import sys
import os
import shutil
import argparse
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PRESETS = {
    "web": {
        "title": "Modern Web Application",
        "modules": ["ui", "state", "api_client"],
        "src_dirs": ["ui", "state", "services"],
        "docs_modules": ["ui.md", "state.md"]
    },
    "backend": {
        "title": "REST / Microservice Backend",
        "modules": ["gateway", "services", "persistence"],
        "src_dirs": ["api", "services", "storage"],
        "docs_modules": ["gateway.md", "persistence.md"]
    },
    "game": {
        "title": "Interactive Game / Simulation",
        "modules": ["engine", "renderer", "state"],
        "src_dirs": ["engine", "render", "state"],
        "docs_modules": ["engine.md", "renderer.md"]
    },
    "cli": {
        "title": "Command-Line Tool / Automation",
        "modules": ["cli_dispatcher", "commands", "config"],
        "src_dirs": ["cli", "commands", "utils"],
        "docs_modules": ["cli_dispatcher.md"]
    },
    "library": {
        "title": "Standalone Modular Library",
        "modules": ["core", "adapters"],
        "src_dirs": ["core", "adapters"],
        "docs_modules": ["core.md"]
    }
}

MODULE_STUB_TEMPLATE = """# Module: {module_name}

Scope: Technical Architecture - Subsystem {module_name}
Related: docs/tech/overview.md, docs/ARCHITECTURE.md

## 1. Responsibilities & Boundaries
- **Owns:** Subsystem contracts, internal logic, and specifications for `{module_name}`.
- **Does NOT Own:** Cross-cutting authentication or infrastructure drivers.

## 2. Invariants (Hard Rules)
- All public functions in `{module_name}` must validate parameter contracts at boundary.
- Zero circular dependencies allowed with sibling modules.

## 3. Specifications & Interfaces
### Exported Signatures
```typescript
export interface {class_name}Service {{
  execute(params: Record<string, any>): Promise<any>;
}}
```

## 4. Decisions & Revisions
- {date}: Initial module specification bootstrapped from template preset.
"""

def scaffold_preset_modules(root_dir: Path, preset_name: str, today_str: str):
    """Scaffolds preset modules into docs/tech/modules/ and creates src/ directories."""
    preset = PRESETS.get(preset_name)
    if not preset:
        return

    docs_mod_dir = root_dir / "docs" / "tech" / "modules"
    docs_mod_dir.mkdir(parents=True, exist_ok=True)

    src_dir = root_dir / "src"
    src_dir.mkdir(parents=True, exist_ok=True)

    tests_dir = root_dir / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)

    for mod in preset["modules"]:
        class_name = "".join(part.capitalize() for part in mod.split("_"))
        mod_doc = docs_mod_dir / f"{mod}.md"
        if not mod_doc.exists():
            content = MODULE_STUB_TEMPLATE.format(
                module_name=mod,
                class_name=class_name,
                date=today_str
            )
            mod_doc.write_text(content, encoding="utf-8")
            print(f"  📐 Scaffolded preset spec: docs/tech/modules/{mod}.md")

        # Create matching src/ folder
        mod_src = src_dir / mod
        mod_src.mkdir(parents=True, exist_ok=True)
        init_file = mod_src / "__init__.py"
        if not init_file.exists():
            init_file.write_text(f'"""{class_name} subsystem package."""\n', encoding="utf-8")

        # Create matching tests/ folder
        mod_test = tests_dir / mod
        mod_test.mkdir(parents=True, exist_ok=True)
        test_file = mod_test / f"test_{mod}.py"
        if not test_file.exists():
            test_file.write_text(f'''import unittest

class Test{class_name}(unittest.TestCase):
    def test_baseline(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
''', encoding="utf-8")

def bootstrap(name: str, description: str, preset: Optional[str] = None, target_dir: Optional[str] = None):
    from datetime import datetime
    today_str = datetime.now().strftime("%Y-%m-%d")

    root = Path(target_dir).resolve() if target_dir else Path.cwd()
    print("=" * 65)
    print(f"🚀 BOOTSTRAPPING NEW PROJECT: '{name}'")
    print(f"   Root Directory: {root}")
    if preset:
        print(f"   Architecture Preset: {preset.upper()} ({PRESETS.get(preset, {}).get('title', '')})")
    print("=" * 65)

    # 1. Update .agent/config.json
    config_path = root / ".agent" / "config.json"
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["workspace"]["name"] = name
            if preset:
                config["workspace"]["preset"] = preset
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
            print(f"  ✅ Updated .agent/config.json with project: '{name}'")
        except Exception as e:
            print(f"  ⚠️ Could not update .agent/config.json: {e}")

    # 2. Update docs/product/overview.md
    product_overview = root / "docs" / "product" / "overview.md"
    if product_overview.exists():
        content = product_overview.read_text(encoding="utf-8")
        lines = content.splitlines()
        if lines and lines[0].startswith("# "):
            lines[0] = f"# Product Overview: {name}"
        product_overview.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"  ✅ Updated docs/product/overview.md title")

    # 3. Apply Architecture Preset if specified
    if preset and preset in PRESETS:
        scaffold_preset_modules(root, preset, today_str)

    # 4. Check / Initialize Git & Install Pre-Commit Hooks
    git_dir = root / ".git"
    if not git_dir.exists():
        try:
            subprocess.run(["git", "init"], cwd=str(root), check=True, capture_output=True)
            print("  ✅ Initialized fresh Git repository (.git/)")
        except Exception:
            pass

    hooks_installer = root / "scripts" / "install_hooks.py"
    if hooks_installer.exists():
        try:
            subprocess.run([sys.executable, str(hooks_installer)], cwd=str(root), check=True, capture_output=True)
            print("  ✅ Automatically activated Git pre-commit compliance hooks")
        except Exception:
            pass

    # 5. Regenerate doc index
    idx_script = root / "scripts" / "generate_doc_index.py"
    if idx_script.exists():
        subprocess.run([sys.executable, str(idx_script)], cwd=str(root), capture_output=True)

    # 6. Run full health audit
    print("\n▶ Running health audit on fresh project...")
    audit_script = root / "scripts" / "audit_repo.py"
    if audit_script.exists():
        res = subprocess.run([sys.executable, str(audit_script)], cwd=str(root), capture_output=True, text=True, encoding="utf-8")
        print(res.stdout.strip())

    print("\n" + "=" * 65)
    print(f"✨ Project '{name}' successfully bootstrapped and ready for autonomous cascade!")
    print("=" * 65)

def main():
    parser = argparse.ArgumentParser(description="Bootstrap a new software project from this template.")
    parser.add_argument("--name", required=True, type=str, help="Name of the new software project")
    parser.add_argument("--description", default="New software project bootstrapped from agentic template", type=str, help="Project summary description")
    parser.add_argument("--preset", choices=list(PRESETS.keys()), help="Architectural framework preset (web, backend, game, cli, library)")
    parser.add_argument("--target-dir", help="Target directory to initialize (defaults to current repository root)")

    args = parser.parse_args()
    bootstrap(args.name, args.description, preset=args.preset, target_dir=args.target_dir)

if __name__ == "__main__":
    main()
