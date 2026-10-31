# ADR-0002: ای after a silent ه — indefinite/copula vs vocative

Status: accepted (2026-10-31)

## Context
`fix_suffix_spacing` joined every standalone `ای` to the previous word. That is right for
the indefinite and the 2nd-person copula (`خانه‌ای`, `خسته‌ای`) but breaks the vocative,
very common in poetry: `گفتا که ای دوست` → `که‌ای دوست`, and `\s+` even glued a verse-initial
`ای` onto the previous line. The same words can carry either reading
(`دیده ای مهربان`: "a kind eye" in prose, "you have seen, O kind one" in verse), so no
purely lexical rule is complete. A POS tagger was rejected: heavy, and taggers trained
on prose are unreliable on classical verse.

An opt-in `poem` flag was tried and dropped: the user should not have to classify the text.

## Decision
Join `ای` only after a silent ه, across a single space on the same line, and decide by
cues, first match wins (`PersianEditor._join_ai`):
1. Host is a vocative-prone function word (`که چه به نه ده مه همه`) or ends in `اه`
   (pronounced h: `شاه`, `راه`; their indefinite is `شاهی`) → keep.
2. Next word is a known addressee (`جان دوست دل یار خدا…`) → keep.
3. Word before the host is a determiner (`یک چه چنین هر…`) → join.
4. Nothing follows (line/hemistich end, punctuation), or the next word is a function word
   or a verb → join. The key fact: a vocative must be followed by its addressee, a noun.
5. Addressee followed by `!` or `من/ما` → keep.
6. No cue: join if the line reads as prose (a sentence-final period, or > 14 words with no
   hemistich gap), otherwise keep the user's spacing.

Errors are asymmetric: a wrong join adds an error, a missed join leaves the text as typed,
so ties go to "keep".

## Consequences
- One default behaviour for prose and verse, no option.
- Known misses (left as typed): short prose lines without a period and without a cue
  (`خانه ای بزرگ خریدیم`), verbs outside the small verb list (`بنوشت`), `ای` after ی.
- Known wrong joins: a vocative after an ه-word in a prose-like line whose addressee is
  not in the list.
- The word lists are the tuning knobs; grow them from real misclassifications, with a test.
