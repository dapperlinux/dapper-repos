# dapper-repos

##About
The Dapper Repos package contains the repository information for the Dapper Linux distribution. It contains Fedora repository information, Dapper Linux COPR information, along with all necessary GPG keys. Note rpmfusion information is not provided here, and should always be fetched from upstream.


##Building
To build this package, first install an RPM development chain:

```bash
$ sudo dnf install fedora-packager fedora-review

```

Next, setup rpmbuild directories with

```bash
$ rpmdev-setuptree
```
And place the file dapper-repos.spec in the SPECS directory, and rename the dapper-repos directory to dapper-repos-25 and compress it:
```bash
$ mv dapper-repos.spec ~/rpmbuild/SPECS/
$ mv dapper-repos dapper-repos-25
$ tar -czvf dapper-repos-25.tar.gz dapper-repos-25
$ mv dapper-repos-25.tar.gz ~/rpmbuild/SOURCES/
```

and finally, you can build RPMs and SRPMs with:
```bash
$ cd ~/rpmbuild/SPECS
$ rpmbuild -ba dapper-repos.spec
```


