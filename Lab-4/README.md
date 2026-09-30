# Lab 4 — VibeCoding: Battleship vs AI

Devansh Gupta · PES1UG24CS145 · Section C

This folder contains the handout deliverables and the requested report.

| Deliverable | File / folder |
| --- | --- |
| Final report | [PDF](PES1UG24CS145_SE_Lab4.pdf) · [DOCX](PES1UG24CS145_SE_Lab4.docx) |
| Original gameplay | [10-second before video](Videos/before_gameplay.mp4) |
| Completed gameplay | [10-second after video](Videos/after_gameplay.mp4) |
| Updated implementation and tests | [Updated_Code](Updated_Code/) |
| Available conversation export | [PDF](PES1UG24CS145_SE_Lab4_Chat_History.pdf) · [DOCX](PES1UG24CS145_SE_Lab4_Chat_History.docx) |
| Verification | [21 passing tests](Evidence/tests.txt) · [Original defects](Evidence/original_defects.txt) |

From `Updated_Code`, run `python main.py` to play and `python -m unittest -v`
to verify the implementation. This is an exact submission snapshot of the root
Python modules and requirements file.

Both replacement videos capture actual gameplay in the VS Code integrated Bash
terminal, matching the lab window’s dark theme, font, prompt, and controls. RNG seed
7 makes the comparison reproducible. Input is automated. The before clip reruns
the original source preserved before code edits. The after clip includes repeat rejection, hits,
a miss, an AI hit followed by adjacent targeting, sinking named ships, and victory.
The game itself does not seed the RNG or write persistent data.

The chat export captures available user and assistant messages through its stated
cutoff, plus clarification prompts. It is not a platform-generated share link;
that URL has not been supplied. The final delivery message necessarily follows
the export cutoff.
