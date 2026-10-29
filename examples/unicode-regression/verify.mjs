#!/usr/bin/env node
/** Check scalar text, encoding sizes and recorded grapheme expectations offline. */
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const metrics = ['codePoints', 'utf8Bytes', 'utf16CodeUnits', 'graphemeClusters'];

export function verify(data, { segmenter = typeof Intl.Segmenter === 'function'
  ? new Intl.Segmenter('en', { granularity: 'grapheme' }) : null } = {}) {
  if (!data || typeof data !== 'object' || data.schemaVersion !== 1) throw new Error('expected schemaVersion 1');
  if (!Array.isArray(data.fixtures) || data.fixtures.length === 0) throw new Error('fixtures must be a nonempty array');
  const ids = new Set();
  const checks = data.fixtures.map(fixture => {
    const name = fixture?.id;
    if (typeof name !== 'string' || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name) || ids.has(name)) {
      throw new Error('fixture IDs must be unique lowercase ASCII identifiers');
    }
    ids.add(name);
    const text = fixture.text;
    if (typeof text !== 'string') throw new Error(`${name}: text must be a string`);
    const characters = [...text];
    if (characters.some(char => char.codePointAt(0) >= 0xD800 && char.codePointAt(0) <= 0xDFFF)) {
      throw new Error(`${name}: unpaired surrogate outside scalar-value scope`);
    }
    if (!fixture.expected || metrics.some(metric => !Number.isSafeInteger(fixture.expected[metric]) || fixture.expected[metric] < 0)) {
      throw new Error(`${name}: expected metrics must be nonnegative integers`);
    }
    const points = characters.map(char => `U+${char.codePointAt(0).toString(16).toUpperCase().padStart(4, '0')}`);
    if (JSON.stringify(points) !== JSON.stringify(fixture.codePointsHex)) {
      throw new Error(`${name}: source text differs from codePointsHex; inspect transport or editing`);
    }
    const actual = {
      codePoints: characters.length,
      utf8Bytes: new TextEncoder().encode(text).length,
      utf16CodeUnits: text.length,
      graphemeClusters: segmenter ? [...segmenter.segment(text)].length : null,
    };
    for (const [metric, value] of Object.entries(actual)) {
      if (value !== null && value !== fixture.expected[metric]) {
        throw new Error(`${name}: ${metric}: expected ${fixture.expected[metric]}, got ${value}; compare runtime Unicode/ICU versions before changing expectations`);
      }
    }
    return { id: name, actual, status: segmenter ? 'passed' : 'partial_no_segmenter' };
  });
  return {
    status: segmenter ? 'passed' : 'partial_no_segmenter',
    fixturesChecked: checks.length,
    runtime: {
      node: process.versions.node,
      v8: process.versions.v8,
      unicode: process.versions.unicode ?? null,
      icu: process.versions.icu ?? null,
      cldr: process.versions.cldr ?? null,
      segmenter: segmenter?.resolvedOptions() ?? null,
    },
    referenceRuntime: data.referenceRuntime.javascript,
    graphemes: { status: segmenter ? 'checked_against_reference' : 'not_measured' },
    checks,
  };
}

async function main() {
  if (process.argv.length > 3) throw new Error('usage: node verify.mjs [fixtures.json]');
  const path = process.argv[2] ? resolve(process.argv[2]) : fileURLToPath(new URL('./fixtures.json', import.meta.url));
  const result = verify(JSON.parse(await readFile(path, 'utf8')));
  console.log(JSON.stringify(result, null, 2));
  if (result.status !== 'passed') process.exitCode = 2;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch(error => {
    console.error(JSON.stringify({ status: 'failed', error: error.message, runtime: { node: process.versions.node, unicode: process.versions.unicode ?? null, icu: process.versions.icu ?? null } }));
    process.exitCode = 1;
  });
}
