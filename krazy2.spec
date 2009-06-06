%define svn  974530

Name:           krazy2
Version:        0.0
Summary:        Code scanner
Release:        %mkrel 0.%svn.1
License:        GPL
Group:          Graphical desktop/KDE
URL:            %name-%version.%svn
Source0:        %name-%version.%svn.tar.bz2
Patch0:         krazy2-fix-install.patch
BuildRoot:      %_tmppath/%name-%version-%release-buildroot
BuildRequires:  qt4-devel
BuildRequires:  kde4-macros
BuildRequires:  perl(HTML::Parser)
BuildRequires:  perl(Tie::IxHash)

%description
Krazy scans KDE source code looking for issues that should be fixed
for reasons of policy, good coding practice, optimization, or any other
good reason.  In typical use, Krazy simply counts up the issues
and provides the line numbers where those issues occurred in each
file processed.  With the verbose option, the offending content will
be printed as well.

Krazy uses "sanity checker programs" which are small plugin programs
to do the real work of the scanning.  It is easy to write your own plugins
and tell Krazy how to use them.


%files
%defattr(-,root,root)
%_kde_bindir/krazy2
%_kde_bindir/krazy2all
%_kde_bindir/krazy2ebn
%_kde_bindir/krazy2xml
%perl_sitelib/Krazy
%_kde_mandir/man1/krazy2.1.*
%_kde_mandir/man1/krazy2all.1.*
%_kde_mandir/man1/krazy2ebn.1.*
%_kde_mandir/man1/krazy2xml.1.*

#-----------------------------------------------------------------------------

%prep
%setup -q -n %name
%patch0 -p0

%build

perl Makefile.PL INSTALLSITEBIN=%_kde_bindir INSTALLSITESCRIPT=%_kde_bindir INSTALLSITEMAN1DIR=%_kde_mandir/man1

%make


%install
rm -rf %buildroot
%makeinstall_std
%clean
rm -rf %{buildroot}

