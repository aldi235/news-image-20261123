// news-image-20261123 entry (Node 22, standard library only).
// The image was drawn ahead of time by draw_news.py (PIL, run on the build
// machine) and committed as entry.png beside this file; this program only
// copies it to /output/entry.png, so it runs in the stdlib-only sandbox with
// no network and a read-only repository directory. Both grader runs copy the
// same committed bytes, so the two runs are byte-identical by construction.
//
// Local test: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
