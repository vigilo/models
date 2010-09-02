%define module  models
%define name    vigilo-%{module}
%define version 2.0.0
%define release 1%{?svn}%{?dist}

%define pyver 26
%define pybasever 2.6
%define __python /usr/bin/python%{pybasever}
%define __os_install_post %{__python26_os_install_post}
%{!?python26_sitelib: %define python26_sitelib %(python26 -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:       %{name}
Summary:    Vigilo data models (ORM)
Version:    %{version}
Release:    %{release}
Source0:    %{module}.tar.bz2
URL:        http://www.projet-vigilo.org
Group:      System/Servers
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-build
License:    GPLv2

BuildRequires:   python26-distribute
BuildRequires:   python26-babel

Requires:   python >= 2.5
Requires:   python26-babel >= 0.9.4
Requires:   python26-distribute
Requires:   python26-psycopg2
Requires:   python26-sqlalchemy
Requires:   python26-zope.sqlalchemy >= 0.4
Requires:   python26-pastescript >= 1.7
Requires:   vigilo-common
Requires:   python26-transaction
######### Dependance from python dependance tree #########
Requires:   vigilo-models
Requires:   vigilo-common
Requires:   python26-transaction
Requires:   python26-pastescript
Requires:   python26-distribute
Requires:   python26-zope.sqlalchemy
Requires:   python26-sqlalchemy
Requires:   python26-psycopg2
Requires:   python26-babel
Requires:   python26-zope-interface 
Requires:   python26-configobj
Requires:   python26-pastedeploy
Requires:   python26-paste

Buildarch:  noarch


%description
This library gives an API to the Vigilo data models.
This library is part of the Vigilo Project <http://vigilo-project.org>

%prep
%setup -q -n %{module}

%build
make PYTHON=%{__python}

%install
rm -rf $RPM_BUILD_ROOT
make install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	SYSCONFDIR=%{_sysconfdir} \
	PYTHON=%{__python}

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
