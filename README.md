# RCauth/AARC RPM Packaging
RPM spec files for the RCauth components:

Package | Version | Spec file
--- | --- | ---
aarc-delegation-server | 0.2.8 | `SPECS/aarc-delegation-server.spec`
aarc-master-portal | 0.2.7 | `SPECS/aarc-master-portal.spec`

This repository mirrors the standard `rpmbuild` directory layout, but only the build inputs are tracked in git. WAR/JAR files are downloaded at build time, and all build output are ignored.

## Prerequisites
Tested on EL9 environment (Rocky/Alma/RHEL9).
```
sudo dnf install -y rpmbuild rpmdevtools git
```
Build as a normal user, not root.

## Building
1. Clone the repository

```
git clone <repo-url> rcauth-aarc-rpm
cd rcauth-aarc-rpm
```

2. Create the build directories that `rpmbuild` expects:
```
mkdir -p BUILD BUILDROOT RPMS SOURCES SPECS SRPMS
```

3. Download the source files:
`spectool` read the `SourceN:` URLs in each spec and downloads them into `SOURCES /`:
```
spectool -g -C SOURCES SPECS/aarc-delegation-server.spec
spectool -g -C SOURCES SPECS/aarc-master-portal.spec
```
> If you already jave a file with the same name in `SOURCES/`, `spectool` will skip it. 

> Delete all files in `SOURCES/` first before download after a version bump.

4. Build the RPMs:

`--define "_topdir $PWD"` tells `rpmbuild` to use this repository as its build tree instead of `~/rpmbuild`:
```
rpmbuild -ba --define "_topdir $PWD" SPECS/aarc-delegation-server.spec
rpmbuild -ba --define "_topdir $PWD" SPECS/aarc-master-portal.spec
```
> `-ba` builds both the binary RPM and source RPM. Use `-bb` for the binary RPM only, or `-bs` for the source RPM only.

5. Install the built RPM packages:
> Note: testing both packages on the same environment `aarc-delegation-server` and `aarc-master-portal` conflict with each other and cannot be installed at the same time. Install only one package at a time, and remove it before installing the other:
```
# test delegation server
sudo dnf install ./RPMS/noarch/aarc-delegation-server-0.2.8-*.rpm
# ... test ...
sudo dnf remove aarc-delegation-server

# then test the master portal
sudo dnf install ./RPMS/noarch/aarc-master-portal-0.2.7-*.rpm
# ... test ...
sudo dnf remove aarc-master-portal
```

## Updating to a new upstream version
1. Edit the `Version:` field in the spec (and reset `Realease:` to `1%{?dist}`).
2. Add a `%changelog` entry, e.g. with `rpmdev-bumpspec`.
3. Remove the old downloaded files from `SOURCES` and repeat steps 3-4 in Building section.
4. Commit only the spec to git.