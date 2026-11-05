"""Stage 5 -- Assemble the portable output package."""

from __future__ import annotations

import os

from ..profile.models import Profile
from ..profile import store
from ..render.templates import SKELETON_FILES, render_all
from ..utils import privacy
from .session import Session


def run(s: Session, p: Profile, base_dir: str) -> None:
    s.note("\n[bold cyan]Stage 5 / 5[/bold cyan]  [b]Assemble[/b]\n")

    # Safety net: never persist sensitive categories that slipped through.
    for layer in ("facts", "preferences", "notes"):
        bucket = getattr(p, layer)
        for key in list(bucket.keys()):
            if privacy.is_sensitive(f"{key} {bucket[key]}"):
                s.note(f"[yellow]Redacted sensitive field:[/yellow] {key}")
                bucket[key] = privacy.redact(bucket[key])

    out_dir = store.profile_dir(base_dir)
    os.makedirs(out_dir, exist_ok=True)

    rendered = render_all(p)
    written = []
    for fname, content in rendered.items():
        path = os.path.join(out_dir, fname)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        written.append(fname)

    profile_path = store.save_profile(p, base_dir)
    written.append(os.path.basename(profile_path))

    s.note("[green]Done.[/green] Wrote the following into:")
    s.note(f"  [cyan]{out_dir}[/cyan]")
    for f in written:
        s.note(f"  - {f}")
    s.note("\nDrop these into any agent that supports a SOUL/IDENTITY/USER/MEMORY skeleton.")
