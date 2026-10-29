# Unicode regression fixtures

Twenty small fixtures for English, Russian, Kazakh and emoji transport, by [Olzhas Azirali](https://aziral.com/en/olzhas-azirali) / [AZIRAL](https://aziral.com). [Try Unicode Text Lab](https://aziral.com/en/tools/unicode-text-checker) in a browser.

Catch a lost joiner, an unexpected normalization step or an encoding-count regression before publishing. The raw text in fixtures.json is paired with explicit code-point labels so an invisible edit cannot silently change the example.

## Run offline

From the repository root:

    python3 examples/unicode-regression/verify.py
    node examples/unicode-regression/verify.mjs
    python3 -m unittest discover -s tests -v

Python 3.10+ uses the standard library. The optional JavaScript check uses Node.js 20+ with Intl.Segmenter and TextEncoder. No package install, API key or network request is involved. Both verifiers print JSON and leave the fixture file unchanged. An optional path argument checks a separate copy.

Python checks scalar identity, code points, UTF-8 bytes and UTF-16 code units. It explicitly reports graphemes as not measured. JavaScript checks those counts plus the recorded grapheme expectation. A runtime without Intl.Segmenter reports partial_no_segmenter, leaves grapheme values null and the JavaScript CLI exits 2. A mismatch or invalid input exits 1; a complete passing CLI check exits 0.

## What is in the file?

- English punctuation, Russian text and upper/lowercase Kazakh letters.
- Composed and decomposed accents, kept distinct.
- A supplementary emoji, a ZWJ sequence and its unjoined counterpart.
- Skin-tone, flag, keycap and family sequences.
- LF versus CRLF, non-ASCII spaces, zero-width spaces and directional isolates.

Each fixture has raw text, codePointsHex and expected counts in four named units. The file records the actual reference runtime: Node 26.8.2, Unicode 17.0, ICU 78.3, CLDR 48.0; encoding values were independently checked with Python 3.14.7, Unicode database 16.0.0. Every run prints its current runtime so differences remain visible.

Grapheme expectations were observed with Intl.Segmenter using locale en and granularity grapheme. They are regression fixtures for that recorded behavior, not a claim of complete Unicode conformance. Investigate a version-dependent mismatch before changing an expectation. The verifiers never regenerate the fixture data.

## Keep a joiner explicit in a published example

Some editing paths can drop invisible characters. This JavaScript string spells out the woman, zero-width joiner and laptop:

    const text = "\u{1F469}\u200D\u{1F4BB}";
    console.log(text.length); // 5 UTF-16 code units
    console.log([...text].length); // 3 Unicode code points
    console.log(new TextEncoder().encode(text).length); // 11 bytes
    console.log([...new Intl.Segmenter("en", {
      granularity: "grapheme"
    }).segment(text)].length); // 1 in the reference runtime

The JSON text field contains the actual sequence. Its codePointsHex entry includes U+200D, so removing the joiner fails verification. Neither verifier strips controls, changes line endings inside a decoded string or normalizes accents.

## Limits

A grapheme cluster does not guarantee one rendered glyph or a fixed display width. This pack supplies no linguistic word model, reading-time estimate, translation score or social-platform character limit. Unpaired surrogates are outside its Unicode-scalar scope and are rejected. This is a focused regression set, not the Unicode conformance test suite.

References: [Unicode text segmentation](https://www.unicode.org/reports/tr29/), [Intl.Segmenter](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter), [Python text sequences](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str).

## По-русски

20 примеров для проверки русского, английского, казахского текста и emoji. Проверки сохраняют исходник, различают кодовые точки, байты UTF-8, кодовые единицы UTF-16 и графемы. Версии среды указаны явно. Число графем не означает число нарисованных знаков или ширину текста. Набор не оценивает перевод и не задаёт лимиты соцсетей. [Браузерная версия](https://aziral.com/tools/unicode-text-checker).

## Қазақша

Орысша, ағылшынша, қазақша мәтін мен emoji үшін 20 мысал. Тексеру бастапқы мәтінді өзгертпейді; Unicode код нүктелері, UTF-8 байттары, UTF-16 код бірліктері және графемалар бөлек көрсетілген. Орта нұсқалары жазылған. Графема саны мәтіннің экрандағы енін білдірмейді. Бұл жинақ аударма сапасын бағаламайды және әлеуметтік желі шегін белгілемейді. [Браузердегі құрал](https://aziral.com/kk/tools/unicode-text-checker).

MIT under the repository [LICENSE](../../LICENSE). Original fixture selection and verification tools by Olzhas Azirali / AZIRAL. Unicode, JavaScript, Python and linked projects retain their own authorship and marks.

