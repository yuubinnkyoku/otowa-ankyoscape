#!/usr/bin/env python3
# 第313回: README.mdの「- **第312回:**」行の直後に .313-bullet.txt の1行を挿入する。
# 冪等: READMEに既に「第313回:」の行がある場合は挿入しない。
# アンカー不在の場合は非ゼロ終了（失敗を可視化し、クリーンアップは行わない）。
import io, sys

README = 'README.md'
BULLET = '.313-bullet.txt'

t = io.open(README, encoding='utf-8').read()
for line in t.split('\n'):
    if line.startswith('- **第313回:'):
        print('README already has round-313 bullet; skip insertion')
        sys.exit(0)
if not any(l.startswith('- **第312回:') for l in t.split('\n')):
    sys.exit('anchor line "- **第312回:**" not found; abort')

b = io.open(BULLET, encoding='utf-8').read().rstrip('\n').rstrip('\r')
lines = t.split('\n')
for i, l in enumerate(lines):
    if l.startswith('- **第312回:'):
        lines.insert(i + 1, b)
        break
io.open(README, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('inserted round-313 bullet after round-312 line')
