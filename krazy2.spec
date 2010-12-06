%define svn     999498

Name:           krazy2
Version:        2.9
Release:        %mkrel 0.%svn.4
Summary:        Krazy is a tool for checking code against the KDE coding guidelines
Group:          Graphical desktop/KDE
License:        GPLv2+
URL:            http://techbase.kde.org/Development/Tutorials/Code_Checking
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export -r 999498 svn://anonsvn.kde.org/home/kde/trunk/quality/krazy2 krazy2-2.8
#  tar -c krazy2-2.9 | bzip2 --best -c > krazy2-2.9.tar.bz2
Source0:        krazy2-%{version}.%svn.tar.bz2
Source1:        krazy-licensecheck
Patch0:         krazy2-prefix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

# krazy-licensecheck moved from kdesdk to here in 4.2.0
Conflicts:      kdesdk < 4.2.0

BuildRequires:  groff
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTML::Parser)
BuildRequires:  perl(Tie::IxHash)
BuildRequires:  perl(XML::LibXML)
BuildRequires:  perl-doc
BuildRequires:  qt4-devel
BuildRequires:  kdelibs4-devel
BuildRequires:  kdevplatform4-devel
# Krazy2 uses desktop-file-validate, so this is an actual Requires
Requires:       desktop-file-utils
Requires:       kdesdk4-core

%description
Krazy scans KDE source code looking for issues that should be fixed
for reasons of policy, good coding practice, optimization, or any other
good reason.


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_mandir}/man1/krazy2.1.*
%{_mandir}/man1/krazy2all.1.*
%{_mandir}/man1/krazy2ebn.1.*
%{_mandir}/man1/krazy2xml.1.*
%{_mandir}/man5/krazyrc.5.*
#Already in kdesdk4-core
%exclude %{_bindir}/krazy-licensecheck
%{_bindir}/krazy2
%{_bindir}/krazy2all
%{_bindir}/krazy2ebn
%{_bindir}/krazy2xml
%{_libdir}/libcpp_parser.so
%{_libdir}/libcppmodel.so
%{_libdir}/libpreprocessor.so
%{_libdir}/libcheckutil.so
%{_libdir}/libcheckutil.so.1
%{_libdir}/libcheckutil.so.1.0
%{_libdir}/krazy2/
%{_datadir}/dtd/
%{perl_vendorlib}/Krazy/

#--------------------------------------------------------------------

%prep
%setup -q
%patch0


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make
pushd src/passbyvalue
%{qmake_qt4}
make %{?_smp_mflags}
popd
pushd cppchecks
%{cmake}
make VERBOSE=1 %{?_smp_mflags}
popd


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install
chmod 0755 %{buildroot}%{_bindir}/krazy2{,all,ebn}
pushd helpers
make DESTDIR=%{buildroot} PREFIX=%{_prefix} \
    %if "%{_lib}" == "lib64"
        LIBSUFFIX=64 \
    %endif
    install
popd
pushd plugins
make PREFIX=%{buildroot}%{_prefix} \
    %if "%{_lib}" == "lib64"
        LIBSUFFIX=64 \
    %endif
    install
popd
pushd extras
make DESTDIR=%{buildroot} PREFIX=%{_prefix} \
    %if "%{_lib}" == "lib64"
        LIBSUFFIX=64 \
    %endif
    install
popd
pushd src/passbyvalue
make INSTALL_ROOT=%{buildroot}%{_prefix} \
    %if "%{_lib}" == "lib64"
        LIBSUFFIX=64 \
    %endif
    install
popd
pushd share
mkdir -p %{buildroot}%{_datadir}/dtd
install -m 644 -p kpartgui.dtd %{buildroot}%{_datadir}/dtd/kpartgui.dtd
install -m 644 -p kcfg.dtd %{buildroot}%{_datadir}/dtd/kcfg.dtd
popd
pushd doc
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install
popd
install -m 644 %{SOURCE1} %{buildroot}%{_bindir}/krazy-licensecheck
pushd cppchecks/build
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install
popd
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
# chmod -R ug+w %{buildroot}%{_bindir}
# chmod -R ug+w %{buildroot}%{_libdir}


%clean
rm -rf %{buildroot}
