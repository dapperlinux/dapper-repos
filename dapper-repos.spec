Summary:        Dapper Linux package repositories
Name:           dapper-repos
Version:        29
Release:        2
License:        MIT
URL:            https://github.com/dapperlinux/dapper-repos/
Source:         %{name}-%{version}.tar.xz
Provides:       dapper-repos(%{version})
Requires:       system-release(%{version})
Requires:       dapper-gpg-keys = %{version}-%{release}
Obsoletes:      fedora-repos-anaconda
Obsoletes:      fedora-repos-modular
Provides:       fedora-repos-modular = %{version}-%{release} 
Provides:       fedora-repos
Provides:       fedora-repos(%{version})
Obsoletes:      fedora-repos
BuildArch:      noarch

%description
Dapper Linux package repository files for yum and dnf along with gpg public keys

%package rawhide
Summary:        Rawhide repo definitions
Requires:       fedora-repos = %{version}
Obsoletes:      fedora-release-rawhide
Obsoletes:      fedora-repos-rawhide-modular
Provides:       fedora-repos-rawhide-modular = %{version}-%{release} 

%description rawhide
This package provides the rawhide repo definitions.

%package -n dapper-gpg-keys
Summary:        Dapper Linux RPM keys
Provides:		fedora-gpg-keys
Obsoletes:		fedora-gpg-keys
Obsoletes:      fedora-release-rawhide <= 22-0.3

%description -n dapper-gpg-keys
This package provides the RPM signature keys.

%prep
%setup -q

%build

%install
# Install the keys
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Link the primary/secondary keys to arch files, according to archmap.
# Ex: if there's a key named RPM-GPG-KEY-fedora-19-primary, and archmap
#     says "fedora-19-primary: i386 x86_64",
#     RPM-GPG-KEY-fedora-19-{i386,x86_64} will be symlinked to that key.
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
for keyfile in RPM-GPG-KEY*; do
    key=${keyfile#RPM-GPG-KEY-} # e.g. 'fedora-20-primary'
    arches=$(sed -ne "s/^${key}://p" $RPM_BUILD_DIR/%{name}-%{version}/archmap) \
        || echo "WARNING: no archmap entry for $key"
    for arch in $arches; do
        # replace last part with $arch (fedora-20-primary -> fedora-20-$arch)
        ln -s $keyfile ${keyfile%%-*}-$arch # NOTE: RPM replaces %% with %
    done
done
# and add symlink for compat generic location
ln -s RPM-GPG-KEY-fedora-%{version}-primary RPM-GPG-KEY-%{version}-fedora
popd

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in fedora*repo dapper*repo; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

%files
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-modular.repo
%config(noreplace) /etc/yum.repos.d/fedora-cisco-openh264.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates-testing.repo 
%config(noreplace) /etc/yum.repos.d/fedora-modular.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates-modular.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates-testing-modular.repo
%config(noreplace) /etc/yum.repos.d/dapperlinux.repo

%files rawhide
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo
%config(noreplace) /etc/yum.repos.d/fedora-rawhide-modular.repo

%files -n dapper-gpg-keys
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*

%changelog
* Sat Nov  3 2018 Matthew Ruffell <msr50@uclive.ac.nz> - 29-1
- Updating for DL29
- add changes for the new modular setup
- update baseurl paths for updates-testing to new Everything ones
- Move modular repos to a subpackage
- Minor cleanups, drop defattr and Group

* Sun Jun 17 2018 Matthew Ruffell <msr50@uclive.ac.nz> - 28-3
- Adding kernel repo for GCC 7 kernel builds

* Sat May  5 2018 Matthew Ruffell <msr50@uclive.ac.nz> - 28-1
- Updating for DL28

* Fri Nov 17 2017 Matthew Ruffell <msr50@uclive.ac.nz> - 27-2
- Moving to Primary copr as main is now broken.

* Fri Nov 17 2017 Matthew Ruffell <msr50@uclive.ac.nz> - 27-1
- DL27, Removing xpra repo and key, adding F28 keys

* Mon Sep  4 2017 Matthew Ruffell <msr50@uclive.ac.nz> - 26-2
- Disabling xpra beta repo

* Fri Aug 11 2017 Matthew Ruffell <msr50@uclive.ac.nz> - 26-1
- Dapper Linux 26, adding Fedora 26, 27 Keyfiles

* Mon Nov 28 2016 Matthew Ruffell <msr50@uclive.ac.nz> - 25-2
- Enabling Fedora Repos and Turning off Rawhide

* Fri Nov  4 2016 Matthew Ruffell <msr50@uclive.ac.nz> - 25-1
- Updating for F25

* Mon Oct 24 2016 Matthew Ruffell <msr50@uclive.ac.nz> - 24-1
- Added Dapper Linux repo information
