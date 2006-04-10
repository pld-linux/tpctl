Summary:	IBM ThinkPad configuration tools
Name:		tpctl
Version:	4.17
Release:	1
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/tpctl/%{name}_%{version}.tar.gz
# Source0-md5:	00d163c09b290b4cdc7488144f3f7faa
Source1:	%{name}.apmiser.init
Patch0:		%{name}-rpm.patch
Patch1:		%{name}-optflags.patch
URL:		http://tpctl.sourceforge.net/
BuildRequires:	ncurses-ext-devel
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
tpctl is a package of IBM ThinkPad configuration tools for Linux.

%package -n apmiser
Summary:	IBM ThinkPad APM settings daemon
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}

%description -n apmiser
apmiser is a tool for IBM ThinkPads that automatically controls the
APM power settings based on your usage patterns.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
cp -p tpctlir/README README.tpctlir

%build
%{__make} all \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I/usr/include/ncurses"
%{__make} -C tpctlir \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I/usr/include/ncurses"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man8,%{_initrddir}}
%{__make} install \
	DEST=$RPM_BUILD_ROOT \
	PATH_BIN=%{_bindir}/ \
	PATH_LIB=%{_libdir}/ \
	PATH_MAN=%{_mandir}/ \
	PATH_SBIN=%{_sbindir}/

install %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/apmiser
install man/apmiser.8 tpctlir/tpctlir.8 $RPM_BUILD_ROOT%{_mandir}/man8


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post -n apmiser
[ $1 -eq 1 ] && chkconfig --add apmiser || :

%preun -n apmiser
if [ $1 -eq 0 ] ; then
  chkconfig --del apmiser
  %{_initrddir}/apmiser stop >/dev/null 2>&1 || :
fi

%postun -n apmiser
[ $1 -gt 0 ] && %{_initrddir}/apmiser try-restart >/dev/null || :


%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING README* SUPPORTED* TROUBLE* VGA-MODES
%attr(755,root,root) %{_bindir}/*tpctl
%attr(755,root,root) %{_sbindir}/tpctlir
%attr(755,root,root) %{_libdir}/libsmapidev.so.*
%{_mandir}/man1/*tpctl.1*
%{_mandir}/man8/tpctlir.8*

%files -n apmiser
%defattr(644,root,root,755)
%doc apmiser/README
%attr(755,root,root) %config %{_initrddir}/*
%attr(755,root,root) %{_sbindir}/apmiser
%{_mandir}/man8/apmiser.8*
