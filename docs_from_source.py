"""Generate the code reference pages and navigation."""

import logging
from pathlib import Path

import mkdocs_gen_files

SRC_PATH = "samudra"
DOC_PATH = ""

nav = mkdocs_gen_files.Nav()

for path in sorted(Path(SRC_PATH).rglob("*.py")):
    module_path = path.relative_to(SRC_PATH).with_suffix("")
    doc_path = path.relative_to(SRC_PATH).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)
    if len(parts) == 1:
        continue
    # print(parts)
    # print(len(parts))

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    nav[parts] = doc_path.as_posix()
    # DOC_FILE = full_doc_path.parts[-1]
    # FULL_DOC_DIR = Path(DOC_PATH, *full_doc_path.parts[:-1])
    # FULL_DOC_DIR.mkdir(parents=True, exist_ok=True)

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: samudra.{ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open(Path("reference", "SUMMARY.md"), "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
