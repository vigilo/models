%define module  @SHORT_NAME@

Name:       vigilo-%{module}
Summary:    @SUMMARY@
Version:    @VERSION@
Release:    1%{?svn}%{?dist}
Source0:    %{name}-%{version}.tar.gz
URL:        @URL@
Group:      System/Servers
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-build
License:    GPLv2
Buildarch:  noarch

BuildRequires:   python-setuptools
BuildRequires:   python-babel

Requires:   python >= 2.5
Requires:   vigilo-common
Requires:   python-transaction
Requires:   python-pastescript >= 1.7
Requires:   python-setuptools
Requires:   python-zope.sqlalchemy >= 0.4
Requires:   python-sqlalchemy >= 0.5
Requires:   python-sqlalchemy < 0.6
Requires:   python-psycopg2
Requires:   python-babel >= 0.9.4
Requires:   python-zope-interface
Requires:   python-configobj
Requires:   python-pastedeploy
Requires:   python-paste
Requires:   python-networkx


%description
@DESCRIPTION@
This library is part of the Vigilo Project <http://vigilo-project.org>

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
make install_pkg \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	SYSCONFDIR=%{_sysconfdir} \
	PYTHON=%{__python}

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc COPYING.txt README.txt doc/*
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %{_sysconfdir}/vigilo
%{python_sitelib}/*


%changelog
* Mon Feb 08 2010 Aurelien Bompard <aurelien.bompard@c-s.fr> - 1.0-1
- initial package
