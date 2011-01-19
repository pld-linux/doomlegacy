Summary:	DOOM Legacy for Linux
Summary(pl.UTF-8):	DOOM Legacy dla Linuksa
Name:		doomlegacy
Version:	1.42
Release:	2
License:	GPL, perhaps except for doom3.wad
Group:		Applications/Games
Source0:	http://dl.sourceforge.net/doomlegacy/legacy_142_src.tar.gz
# Source0-md5:	e1cc5039872dc70e506cd427a9015080
Source1:	http://downloads.sourceforge.net/doomlegacy/doom3_wad_132.zip
# Source1-md5:	3d737bb577bc4295af68d54988191344
Source2:	http://ep09.pld-linux.org/~havner/legacy.dat
# Source2-md5:	df5cac5c3d37849ceb432cbff4df2415
Source4:	%{name}-x11.desktop
Source5:	%{name}-sdl.desktop
Source6:	%{name}.png
Patch0:		%{name}-paths.patch
Patch1:		%{name}-Makefile.patch
Patch2:		%{name}-nosndstat.patch
Patch3:		%{name}-sound.patch
Patch4:		%{name}-errno.patch
Patch5:		%{name}-nocmap.patch
Patch6:		%{name}-vidmodes.patch
Patch7:		%{name}-c.patch
URL:		http://doomlegacy.sourceforge.net/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	nasm
BuildRequires:	rpmbuild(macros) >= 1.595
BuildRequires:	unzip
BuildRequires:	xorg-lib-libXext-devel
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debugcflags	-O1 -g
%define		_noautoreqdep	libGL.so.1 libGLU.so.1

%description
DOOM Legacy for Linux.

%description -l pl.UTF-8
DOOM Legacy dla Linuksa.

%package common
Summary:	DOOM Legacy for Linux - common files
Summary(pl.UTF-8):	DOOM Legacy dla Linuksa - pliki wspólne
Group:		X11/Applications/Games

%description common
Common files for both versions of DOOM Legacy.

%description common -l pl.UTF-8
Pliki wspólne dla obu wersji DOOM Legacy.

%package X11
Summary:	DOOM Legacy for Linux - X Window and OpenGL version
Summary(pl.UTF-8):	DOOM Legacy dla Linuksa - wersja korzystająca z X Window i OpenGL
Group:		X11/Applications/Games
Obsoletes:	doomlegacy-x11

%description X11
This is DOOM Legacy for Linux - X11 and OpenGL version.

%description X11 -l pl.UTF-8
To jest DOOM Legacy dla Linuksa - wersja korzystająca z X Window i
OpenGL.

%package sdl
Summary:	DOOM Legacy for Linux - SDL version
Summary(pl.UTF-8):	DOOM Legacy dla Linuksa - wersja korzystająca z SDL
Group:		X11/Applications/Games

%description sdl
This is DOOM Legacy for Linux - SDL version.

%description sdl -l pl.UTF-8
To jest DOOM Legacy dla Linuksa - wersja SDL.

%prep
%setup -qc -a1
mv doomlegacy_142_src src
cd src
%patch0 -p1
%patch1 -p2
%patch2 -p1
%patch3 -p1
%patch4 -p2
%patch5 -p2
%patch6 -p2
%patch7 -p2

%build
install -d objs bin
cd src

# linux_x contains some precompiled binary objects (incompatible with glibc 2.3) - kill them
%{__make} clean \
	LINUX=1

# build musserv/sndserv first. with our flags
%{__make} -C linux_x/musserv -f Makefile.linux \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"
	LDFLAGS="%{rpmldflags}"
install -p linux_x/musserv/linux/musserver ../bin

%{__make} -C linux_x/sndserv \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"
	LDFLAGS="%{rpmldflags}"
install -p linux_x/sndserv/linux/llsndserv ../bin

# build llxdoom
%{__make} \
	PGCC=1 \
	LINUX=1 \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"

%{__make} clean \
	LINUX=1

# build lsdldoom
%{__make} \
	PGCC=1 \
	LINUX=1 \
	SDL=1 \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/doomlegacy,%{_datadir}/doomlegacy} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}

install -p bin/llxdoom	$RPM_BUILD_ROOT%{_bindir}
install -p bin/lsdldoom	$RPM_BUILD_ROOT%{_bindir}
install -p bin/llsndserv $RPM_BUILD_ROOT%{_libdir}/doomlegacy
install -p bin/musserver $RPM_BUILD_ROOT%{_libdir}/doomlegacy
install -p bin/r_opengl.so	$RPM_BUILD_ROOT%{_libdir}/doomlegacy

cp -p doom3.wad	$RPM_BUILD_ROOT%{_datadir}/doomlegacy
cp -p %{SOURCE2}	$RPM_BUILD_ROOT%{_datadir}/doomlegacy

cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE6} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post common
%banner -o -e %{name}-common <<'EOF'
To run doomlegacy you need some WAD file: either freedoom package
or some shareware or commercial WAD from Doom or Heretic:
Doom.wad, Doom1.wad, Doom2.wad, Tnt.wad, Plutonia.wad,
Heretic.wad or Heretic1.wad .
EOF

%files common
%defattr(644,root,root,755)
%doc src/_doc/*.txt
%dir %{_libdir}/doomlegacy
%attr(755,root,root) %{_libdir}/doomlegacy/*serv*
%{_datadir}/doomlegacy
%{_pixmapsdir}/*

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/llxdoom
%attr(755,root,root) %{_libdir}/doomlegacy/r_opengl.so
%{_desktopdir}/*x11.desktop

%files sdl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lsdldoom
%{_desktopdir}/*sdl.desktop
