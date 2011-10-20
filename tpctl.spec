Summary:	IBM ThinkPad configuration tools
Summary(pl.UTF-8):	Narzędzia konfiguracyjne dla laptopów IBM ThinkPad
Name:		tpctl
Version:	4.17
Release:	3
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/tpctl/%{name}_%{version}.tar.gz
# Source0-md5:	00d163c09b290b4cdc7488144f3f7faa
Source1:	%{name}.apmiser.init
Source2:	http://tpctl.sourceforge.net/PS2-ref.txt
# Source2-md5:	c10d14fd24df4e5aff33f564daed04c4
Patch0:		%{name}-makefile.patch
URL:		http://tpctl.sourceforge.net/
BuildRequires:	ncurses-ext-devel
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
tpctl is a package of IBM ThinkPad configuration tools for Linux.

%description -l pl.UTF-8
tpctl to pakiet narzędzie konfiguracyjnych dla laptopów IBM ThinkPad
dla Linuksa.

%package -n apmiser
Summary:	IBM ThinkPad APM settings daemon
Summary(pl.UTF-8):	Demon ustawień APM dla laptopów IBM ThinkPad
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}

%description -n apmiser
apmiser is a tool for IBM ThinkPads that automatically controls the
APM power settings based on your usage patterns.

%description -n apmiser -l pl.UTF-8
apmiser to narzędzie dla laptopów IBM ThinkPad automatycznie sterujące
ustawieniami zasilania APM w oparciu o wybrane wzorce wykorzystania.

%prep
%setup -q
%patch0 -p1
cp -p tpctlir/README README.tpctlir
install %{SOURCE2} .

%build
%{__make} all \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I/usr/include/ncurses"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man8,/etc/rc.d/init.d}
%{__make} install \
	DEST=$RPM_BUILD_ROOT \
	PATH_BIN=%{_bindir}/ \
	PATH_LIB=%{_libdir}/ \
	PATH_MAN=%{_mandir}/ \
	PATH_SBIN=%{_sbindir}/

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/apmiser

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%banner -e %{name} << EOF
You need to install kernel-misc-thinkpad for this package to work.
EOF
%postun	-p /sbin/ldconfig

%post -n apmiser
/sbin/chkconfig --add apmiser
#%%service apmiser restart
if [ "$1" != "0" ]; then
	/etc/rc.d/init.d/apmiser try-restart
fi

%preun -n apmiser
if [ "$1" = "0" ] ; then
	%service apmiser stop
	/sbin/chkconfig --del apmiser
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog PS2-ref.txt README* SUPPORTED* TROUBLE* VGA-MODES
%attr(755,root,root) %{_bindir}/*tpctl
%attr(755,root,root) %{_sbindir}/tpctlir
%attr(755,root,root) %{_libdir}/libsmapidev.so.*
%{_mandir}/man1/*tpctl.1*
%{_mandir}/man8/tpctlir.8*

%files -n apmiser
%defattr(644,root,root,755)
%doc apmiser/README
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) %{_sbindir}/apmiser
%{_mandir}/man8/apmiser.8*
