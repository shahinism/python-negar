# ADR-0001: Pronoun endings (-تان/-مان/-شان) stay attached after joining letters

Status: accepted (2026-10-31)

## Context
`fix_suffix_separate` split any word ending in `[تمش]ان` at the shortest stem of
two or more letters. That is a lexical guess with no dictionary, so real words were
broken: `بخشان` → `بخ‌شان`, `کشان`, `نشان`, `آتش‌فشان`. Rules also compound: the prefix
rule took `بی` off `بیخشان`, then the suffix rule split the remainder.
Each false positive was patched by adding the word to `data/immutable.words`
(~1,900 entries), and a stem-length threshold cannot fix it (`دلشان`, `بدتان` have
two-letter stems).

## Decision
- When the text is typed attached, the endings `تان/مان/شان` get a ZWNJ only after
  `ه` or `ی` (`خانه‌شان`, `پایانی‌تان`). After joining letters they stay attached
  (`کتابشان`, `بخشان`). This follows the Persian Academy convention as the author
  recalls it; verify against the official guideline.
- When the user typed a space (`کتاب شان`), the intent is clear, so
  `fix_suffix_spacing` still joins with a ZWNJ. Unchanged.
- Words the rules now leave alone are removed from `immutable.words` and listed in
  `NO_LONGER_IMMUTABLE` in `tests/test_unittest.py`, which runs them with an
  empty immutable list, in both modes.
- `بیخشان` stays in the immutable list: the prefix rule cannot tell it from `بی` + `خشان`.

## Consequences
- Removes the whole false-positive class for these endings.
- Inconsistent by design: `کتابشان` stays, `کتاب شان` becomes `کتاب‌شان`.
- Other rules (`ها`, `تر`, `گذار`...) and the prefix/suffix stacking problem are untouched.
- A known limit: a word that is a real stem + `شان` after a joining letter is no longer split.
