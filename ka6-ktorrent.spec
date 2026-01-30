#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	webengine	# build without webengine
%define		kdeappsver	25.12.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		ktorrent
%ifarch x32 i686
%undefine	with_webengine
%endif
Summary:	Native KDE BitTorrent client
Summary(de.UTF-8):	Ein nativer KDE BitTorrent Klient
Summary(pl.UTF-8):	Natywny klient BitTorrenta dla KDE
Name:		ka6-%{kaname}
Version:	25.12.1
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	685e0fa1d625a785b592f686255985d7
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Network >= %{qtver}
BuildRequires:	Qt6Positioning-devel >= %{qtver}
BuildRequires:	Qt6PrintSupport-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
%{?with_webengine:BuildRequires:	Qt6WebChannel-devel >= %{qtver}}
%{?with_webengine:BuildRequires:	Qt6WebEngine-devel >= %{qtver}}
BuildRequires:	Qt6Widgets-devel
BuildRequires:	boost-devel
BuildRequires:	gettext-devel
BuildRequires:	ka6-libktorrent-devel >= 21.04.1
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-karchive-devel >= %{kframever}
BuildRequires:	kf6-kauth-devel >= %{kframever}
BuildRequires:	kf6-kcmutils-devel >= %{kframever}
BuildRequires:	kf6-kcodecs-devel >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdnssd-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kitemviews-devel >= %{kframever}
BuildRequires:	kf6-kjobwidgets-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-knotifyconfig-devel >= %{kframever}
BuildRequires:	kf6-kparts-devel >= %{kframever}
BuildRequires:	kf6-kplotting-devel >= %{kframever}
BuildRequires:	kf6-kservice-devel >= %{kframever}
BuildRequires:	kf6-ktextwidgets-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	kf6-solid-devel >= %{kframever}
BuildRequires:	kf6-sonnet-devel >= %{kframever}
BuildRequires:	kf6-syndication-devel >= %{kframever}
BuildRequires:	kp6-plasma-workspace-devel
BuildRequires:	phonon-qt6-devel
BuildRequires:	pkgconfig
BuildRequires:	taglib-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
BuildRequires:	zlib-devel
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KTorrent is a BitTorrent program for KDE.

Its main features are:
- Downloads torrent files
- Upload speed capping, seeing that most people can't upload infinite
  amounts of data.
- Internet searching using various search engines, you can even add
  your own.
- UDP Trackers

%description -l de.UTF-8
KTorrent ist ein BitTorrent Klient für KDE.

Hauptfunktionen sind:
- Torrent-Dateien Download
- Begränzung des Uploades, so dass Mehrheit der Leute nicht unerlaubt
  unbegränzte Datenflüsse sendet
- Durchsuchung des Internets mit hilfe diverser Browser, man kann
  sogar den eigenen Browser dazu schreiben
- UDP Trackers

%description -l pl.UTF-8
KTorrent to klient BitTorrenta dla KDE.

Główne cechy to:
- ściąganie plików torrent
- ograniczanie szybkości uploadu, baczące żeby większość ludzi nie
  przesyłała nieograniczonej ilości danych
- przeszukiwanie Internetu przy użyciu różnych wyszukiwarek, można
  nawet dodać własną
- trackery UDP

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ktmagnetdownloader
%attr(755,root,root) %{_bindir}/ktorrent
%attr(755,root,root) %{_bindir}/ktupnptest
%ghost %{_libdir}/libktcore.so.16
%{_libdir}/libktcore.so.*.*.*
%if %{with webengine}
%{_iconsdir}/hicolor/16x16/actions/kt-add-feeds.png
%{_iconsdir}/hicolor/16x16/actions/kt-add-filters.png
%{_iconsdir}/hicolor/16x16/actions/kt-remove-feeds.png
%{_iconsdir}/hicolor/16x16/actions/kt-remove-filters.png
%{_iconsdir}/hicolor/22x22/actions/kt-add-feeds.png
%{_iconsdir}/hicolor/22x22/actions/kt-add-filters.png
%{_iconsdir}/hicolor/22x22/actions/kt-remove-feeds.png
%{_iconsdir}/hicolor/22x22/actions/kt-remove-filters.png
%{_iconsdir}/hicolor/32x32/actions/kt-add-feeds.png
%{_iconsdir}/hicolor/32x32/actions/kt-add-filters.png
%{_iconsdir}/hicolor/32x32/actions/kt-remove-feeds.png
%{_iconsdir}/hicolor/32x32/actions/kt-remove-filters.png
%endif
%{_desktopdir}/org.kde.ktorrent.desktop
%{_iconsdir}/hicolor/128x128/apps/ktorrent.png
%{_iconsdir}/hicolor/16x16/actions/kt-stop-all.png
%{_iconsdir}/hicolor/16x16/actions/kt-stop.png
%{_iconsdir}/hicolor/16x16/actions/kt-upnp.png
%{_iconsdir}/hicolor/16x16/apps/ktorrent.png
%{_iconsdir}/hicolor/22x22/actions/kt-magnet.png
%{_iconsdir}/hicolor/22x22/actions/kt-pause.png
%{_iconsdir}/hicolor/22x22/actions/kt-remove.png
%{_iconsdir}/hicolor/22x22/actions/kt-set-max-download-speed.png
%{_iconsdir}/hicolor/22x22/actions/kt-set-max-upload-speed.png
%{_iconsdir}/hicolor/22x22/actions/kt-speed-limits.png
%{_iconsdir}/hicolor/22x22/actions/kt-start-all.png
%{_iconsdir}/hicolor/22x22/actions/kt-start.png
%{_iconsdir}/hicolor/22x22/actions/kt-stop-all.png
%{_iconsdir}/hicolor/22x22/actions/kt-stop.png
%{_iconsdir}/hicolor/22x22/apps/ktorrent.png
%{_iconsdir}/hicolor/32x32/actions/kt-info-widget.png
%{_iconsdir}/hicolor/32x32/actions/kt-magnet.png
%{_iconsdir}/hicolor/32x32/actions/kt-pause.png
%{_iconsdir}/hicolor/32x32/actions/kt-queue-manager.png
%{_iconsdir}/hicolor/32x32/actions/kt-remove.png
%{_iconsdir}/hicolor/32x32/actions/kt-set-max-download-speed.png
%{_iconsdir}/hicolor/32x32/actions/kt-set-max-upload-speed.png
%{_iconsdir}/hicolor/32x32/actions/kt-speed-limits.png
%{_iconsdir}/hicolor/32x32/actions/kt-start-all.png
%{_iconsdir}/hicolor/32x32/actions/kt-start.png
%{_iconsdir}/hicolor/32x32/actions/kt-stop-all.png
%{_iconsdir}/hicolor/32x32/actions/kt-stop.png
%{_iconsdir}/hicolor/32x32/actions/kt-upnp.png
%{_iconsdir}/hicolor/32x32/apps/ktorrent.png
%{_iconsdir}/hicolor/48x48/actions/kt-bandwidth-scheduler.png
%{_iconsdir}/hicolor/48x48/actions/kt-change-tracker.png
%{_iconsdir}/hicolor/48x48/actions/kt-check-data.png
%{_iconsdir}/hicolor/48x48/actions/kt-chunks.png
%{_iconsdir}/hicolor/48x48/actions/kt-info-widget.png
%{_iconsdir}/hicolor/48x48/actions/kt-magnet.png
%{_iconsdir}/hicolor/48x48/actions/kt-pause.png
%{_iconsdir}/hicolor/48x48/actions/kt-plugins.png
%{_iconsdir}/hicolor/48x48/actions/kt-queue-manager.png
%{_iconsdir}/hicolor/48x48/actions/kt-remove.png
%{_iconsdir}/hicolor/48x48/actions/kt-restore-defaults.png
%{_iconsdir}/hicolor/48x48/actions/kt-set-max-download-speed.png
%{_iconsdir}/hicolor/48x48/actions/kt-set-max-upload-speed.png
%{_iconsdir}/hicolor/48x48/actions/kt-show-hide.png
%{_iconsdir}/hicolor/48x48/actions/kt-show-statusbar.png
%{_iconsdir}/hicolor/48x48/actions/kt-speed-limits.png
%{_iconsdir}/hicolor/48x48/actions/kt-start-all.png
%{_iconsdir}/hicolor/48x48/actions/kt-start.png
%{_iconsdir}/hicolor/48x48/actions/kt-stop-all.png
%{_iconsdir}/hicolor/48x48/actions/kt-stop.png
%{_iconsdir}/hicolor/48x48/actions/kt-upnp.png
%{_iconsdir}/hicolor/48x48/apps/ktorrent.png
%{_iconsdir}/hicolor/64x64/actions/kt-magnet.png
%{_iconsdir}/hicolor/64x64/apps/ktorrent.png
%{_iconsdir}/hicolor/scalable/actions/kt-magnet.svgz
%{_iconsdir}/hicolor/scalable/actions/kt-set-max-download-speed.svgz
%{_iconsdir}/hicolor/scalable/actions/kt-set-max-upload-speed.svgz
%{_iconsdir}/hicolor/scalable/actions/kt-speed-limits.svgz
%{_datadir}/knotifications6/ktorrent.notifyrc
%{?with_webengine:%{_datadir}/ktorrent}
%{_datadir}/kxmlgui5/ktorrent
%{_datadir}/metainfo/org.kde.ktorrent.appdata.xml
%dir %{_libdir}/qt6/plugins/ktorrent_plugins
%{_libdir}/qt6/plugins/ktorrent_plugins/BandwidthSchedulerPlugin.so
%{_libdir}/qt6/plugins/ktorrent_plugins/DownloadOrderPlugin.so
%{_libdir}/qt6/plugins/ktorrent_plugins/IPFilterPlugin.so
%{_libdir}/qt6/plugins/ktorrent_plugins/InfoWidgetPlugin.so
%{_libdir}/qt6/plugins/ktorrent_plugins/LogViewerPlugin.so
%{_libdir}/qt6/plugins/ktorrent_plugins/MagnetGeneratorPlugin.so
%{_libdir}/qt6/plugins/ktorrent_plugins/MediaPlayerPlugin.so
%{_libdir}/qt6/plugins/ktorrent_plugins/ScanFolderPlugin.so
%{_libdir}/qt6/plugins/ktorrent_plugins/ScanForLostFilesPlugin.so
%{_libdir}/qt6/plugins/ktorrent_plugins/ShutdownPlugin.so
%{_libdir}/qt6/plugins/ktorrent_plugins/StatsPlugin.so
%{_libdir}/qt6/plugins/ktorrent_plugins/UPnPPlugin.so
%{_libdir}/qt6/plugins/ktorrent_plugins/ZeroconfPlugin.so
%if %{with webengine}
%{_libdir}/qt6/plugins/ktorrent_plugins/SearchPlugin.so
%{_libdir}/qt6/plugins/ktorrent_plugins/SyndicationPlugin.so
%endif
