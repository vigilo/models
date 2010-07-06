%define module  models
%define name    vigilo-%{module}
%define version 2.0.0
%define release 1%{?svn}

Name:       %{name}
Summary:    Vigilo data models (ORM)
Version:    %{version}
Release:    %{release}
Source0:    %{module}.tar.bz2
URL:        http://www.projet-vigilo.org
Group:      System/Servers
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-build
License:    GPLv2

BuildRequires:   python-setuptools
BuildRequires:   python-babel

Requires:   python >= 2.5
Requires:   python-babel >= 0.9.4
Requires:   python-setuptools
Requires:   python-psycopg2
Requires:   python-sqlalchemy
Requires:   python-zope.sqlalchemy >= 0.4
Requires:   python-pastescript >= 1.7
Requires:   vigilo-common
Requires:   vigilo-transaction
Requires:   vigilo-decorator
Requires:   python-turbojson >= 1.2
Requires:   python-prioritized_methods >= 0.2.1
Requires:   python-formencode >= 1.1
Requires:   python-webflash >= 0.1a7
Requires:   python-peak-rules >= 0.5a1.dev-r2569
Requires:   python-repoze.what-pylons >= 1.0rc3
Requires:   python-weberror >= 0.10.1
Requires:   python-pylons >= 0.9.7
Requires:   python-repoze.who >= 1.0.10
Requires:   python-sqlalchemy-migrate >= 0.5.1
Requires:   python-repoze.what.plugins.sql >= 1.0rc1
Requires:   python-repoze.who.plugins.sa >= 1.0rc1
Requires:   python-repoze.what >= 1.0.3
Requires:   python-extremes >= 1.1 
Requires:   python-addons >= 0.6
Requires:   python-decoratortools >= 1.7dev-r2450
Requires:   python-bytecodeassembler >= 0.3
Requires:   python-pygments
Requires:   python-tempita
Requires:   python-webtest >= 1.1
Requires:   python-mako >= 0.2.4
Requires:   python-nose >= 0.10.4
Requires:   python-webhelpers >= 0.6.4
Requires:   python-repoze.who-testutil >= 1.0b2
Requires:   python-symboltype >= 1.0

Buildarch:  noarch


%description
This library gives an API to the Vigilo data models.
This library is part of the Vigilo Project <http://vigilo-project.org>

%prep
%setup -q -n %{module}

%build
make PYTHON=%{_bindir}/python

%install
rm -rf $RPM_BUILD_ROOT
make install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	SYSCONFDIR=%{_sysconfdir} \
	PYTHON=%{_bindir}/python

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/vigilo
%{python_sitelib}/*


%changelog
* Mon Feb 08 2010 Aurelien Bompard <aurelien.bompard@c-s.fr> - 1.0-1
- initial package
