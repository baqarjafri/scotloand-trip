# Surah Al-Falaq (113): numbers, letters, structure and protection

Part 1 of a study of the *Mu'awwidhatayn* (the two "refuge" surahs, 113 and 114). This part covers Al-Falaq.
Part 2 ([02-al-falaq-counter-pattern.md](02-al-falaq-counter-pattern.md)) reads the surah as a counter-pattern to sorcery. An-Nas and the combined analysis come next; section 9 previews them.

> قُلْ أَعُوذُ بِرَبِّ ٱلْفَلَقِ ۝١ مِن شَرِّ مَا خَلَقَ ۝٢ وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ ۝٣
> وَمِن شَرِّ ٱلنَّفَّٰثَٰتِ فِى ٱلْعُقَدِ ۝٤ وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ ۝٥
>
> Say: I seek refuge in the Lord of the Daybreak (1) from the evil of what He created (2), from the evil of
> darkness when it settles (3), from the evil of those who blow on knots (4), and from the evil of an envier
> when he envies (5).

## How to read this document

Each point is tagged so you can tell solid ground from interpretation:

| Tag | Meaning |
|---|---|
| **[Fact]** | Computed from the text or a fixed property of the mushaf. Anyone can recheck it. |
| **[Tradition]** | From hadith or classical tafsir. The grading is given where it matters. |
| **[Reflection]** | A symbolic or numerological reading. It is meaningful for contemplation (*tadabbur*), but it is not proof. |

All counts and abjad values were computed with `abjad_analysis.py` (in this folder) from the Quranic Arabic Corpus
morphology file (Uthmani text, 77,429 words, 6,236 verses). Nothing was copied from numerology websites.

**Abjad conventions used:** the eastern (Mashriqi) abjad: ا1 ب2 ج3 د4 ه5 و6 ز7 ح8 ط9 ي10 ك20 ل30 م40 ن50 س60 ع70 ف80
ص90 ق100 ر200 ش300 ت400 ث500 خ600 ذ700 ض800 ظ900 غ1000. Each written letter counts once, so a shadda is not doubled.
Hamza forms count as alif (1).

---

## 1. Key facts at a glance

| Item | Value | Note |
|---|---|---|
| Position | 113th of 114 surahs | Second to last; with An-Nas it closes the mushaf. **[Fact]** |
| Verses | 5 | Global verses **6226–6230** of 6236. **[Fact]** |
| Words | 23 | 4 + 4 + 5 + 5 + 5. **[Fact]** |
| Letters | **71** in the Uthmani rasm, 73 in modern spelling | The difference is النفّٰثٰت, written without its two alifs in the Uthmani script. 71 matches the traditional count. **[Fact]** |
| Distinct letters | 20 of 28 | Absent: ج ه ز ط ك ص ض ظ. **[Fact]** |
| Abjad total | **8675** (Uthmani) / 8677 (modern spelling) | 9607 if shaddas are doubled. The total depends on convention (see §7). **[Fact]** |
| Revelation order | 20th (An-Nas 21st) | Traditional order based on narrations from Ibn Abbas. Marked Makki in the standard mushaf, though many scholars consider it Madani and link it to the sorcery incident in Madinah. **[Tradition]** |
| Mushaf location | Juz 30, page 604 (Madinah mushaf) | It shares the final page with Al-Ikhlas and An-Nas. **[Fact]** |

---

## 2. Its position in the Quran

### 2.1 The number 113 points to its own structure: 1 + 1 + 3 = 5 verses **[Fact]**
The digit sum of the surah's number equals its number of verses:

| Surah | Digit sum | Verses |
|---|---|---|
| 112 Al-Ikhlas | 1+1+2 = **4** | **4** |
| 113 Al-Falaq | 1+1+3 = **5** | **5** |
| 114 An-Nas | 1+1+4 = **6** | **6** |

I checked all 114 surahs. This holds for only four of them: 66 (At-Tahrim, 6+6 = 12 verses), 112, 113 and 114.
**The three "Qul" surahs at the end of the Quran are the only consecutive run.** These are the same three surahs the
Prophet ﷺ told us to recite together three times morning and evening. The verse counts 4-5-6 rise by one, matching the
surah numbers 112-113-114.

### 2.2 The last prime-numbered surah **[Fact]**
113 is a prime number, the 30th prime. 114 is not prime, so Al-Falaq is the highest prime-numbered surah in the Quran.
**[Reflection]** A prime cannot be divided by anything except 1 and itself. It is a natural symbol for something that
cannot be broken into or split apart, which suits a surah of impenetrable refuge.

### 2.3 The mushaf opens and closes with *ruqya* **[Tradition]**
- Al-Fatiha, the first surah, is itself called a *ruqya*. When a companion recited it over a man stung by a scorpion,
  the Prophet ﷺ asked, "How did you know that it is a ruqya?" (Bukhari 2276).
- Al-Falaq and An-Nas, the last two surahs, are the *Mu'awwidhatayn*, "the two that give refuge".

**[Reflection]** The Quran is physically wrapped in protection: healing at the front cover, refuge at the back. Both
ends also name Allah as **Rabb**: *Rabb al-'alamin* (1:2), *Rabb al-falaq* (113:1) and *Rabb an-nas* (114:1).

### 2.4 The letter "bookends" **[Fact]**
Al-Fatiha famously does not contain 7 letters: ث ج خ ز ش ظ ف. Al-Falaq contains four of them: **ش ف خ ث**. The letter
**ش** appears only inside the word **شَرّ** ("evil"). Together, Al-Fatiha, Al-Falaq and An-Nas use 26 of the 28
letters. Only **ز** and **ظ** are absent from all three.

**[Reflection]** The opening surah of praise has no "sh" for *sharr*. The closing refuge surahs are where evil is
finally named, four times, so that refuge can be sought from it.

---

## 3. Structure: one refuge against four evils

```
v1  قُلْ أَعُوذُ بِرَبِّ ٱلْفَلَقِ          THE REFUGE      (one Lord, one attribute)
v2  مِن شَرِّ مَا خَلَقَ                  evil #1  general: everything created
v3  وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ         evil #2  hidden in TIME   (darkness / night)
v4  وَمِن شَرِّ ٱلنَّفَّٰثَٰتِ فِى ٱلْعُقَدِ   evil #3  hidden in ACTION (sorcery)
v5  وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ         evil #4  hidden in the HEART (envy / evil eye)
```

- **One general, then three specific evils [Fact].** Verse 2 covers every created harm. Verses 3–5 then single out
  three, joined by **وَ** ("and"). *Min sharri* (مِن شَرِّ) appears **4 times**, and the letter ش appears **4 times**.
- **The word pattern 4-4-5-5-5 follows the meaning [Fact].** The two "framing" verses (the refuge and the general
  evil) have 4 words each. The three specific evils have 5 words each.
- **All three specific evils are unseen [Reflection, built on the tafsir].** Darkness hides an attacker, sorcery
  works in secret, and envy lives inside a person. The surah is about harms you cannot see coming. That is why the
  scholars made it the core of *ruqya* against sihr and the evil eye.
- **Light against darkness [Reflection].** You seek refuge in the Lord of the *Falaq*, the daybreak that splits the
  night, from evils that need darkness: the night itself, secret knots and hidden envy.
- **"إذا" ("when") appears twice [Fact].** Darkness harms *when it settles*, and the envier harms *when he envies*.
  Classical commentators also note that غاسق and حاسد are indefinite: not every night is harmful, and not every
  envier acts on it. **[Reflection]** The evils are conditional and limited to certain moments. The refuge, *Rabb
  al-Falaq*, comes with no condition at all.
- **The surah names the two times the Sunnah says to recite it [Reflection, built on hadith].** It names dawn
  (*al-falaq*) and nightfall (*ghasiq idha waqab*). The Prophet ﷺ prescribed reciting it **morning and evening**,
  exactly these two boundaries of the day (Abu Dawud 5082; Tirmidhi 3575).

---

## 4. The words

### 4.1 Abjad values, word by word **[Fact]**

| v | Word | Meaning | Abjad | Letters |
|---|---|---|---|---|
| 1 | قل | Say | 130 | 2 |
| 1 | **أعوذ** | I seek refuge | **777** | 4 |
| 1 | برب | in the Lord | 204 | 3 |
| 1 | **الفلق** | of the Daybreak | **241** | 5 |
| 2 | من | from | 90 | 2 |
| 2 | شر | the evil | 500 | 2 |
| 2 | ما | of what | 41 | 2 |
| 2 | خلق | He created | 730 | 3 |
| 3 | ومن | and from | 96 | 3 |
| 3 | شر | the evil | 500 | 2 |
| 3 | غاسق | darkness | 1161 | 4 |
| 3 | إذا | when | 702 | 3 |
| 3 | وقب | it settles | 108 | 3 |
| 4 | ومن | and from | 96 | 3 |
| 4 | شر | the evil | 500 | 2 |
| 4 | النفثت | those who blow | 1061 (1063 in modern spelling) | 6 (8) |
| 4 | فى | on | 90 | 2 |
| 4 | العقد | the knots | 205 | 5 |
| 5 | ومن | and from | 96 | 3 |
| 5 | شر | the evil | 500 | 2 |
| 5 | حاسد | an envier | 73 | 4 |
| 5 | إذا | when | 702 | 3 |
| 5 | حسد | he envies | 72 | 3 |

**Verse totals:** 1352 · 1361 · 2567 · 1952 · 1443 = **8675**

### 4.2 أَعُوذُ = 777, and the word appears exactly 7 times in the Quran
- **[Fact]** أ(1) + ع(70) + و(6) + ذ(700) = **777**.
- **[Fact]** The first-person form أعوذ ("I seek refuge"), counting وأعوذ, appears **exactly 7 times** in the whole
  Quran:

  | Ref | Speaker | Seeking refuge from |
  |---|---|---|
  | 2:67 | Musa | being among the ignorant |
  | 11:47 | Nuh | asking what he has no knowledge of |
  | 19:18 | Maryam | the stranger (Jibril, in human form) |
  | 23:97 | The Prophet ﷺ (commanded) | the incitements of the devils |
  | 23:98 | The Prophet ﷺ (commanded) | the devils' presence |
  | 113:1 | Every reciter ("Say") | the evils of creation |
  | 114:1 | Every reciter ("Say") | the whisperer |

- **[Tradition]** Seven is the number the Sunnah attaches to protection:
  - "Whoever eats **seven** 'ajwa dates in the morning, neither poison nor **sihr** will harm him that day"
    (Bukhari 5445).
  - For pain, the Prophet ﷺ taught: say *Bismillah* three times, then **seven times**
    *"A'udhu bi'izzatillahi wa qudratihi min sharri ma ajidu wa uhadhir"* (Muslim 2202). The word *a'udhu* is
    literally repeated seven times.
  - Al-Fatiha, the other ruqya surah, is *as-sab' al-mathani*, "the seven oft-repeated verses".
- **[Reflection]** This is the strongest numerical link in the surah. The word that opens it is 7-7-7. It occurs 7
  times in revelation, and the prophets who used it were the ones under the heaviest pressure: Musa facing his people,
  Nuh facing the flood, Maryam alone, and the Prophet ﷺ against the shayatin. Al-Falaq hands their exact word to every
  believer.

### 4.3 The shared opening قُلْ أَعُوذُ بِرَبِّ = **1111** **[Fact]**
130 + 777 + 204 = **1111**. These three words open **both** Al-Falaq and An-Nas.
- Al-Falaq v1 = 1111 + الفلق (241) = **1352**
- An-Nas v1 = 1111 + الناس (142) = **1253**

**[Reflection]** The common gateway of the two refuge surahs is a repdigit of 1, the numeral of *tawhid*. It comes
directly after Al-Ikhlas, *"Qul huwa Allahu Ahad"* ("He is One"). See §9 for the mirror between 241 and 142.

### 4.4 Root echoes across the Quran **[Fact]** (with **[Reflection]**)

| Root | Occurrences in the Quran | Where |
|---|---|---|
| **ف-ل-ق** (split open) | **4** | 6:95 *fāliq al-ḥabb* (splits the seed), 6:96 *fāliq al-iṣbāḥ* (splits the dawn), 26:63 *fanfalaqa* (the sea split for Musa), 113:1 |
| **غ-س-ق** (deep darkness) | 4 | 17:78 (prayer until the darkness of night), 38:57 and 78:25 (*ghassāq*, a dark fluid of Hell), 113:3 |
| **و-ق-ب** (to settle in, enter) | **1, here only** | a hapax: it occurs nowhere else in the Quran |
| **ن-ف-ث** (to blow, spit lightly) | **1, here only** | a hapax |
| **ع-ق-د** (knot, binding) | **7** | 2:235 and 2:237 (marriage knot), 4:33 and 5:89 (oaths), 5:1 (contracts), **20:27 Musa: "untie the knot from my tongue"**, 113:4 |
| **ح-س-د** (envy) | 5 | 2:109, 4:54, 48:15, and twice in 113:5 |

- **ف-ل-ق, splitting that rescues.** Every Quranic use is Allah breaking something open to bring out life, light or
  safety: life from a dead seed, light from night, and a road through the sea that saved Musa from Pharaoh.
  **[Reflection]** *Rabb al-Falaq* is "the Lord whose way is to break through what encloses". That is exactly what a
  person under a knot, a spell or a dark weight needs.
- **ع-ق-د, the knot.** In 6 of its 7 uses, a knot is something sacred: marriage, oaths, covenants. Sorcery in 113:4 is
  the knot corrupted. The only plea to *untie* a knot comes from Musa (20:27). **[Reflection]** Musa links several of
  these threads. He is the first speaker of أعوذ (2:67), the sea split for him (26:63), he asked for a knot to be
  untied (20:27), and he defeated Pharaoh's sorcerers ("the sorcerer will not succeed wherever he comes", 20:69).
- **Hapax words.** وَقَبَ and ٱلنَّفَّٰثَٰت appear nowhere else in the Quran. **[Reflection]** Both describe the most
  hidden mechanisms, darkness *seeping in* and *covert* blowing. The vocabulary for them appears only once, inside the
  surah built to counter them.

### 4.5 Notable individual values **[Fact]**
- **غاسق = 1161**, the heaviest word. It holds **غ (1000)**, the highest-valued letter in the abjad, which appears
  only once in the surah. Verse 3 (darkness) is therefore the highest-valued verse at 2567. **[Reflection]** The
  "weight" of the surah sits in the darkness verse.
- **شر = 500**, four times, giving **2000** for "evil". **ش (300)** occurs only in this word.
- **الفلق = 241**, a prime number. "Lord of the Daybreak" is رب الفلق = 443, also prime.
- **حاسد = 73** and **حسد = 72**. 73 is also the surah's letter count in modern spelling. This is a curiosity, not a
  strong finding, because it depends on the spelling convention.

---

## 5. The letters

### 5.1 Frequency **[Fact]**
ا 11 · **ق 6** · ل 6 · و 5 · ر 5 · م 5 · ن 5 · **ش 4** · ذ 3 · ب 3 · ف 3 · س 3 · د 3 · ع 2 · ح 2 · خ 1 · **غ 1** · ث 1 · ت 1 · ي 1

- **ق (100) is the signature letter.** It opens the surah (**ق**ل), closes verses 1 and 2 (الفل**ق**, خل**ق**), and
  appears 6 times. Only alif occurs more often, and ل ties it at 6. It is a letter of strength (*isti'la'*) and
  *qalqala*.
- The surah has **7 written shaddas** (بِرَبِّ, شَرِّ ×4, and two in ٱلنَّفَّٰثَٰتِ). This is another 7.

### 5.2 Every verse ends on a *qalqala* (echoing) letter **[Fact]**
The verse endings are الفلق**ْ** – خلق**ْ** – وقب**ْ** – العقد**ْ** – حسد**ْ**, that is **ق ق ب د د**. All five are
*qalqala* letters (ق ط ب ج د). When you pause on them, they "bounce" with a strong echo.
**[Reflection]** *Qalqala* literally means shaking or jolting. Each verse ends on a sound like a snap, which suits a
surah associated with breaking knots. An-Nas, by contrast, ends every verse on **س**, a soft hissing whisper letter
that matches *al-waswas*. See §9.

### 5.3 No emphatic "itbaq" letters **[Fact]**
All four "covered" emphatic letters (*huruf al-itbaq*: **ص ض ط ظ**) are absent. So are ج ه ز ك. The surah is built
from 20 letters.

---

## 6. Linking the numbers to the protection

This is the synthesis you asked for. Each line ties a number to the protective function and gives its basis.

| Number | Where it appears in Al-Falaq | Protective link | Basis |
|---|---|---|---|
| **1** | One Lord, one attribute (*Rabb al-Falaq*); opening = 1111 | The refuge is single and unconditional, even though the threats are many | [Fact] + [Reflection] |
| **3** | Three specific hidden evils: darkness, sorcery, envy | Recite **3×** morning, **3×** evening and **3×** before sleep (blowing into the palms and wiping the body) | Abu Dawud 5082, Tirmidhi 3575, Bukhari 5017 |
| **4** | *Min sharri* ×4; ش ×4; root ف-ل-ق ×4 | Four doors of harm closed by one key. Each of the 4 "splittings" in the Quran is a rescue | [Fact] + [Reflection] |
| **5** | 5 verses; 1+1+3 = 5 | Recite after each of the **5** daily prayers | Abu Dawud 1523, Tirmidhi 2903 |
| **7** | أعوذ = 777; أعوذ ×7 in the Quran; 7 shaddas; root ع-ق-د ×7 | 7 'ajwa dates against sihr; *a'udhu* said 7× over pain | Bukhari 5445, Muslim 2202 |
| **11** | 5 + 6 = 11 verses of the Mu'awwidhatayn | The narration of the **11 knots**: each verse recited untied one knot | Al-Baghawi, from Muqatil and al-Kalbi. **Weak chain** (see below) |
| **Dawn / dusk** | *al-falaq* and *ghasiq* | The surah names the morning and evening it is recited in | [Reflection] on the hadith |

### Why this surah protects, according to the sources **[Tradition]**
- **Revealed as unmatched refuge.** "Have you not seen verses revealed tonight, the like of which has never been seen?
  *Qul a'udhu bi Rabbil-falaq* and *Qul a'udhu bi Rabbin-nas*" (Muslim 814). And to 'Uqbah: "Seek refuge with these
  two, for no one has ever sought refuge with anything like them" (Abu Dawud 1463).
- **Jinn and the evil eye.** "The Prophet ﷺ used to seek refuge from the jinn and from the evil eye of humans until
  the Mu'awwidhatayn were revealed. When they were revealed, he took them and left everything else"
  (Tirmidhi 2058, Ibn Majah 3511; graded hasan/sahih).
- **The evil eye is real.** "Al-'ayn haqq" (Bukhari 5740, Muslim 2188). Scholars such as Ibn al-Qayyim explain that
  the eye is an outgrowth of envy, which is why verse 5 (*hasid*) is read as the evil-eye verse.
- **Sorcery.** The Prophet ﷺ was affected by sorcery done by Labid ibn al-A'sam, using a comb and hair hidden in a
  palm spathe in the well of Dharwan (Bukhari 5763, Muslim 2189). That sahih account does **not** give the number of
  knots or say the surahs were revealed at that moment. The detail of **11 knots untied by 11 verses** comes from
  al-Baghawi's tafsir, which reports it from Muqatil and al-Kalbi. Hadith critics consider both narrators weak. So the
  11 = 11 link is best used as a beautiful symbol, not as an authenticated report.
- **The moon (the celestial link).** 'A'isha said the Prophet ﷺ looked at the moon and said: "Seek refuge with Allah
  from the evil of this, for this is *al-ghasiq idha waqab*" (Tirmidhi 3366, hasan sahih). Other views say it means
  the night when it falls (Ibn Abbas and others), or the setting of the Pleiades. This is the surah's one link to the
  heavens.
- **His final illness.** He recited the Mu'awwidhat over himself and blew. When he became too weak, 'A'isha recited
  them and wiped his own hand over him (Bukhari 5016).

### A note on "extra-terrestrial" and paranormal influences
Al-Falaq itself names four things: created things in general, darkness or the night (and the moon, per the hadith
above), sorcery, and envy. **Jinn are named explicitly in An-Nas** (114:6, *min al-jinnati wan-nas*), not in Al-Falaq.
Through the hadith of Abu Sa'id above, however, the Prophet's ﷺ practice shows the pair covers jinn and the evil eye.
Nothing in the text or the hadith refers to "aliens" in the modern sense. The surah's own category is broader: *min
sharri ma khalaq*, "the evil of **everything** He created", seen or unseen, earthly or celestial.

---

## 7. Totals, and how much weight they can bear

| Convention | Letters | Abjad |
|---|---|---|
| Uthmani rasm, shadda once | 71 | **8675** |
| Modern spelling, shadda once | 73 | 8677 (a prime number) |
| Uthmani, shadda doubled | 78 | 9607 |

The grand total moves with every spelling choice, so no stable meaning can be built on it. The findings that **do not
depend on convention** are the strongest ones:

1. The digit sum of the surah number equals its verse count, which holds only for the final three surahs as a
   consecutive run (§2.1).
2. أعوذ = 777, and the word occurs exactly 7 times (§4.2).
3. The shared opening = 1111, followed by the mirror الفلق 241 ↔ الناس 142 (§4.3, §9).
4. Every verse ends on a qalqala letter (§5.2).
5. The hapax roots, and the "splitting = rescue" pattern of ف-ل-ق (§4.4).

**Lighter curiosities.** These are worth noting, but they could easily be chance:
- 71 letters is the **20th** prime. The surah uses **20** distinct letters and was the **20th** surah revealed.
- 23 words matches the **23** years of revelation.
- Its first global verse number, 6226, is a palindrome.

### A candid note on method
I computed well over a hundred quantities across this surah. With that many numbers, some "meaningful-looking"
matches are statistically guaranteed. That is why everything above is ranked. Historically, abjad was used for
chronograms and in the *'ilm al-huruf* tradition (al-Buni and others). Many scholars, Ibn Khaldun among them,
cautioned against using it for divination or talismans. In the hadith, the protection of Al-Falaq comes from
**reciting it with trust in Allah**, as the Prophet ﷺ did, at the times and counts he set. The Sunnah counts are 1
after each prayer and 3 in the morning, evening and before sleep. Fixed counts found in folk practice, such as 41 or
100, have no basis in the hadith. The numbers in this document are best used to **deepen attention to the words**,
not as a mechanism of their own.

---

## 8. Summary: the "numerical signature" of Al-Falaq

- **Position:** 113, prime, with digits that sum to its 5 verses. It is one of only three consecutive surahs with
  this property, and it sits in the protective "seal" of the mushaf, mirroring the ruqya of Al-Fatiha.
- **Words:** it opens with **777** (أعوذ, a 7-times word in the Quran), inside the shared gateway **1111**. Evil (شر,
  500) is named 4 times against 1 Lord.
- **Letters:** 71 letters (Uthmani), 20 distinct letters, no emphatic letters, ق as the signature letter, and every
  verse ending in a qalqala snap.
- **Structure:** 1 refuge, then 1 general evil, then 3 hidden evils (time, action, heart). Dawn against darkness. It
  names the very times, morning and evening, at which it is to be recited.
- **Combination:** 5 + 6 = 11 verses with An-Nas, which carries the 11-knots symbolism.

---

## 9. Preview of Part 2: the combination with An-Nas

Already computed with the same method. These will be developed fully in Part 2:

| | Al-Falaq | An-Nas | Combined |
|---|---|---|---|
| Verses | 5 | 6 | **11** |
| Words | 23 | 20 | 43 |
| Letters (Uthmani) | 71 | 80 | **151**, a palindromic prime |
| Abjad | 8675 | 4901 | 13576 |
| Name / key word | الفلق = **241** | الناس = **142** | **mirror numbers**; 241 + 142 = **383**, a palindromic prime; difference = **99** |
| Distinct letters | 20 | 20 | **24**. Each surah supplies exactly 4 letters the other lacks (Falaq: ح ت ث غ; Nas: ج ه ك ص); both lack ز ط ض ظ |
| Verse endings | ق ق ب د د: hard qalqala "snaps" | س ×6: soft whisper | outer force against inner whisper |
| Attributes of Allah : evils | **1 : 4** (*Rabb*; four evils) | **3 : 1** (*Rabb, Malik, Ilah*; one evil) | |
| Kind of evil | **External**: harm done *to* you by others | **Internal**: the whisper that leads *you* to sin | |

The last row follows Ibn al-Qayyim's division in his treatise on the Mu'awwidhatayn. Evil reaches a person either
from their own sins, whose root is the whisper (An-Nas), or from harm done to them by others, human, jinn or creature
(Al-Falaq). He held the first to be the greater danger, which may be why An-Nas calls on three attributes against a
single evil.

---

## Sources

- Quranic text and roots: Quranic Arabic Corpus morphology data,
  [mustafa0x/quran-morphology](https://github.com/mustafa0x/quran-morphology).
- Traditional count (5 verses / 23 words / 71 letters):
  [Alukah, تفسير سورة الفلق](https://www.alukah.net/sharia/1001/150084/).
- The 11-knots narration: [al-Baghawi, Ma'alim at-Tanzil on 113:1](https://quran-tafsir.net/baghawy-ashour-mobdii/sura113-aya1.html).
- The moon hadith: [Tirmidhi 3366](https://islamtics.com/hadith/tirmidhi/3366/).
- Ibn al-Qayyim's two kinds of evil, as summarised in
  [لطائف من سورة الفلق](https://e3arabi.com/%D8%A7%D9%84%D8%A2%D8%AF%D8%A7%D8%A8/%D9%84%D8%B7%D8%A7%D8%A6%D9%81-%D9%85%D9%86-%D8%B3%D9%88%D8%B1%D8%A9-%D8%A7%D9%84%D9%81%D9%84%D9%82/).
- Hadith references (standard numbering): Bukhari 2276, 5016, 5017, 5445, 5740, 5763; Muslim 814, 2188, 2189, 2202;
  Abu Dawud 1463, 1523, 5082; Tirmidhi 2058, 2903, 3366, 3575; Ibn Majah 3511.

To reproduce every number: download the morphology file (see the header of `abjad_analysis.py`) and run
`python3 abjad_analysis.py quran-morphology.txt 113`.
