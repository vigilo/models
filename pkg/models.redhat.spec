%define module  @SHORT_NAME@

Name:       vigilo-%{module}
Summary:    @SUMMARY@
Version:    @VERSION@
Release:    @RELEASE@%{?dist}
Source0:    %{name}-%{version}.tar.gz
URL:        @URL@
Group:      Applications/System
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-build
License:    GPLv2
Buildarch:  noarch

BuildRequires:   python-distribute
BuildRequires:   python-babel

Requires:   python-babel >= 0.9.4
Requires:   python-distribute
Requires:   python-psycopg2
Requires:   python-sqlalchemy >= 0.7.8
Requires:   python-sqlalchemy < 0.8
Requires:   python-zope-sqlalchemy >= 0.4
# On contraint la version à cause d'incompatibilités
# constatées avec la version 0.7.6 apportée par RHEL 7.
Requires:   python-zope-sqlalchemy < 0.5
Requires:   python-paste-deploy
Requires:   vigilo-common
Requires:   python-transaction
Requires:   python-networkx
Requires:   python-passlib


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
%{_sysconfdir}/vigilo
%{_sysconfdir}/vigilo/%{module}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/vigilo/%{module}/settings.ini
%{python_sitelib}/*


%changelog
* Fri Jan 21 2011 Vincent Quéméner <vincent.quemener@c-s.fr>
- Rebuild for RHEL6.

* Mon Feb 08 2010 Aurelien Bompard <aurelien.bompard@c-s.fr>
- initial package
