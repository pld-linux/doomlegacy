Summary:	DOOM Legacy for Linux
Summary(pl):	DOOM Legacy dla Linuksa
Name:		doomlegacy
Version:	1.40
Release:	4
License:	GPL, perhaps except for doom3.wad
Group:		Applications/Games
Source0:	http://dl.sourceforge.net/doomlegacy/legacy_140_src.tar.gz
Source1:	http://dl.sourceforge.net/doomlegacy/doom3_wad_132.zip
Source2:	http://dl.sourceforge.net/doomlegacy/legacy_dat.zip
Source3:	%{name}-x11.desktop
Source4:	%{name}-sdl.desktop
Source5:	%{name}.png
Icon:		doomlegacy.xpm
URL:		http://legacy.newdoom.com/
Patch0:		%{name}-paths.patch
Patch1:		%{name}-Makefile.patch
Patch2:		%{name}-nosndstat.patch
Patch3:		%{name}-sound.patch
Patch4:		%{name}-errno.patch
Patch5:		%{name}-nocmap.patch
BuildRequires:	OpenGL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	XFree86-devel
BuildRequires:	nasm
BuildRequires:	unzip
ExclusiveArch:	%{ix86}
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debugcflags	-O1 -g
%define		_noautoreqdep	libGL.so.1 libGLU.so.1

%description
DOOM Legacy for Linux.

%description -l pl
DOOM Legacy dla Linuksa.

%package common
Summary:	DOOM Legacy for Linux - common files
Summary(pl):	DOOM Legacy dla Linuksa - pliki wspólne
Group:		X11/Applications/Games

%description common
Common files for both versions of DOOM Legacy.

%description common -l pl
Pliki wspólne dla obu wersji DOOM Legacy.

%package X11
Summary:	DOOM Legacy for Linux - X Window and OpenGL version
Summary(pl):	DOOM Legacy dla Linuksa - wersja korzystająca z X Window i OpenGL
Group:		X11/Applications/Games
Requires:	OpenGL
Obsoletes:	%{name}-x11

%description X11
This is DOOM Legacy for Linux - X11 and OpenGL version.

%description X11 -l pl
To jest DOOM Legacy dla Linuksa - wersja korzystająca z X Window i
OpenGL.

%package sdl
Summary:	DOOM Legacy for Linux - SDL version
Summary(pl):	DOOM Legacy dla Linuksa - wersja korzystająca z SDL
Group:		X11/Applications/Games
Requires:	OpenGL

%description sdl
This is DOOM Legacy for Linux - SDL version.

%description sdl -l pl
To jest DOOM Legacy dla Linuksa - wersja SDL.

%prep
%setup -q -c -a 1 -a 2
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p1
%patch5 -p1

%build
mkdir bin

# linux_x contains some precompiled binary objects (incompatible with glibc 2.3) - kill them
%{__make} -C doomlegacy_src clean LINUX=1
%{__make} -C doomlegacy_src \
	PGCC=1 LINUX=1 OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"

%{__make} -C doomlegacy_src clean LINUX=1
%{__make} -C doomlegacy_src \
	PGCC=1 LINUX=1 SDL=1 OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/doomlegacy,%{_datadir}/doomlegacy} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_applnkdir}/Games/FPP}

install bin/llxdoom	$RPM_BUILD_ROOT%{_bindir}
install bin/lsdldoom	$RPM_BUILD_ROOT%{_bindir}
install doomlegacy_src/linux_x/sndserv/linux/llsndserv $RPM_BUILD_ROOT%{_libdir}/doomlegacy
install doomlegacy_src/linux_x/musserv/linux/musserver $RPM_BUILD_ROOT%{_libdir}/doomlegacy
install bin/r_opengl.so	$RPM_BUILD_ROOT%{_libdir}/doomlegacy

install doom3.wad	$RPM_BUILD_ROOT%{_datadir}/doomlegacy
install legacy.dat	$RPM_BUILD_ROOT%{_datadir}/doomlegacy

install %{SOURCE3} $RPM_BUILD_ROOT%{_applnkdir}/Games/FPP
install %{SOURCE4} $RPM_BUILD_ROOT%{_applnkdir}/Games/FPP
install %{SOURCE5} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf ${RPM_BUILD_ROOT}

%post common
echo "To run legacy doom You need either Doom.wad, Doom1.wad, Doom2.wad,"
echo "Tnt.wad, Plutonia.wad, Heretic.wad or Heretic1.wad"
echo "from any sharware or commercial version of Doom or Heretic!"

%files common
%defattr(644,root,root,755)
%doc doomlegacy_src/_doc/*.txt
%dir %{_libdir}/doomlegacy
%attr(755,root,root) %{_libdir}/doomlegacy/*serv*
%{_datadir}/doomlegacy
%{_pixmapsdir}/*

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/llxdoom
%attr(755,root,root) %{_libdir}/doomlegacy/r_opengl.so
%{_applnkdir}/Games/FPP/*x11.desktop

%files sdl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lsdldoom
%{_applnkdir}/Games/FPP/*sdl.desktop
