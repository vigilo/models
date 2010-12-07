%define module  models
%define name    vigilo-%{module}
%define version 2.0.0
%define release 1%{?svn}%{?dist}

Name:       %{name}
Summary:    Vigilo data models (ORM)
Version:    %{version}
Release:    %{release}
Source0:    %{name}-%{version}.tar.gz
URL:        http://www.projet-vigilo.org
Group:      System/Servers
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-build
License:    GPLv2

BuildRequires:   python-setuptools
BuildRequires:   python-babel
BuildRequires:   epydoc

Requires:   python >= 2.5
Requires:   python-babel >= 0.9.4
Requires:   python-setuptools
Requires:   python-psycopg2
Requires:   python-sqlalchemy
Requires:   python-zope.sqlalchemy >= 0.4
Requires:   python-pastescript >= 1.7
Requires:   vigilo-common
Requires:   python-transaction
######### Dependance from python dependance tree #########
Requires:   vigilo-models
Requires:   vigilo-common
Requires:   python-transaction
Requires:   python-pastescript
Requires:   python-setuptools
Requires:   python-zope.sqlalchemy
Requires:   python-sqlalchemy
Requires:   python-psycopg2
Requires:   python-babel
Requires:   python-zope-interface 
Requires:   python-configobj
Requires:   python-pastedeploy
Requires:   python-paste

Buildarch:  noarch


%description
This library gives an API to the Vigilo data models.
This library is part of the Vigilo Project <http://vigilo-project.org>

%prep
%setup -q

%build
make PYTHON=%{_bindir}/python
make apidoc EPYDOC=%{_bindir}/epydoc

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
%defattr(644,root,root,755)
%doc COPYING README.txt doc/*
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %{_sysconfdir}/vigilo
%{python_sitelib}/*


%changelog
* Mon Feb 08 2010 Aurelien Bompard <aurelien.bompard@c-s.fr> - 1.0-1
- initial package
