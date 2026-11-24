# insert README bullet after the 第303回 line (第304回)
bullet = open('.304-bullet.txt', encoding='utf-8').read()
bullet = bullet.rstrip('\n') + '\n'
readme = open('README.md', encoding='utf-8').read()
anchor = '\n- **第303回:'
n = readme.count(anchor)
assert n == 1, 'README anchor count=%d' % n
head = bullet.split('\n', 1)[0]
assert head not in readme, 'bullet already present'
i = readme.index(anchor)
end = readme.index('\n', i + 1)
new = readme[:end+1] + bullet + readme[end+1:]
open('README.md', 'w', encoding='utf-8').write(new)
print('bullet inserted')
