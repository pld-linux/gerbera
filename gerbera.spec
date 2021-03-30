Summary:	UPnP Media Server
Name:		gerbera
Version:	1.7.0
Release:	1
License:	GPL v2
Group:		Applications
Source0:	https://github.com/gerbera/gerbera/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	254f734208a112bc46a7263406488e95
URL:		https://gerbera.io
BuildRequires:	cmake >= 3.13
BuildRequires:	curl-devel
BuildRequires:	exiv2-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	ffmpegthumbnailer-devel
BuildRequires:	libexif-devel
BuildRequires:	libfmt-devel >= 5.3
BuildRequires:	libmagic-devel
BuildRequires:	libmatroska-devel
BuildRequires:	libstdc++-devel >= 6:7.1
BuildRequires:	libupnp-devel >= 1.12.1
BuildRequires:	libuuid-devel
BuildRequires:	pugixml-devel
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	spdlog-devel
BuildRequires:	sqlite3-devel
BuildRequires:	systemd-devel
BuildRequires:	taglib-devel
BuildRequires:	zlib-devel
Requires:	libfmt >= 5.3
Requires:	libupnp >= 1.12.1
Requires:	systemd-units >= 38
Provides:	group(gerbera)
Provides:	user(gerbera)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gerbera is a UPnP media server which allows you to stream your digital
media through your home network and consume it on a variety of UPnP
compatible devices.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	-DWITH_AVCODEC=1 \
	-DWITH_DEBUG=0 \
	-DWITH_EXIV2=1 \
	-DWITH_FFMPEGTHUMBNAILER=1 \
	-DWITH_JS=0

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/gerbera,/var/lib/gerbera}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 338 gerbera
%useradd -u 338 -r -d /var/lib/gerbera -s /bin/false -c "Gerbera user" -g gerbera gerbera

%post
%systemd_post gerbera.service

%preun
if [ "$1" = "0" ]; then
	%service gerbera stop
fi
%systemd_preun gerbera.service

%postun
if [ "$1" = "0" ]; then
	%userremove gerbera
	%groupremove gerbera
fi
%systemd_reload

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog.md CONTRIBUTING.md README.md
%attr(755,root,root) %{_bindir}/gerbera
%dir %attr(750,gerbera,gerbera) %{_sysconfdir}/gerbera
%{_datadir}/gerbera
%{_mandir}/man1/gerbera.1*
%{systemdunitdir}/gerbera.service
%dir %attr(770,gerbera,gerbera) /var/lib/gerbera
