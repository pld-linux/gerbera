#
# Conditional build:
%bcond_without	js	# JavaScript scripting support

Summary:	UPnP Media Server
Summary(pl.UTF-8):	Serwer mediów UPnP
Name:		gerbera
Version:	2.6.1
Release:	2
License:	GPL v2
Group:		Applications/Multimedia
#Source0Download: https://github.com/gerbera/gerbera/releases
Source0:	https://github.com/gerbera/gerbera/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bc6cf5a7082aac9c8b95c5e363a4e044
URL:		https://gerbera.io/
BuildRequires:	cmake >= 3.19
BuildRequires:	curl-devel
%{?with_js:BuildRequires:	duktape-devel}
BuildRequires:	exiv2-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	ffmpegthumbnailer-devel
BuildRequires:	jsoncpp-devel
BuildRequires:	libexif-devel
BuildRequires:	libfmt-devel >= 7.1.3
BuildRequires:	libicu-devel
BuildRequires:	libmagic-devel
BuildRequires:	libmatroska-devel
BuildRequires:	libstdc++-devel >= 6:7.1
BuildRequires:	libupnp-devel >= 1.14.6
BuildRequires:	libuuid-devel
BuildRequires:	pugixml-devel
BuildRequires:	rpmbuild(macros) >= 1.742
BuildRequires:	spdlog-devel >= 1:1.8.1
BuildRequires:	sqlite3-devel >= 3.7.11
BuildRequires:	systemd-devel
BuildRequires:	taglib-devel >= 1.12
BuildRequires:	wavpack-devel >= 5.1.0
BuildRequires:	zlib-devel
Requires:	libfmt >= 7.1.3
Requires:	libupnp >= 1.14.6
Requires:	spdlog >= 1:1.8.1
Requires:	sqlite3-libs >= 3.7.11
Requires:	systemd-units >= 38
Requires:	taglib >= 1.12
Requires:	wavpack-libs >= 5.1.0
Provides:	group(gerbera)
Provides:	user(gerbera)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gerbera is a UPnP media server which allows you to stream your digital
media through your home network and consume it on a variety of UPnP
compatible devices.

%description -l pl.UTF-8
Gerbera to serwer mediów UPnP, pozwalający na wysyłanie strumieni
mediów cyfrowych poprzez domową sieć i odbieranie ich na różnych
urządzeniach zgodnych z UPnP.

%prep
%setup -q

%build
%cmake -B build \
	-DWITH_AVCODEC:BOOL=ON \
	-DWITH_DEBUG:BOOL=OFF \
	-DWITH_EXIV2:BOOL=ON \
	-DWITH_FFMPEGTHUMBNAILER:BOOL=ON \
	-DWITH_WAVPACK:BOOL=ON \
	%{cmake_on_off js WITH_JS}

%{__make} -C build

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
%{bash_compdir}/gerbera
