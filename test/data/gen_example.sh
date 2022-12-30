#!/usr/bin/env bash
#
# Script to generate the example IPS repository for our tests.

set -xe

mkdir pkg.root
mkdir -p pkg.root/usr/bin

cat > pkg.root/usr/bin/foo << EOF
#!/bin/sh
echo foo
EOF
chmod a+x pkg.root/usr/bin/foo

cat > pkg.root/LICENSE << EOF
Example license text
EOF

pkgsend generate pkg.root | grep -v '^dir ' > pkg.p5m.1

cat >> pkg.p5m.1 << EOF
set name=pkg.fmri value=pkg:/system/file-system/example@1.0,5.11-0.1.0
set name=pkg.summary value="Example package"
license LICENSE license="Example license"
<transform file path=LICENSE -> drop>
EOF

pkgmogrify pkg.p5m.1 > pkg.p5m.2

pkgrepo create pkg.repo
pkgrepo -s pkg.repo set publisher/prefix=example.com
pkgrepo -s pkg.repo set repository/description=Example

pkgsend -s pkg.repo publish -d pkg.root pkg.p5m.2

rm -rf pkg.root pkg.p5m.?

echo
echo "Generated repo in pkg.repo/"
