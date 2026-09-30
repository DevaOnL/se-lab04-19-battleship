# Scenario 19 — Battleship vs AI

A terminal Battleship game with separate board and AI modules.

## Provided files

- `main.py` — entry point.
- `game.py` — turn flow and setup.
- `board.py` — ship and shot state.
- `ai.py` — computer targeting.
- `requirements.txt` — dependency declaration.

## Setup

```bash
python main.py
```

## Before changing the code

Inspect how coordinates are represented in every module. Fire at known ship cells and
known empty cells. Then trace an AI shot from selection to hit detection.

## Task 1 — Consistent coordinate handling

Make coordinate representation consistent across input, ship placement, player shots,
and AI shots so occupied cells are recognised correctly.

**Done when:** every real ship coordinate is treated as a hit and every known empty
coordinate is treated as a miss.

## Task 2 — Complete fleet and win logic

Support multiple ships, track individual ship damage, identify sunk ships, prevent
repeated shots, and end the game when the fleet is sunk.

## Task 3 — Improve the AI

After a hit, make the AI preferentially consider nearby untried cells. It must never
shoot the same coordinate twice and must handle a board with no remaining choices.

## Task 4 — Shot-level feedback

Ensure hit/miss/sunk feedback occurs exactly once for an actual shot. Internal AI
candidate selection must not produce false hit/miss messages.

## Required testing

Test hits, misses, repeated shots, sinking one ship, sinking all ships, AI repeated-shot
prevention, adjacent targeting after a hit, invalid coordinates, and quitting.


## LLM usage

You may use an LLM during the lab. The goal is to use it as a coding assistant while
retaining responsibility for understanding and testing the result.

- Inspect the existing code before asking for changes.
- Ask for explanations when you do not understand a proposed change.
- Test generated code against the stated behaviour and edge cases.
- Keep your complete LLM chat history for submission.
- Do not replace the whole project with an unrelated implementation.
- Keep all state in memory; do not add CSV, JSON, SQLite, or other persistence.

## Submission checklist

- [x] Task 1 completed and the original defect was reproduced and fixed.
- [x] Tasks 2–4 completed and tested.
- [x] Boundary and invalid-input cases tested.
- [x] No unnecessary external dependencies added.
- [x] No persistent storage added.
- [x] Code remains understandable and modular.
- [ ] Complete LLM chat-history link included.

## Folder structure

```text
scenario-07-battleship/
├── README.md
├── requirements.txt
├── main.py
├── game.py
├── board.py
└── ai.py
```

## Submission Checklist

Submission is only the following three things:

- [x] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [x] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history

## Completed lab implementation

Tasks 1–4 are implemented. Internal coordinates are zero-based `(row, column)` tuples;
terminal input/output uses `1–6`. Each side has three ships of lengths 3, 2, and 1.
Shots update the target board, track individual damage, reject repeats, and produce
one outcome message. The AI follows hits with nearby untried cells and handles
exhaustion. Both fleets can win. Enter `q` to quit.

Run the game and the 21 behavioral regression tests from this directory:

```bash
python main.py
python -m unittest -v
```

No game dependencies or persistent storage were added. The original files remain
in this repository's Git history; the changes retain the board/AI/game modules.

### Lab-4 submission

- [Report (PDF)](Lab-4/PES1UG24CS145_SE_Lab4.pdf)
- [Report (DOCX)](Lab-4/PES1UG24CS145_SE_Lab4.docx)
- [Before gameplay — 10 seconds](Lab-4/Videos/before_gameplay.mp4)
- [After gameplay — 10 seconds](Lab-4/Videos/after_gameplay.mp4)
- [Chat-history export (PDF)](Lab-4/PES1UG24CS145_SE_Lab4_Chat_History.pdf)
- [Chat-history export (DOCX)](Lab-4/PES1UG24CS145_SE_Lab4_Chat_History.docx)
- [Updated code snapshot](Lab-4/Updated_Code)
- [Test results](Lab-4/Evidence/tests.txt)
- [Original defect reproduction](Lab-4/Evidence/original_defects.txt)

The videos capture actual seeded pseudo-terminal sessions rendered as terminal
frames; both last exactly 10 seconds. Ordinary gameplay uses unseeded randomness.
The before video was captured before editing the source. Chat exports include the
available user/assistant conversation through their recorded export cutoff. A
separate ChatGPT/Codex platform share URL has not been provided.
