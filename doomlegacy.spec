#
# Conditional build:
%bcond_with		x11	# build with System Media Interface (broken, seems unsupported)
%bcond_without	sdl	# build with SDL System Media Interface

%define		rel	2
%define		svnrev	817
Summary:	DOOM Legacy for Linux
Summary(pl.UTF-8):	DOOM Legacy dla Linuksa
Name:		doomlegacy
Version:	1.44
Release:	0.alpha2.r%{svnrev}.%{rel}
License:	GPL, perhaps except for legacy.wad
Group:		Applications/Games
#Source0:	http://doomlegacy.sourceforge.net/releases/%{name}_144_alpha2_src_r777.zip
# no upstream source, so create our own
# svn co https://doomlegacy.svn.sourceforge.net/svnroot/doomlegacy/legacy_one/trunk legacy_one
# rm -rf doomlegacy_144_alpha2 && svn export legacy_one doomlegacy_144_alpha2
# zip -r doomlegacy_144_alpha2_src_r$(svnversion legacy_one).zip doomlegacy_144_alpha2
Source0:	%{name}_144_alpha2_src_r817.zip
# Source0-md5:	28b564983eec5106f6cc3b39bd793dca
# legacy wad extracted from binary archive: doomlegacy_144_alpha2_linux2.4_32bit.zip
Source1:	http://carme.pld-linux.org/~glen/legacy.wad
# Source1-md5:	2c29a4d7cedcf95d09dec71c41025aa5
Source4:	%{name}-x11.desktop
Source5:	%{name}-sdl.desktop
Source6:	%{name}.png
Patch0:		%{name}-paths.patch
Patch1:		%{name}-Makefile.patch
Patch2:		%{name}-nosndstat.patch
Patch3:		%{name}-sound.patch
Patch4:		svnversion.patch
URL:		http://doomlegacy.sourceforge.net/
BuildRequires:	OpenGL-GLU-devel
%{?with_sdl:BuildRequires:	SDL_mixer-devel}
BuildRequires:	nasm
BuildRequires:	rpmbuild(macros) >= 1.595
BuildRequires:	unzip
BuildRequires:	xorg-lib-libXext-devel
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debugcflags		-O1 -g
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
Requires:	%{name}-common = %{version}-%{release}
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
Requires:	%{name}-common = %{version}-%{release}

%description sdl
This is DOOM Legacy for Linux - SDL version.

%description sdl -l pl.UTF-8
To jest DOOM Legacy dla Linuksa - wersja SDL.

%prep
%setup -qc
mv doomlegacy_144_alpha2 src
cd src
%patch0 -p1
%patch1 -p2
%patch2 -p1
%patch3 -p1
cd -
%patch4 -p1
echo %{svnrev} > src/svnrev.txt

%build
install -d objs bin src/linux_x/{mus,snd}serv/linux
cd src

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

%if %{with sdl}
%{__make} -j1 \
	SMIF=SDL \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"
%endif

%if %{with x11}
%{__make} clean
%{__make} \
	SMIF=LINUX_X11 \
	CC="%{__cc}" \
	LDFLAGS="%{rpmldflags}" \
	OPTFLAGS="%{rpmcflags} %{!?debug:-fomit-frame-pointer}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/doomlegacy,%{_datadir}/doomlegacy} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}

install -p bin/llsndserv $RPM_BUILD_ROOT%{_libdir}/doomlegacy
install -p bin/musserver $RPM_BUILD_ROOT%{_libdir}/doomlegacy

%if %{with x11}
install -p bin/llxdoom	$RPM_BUILD_ROOT%{_bindir}
install -p bin/r_opengl.so	$RPM_BUILD_ROOT%{_libdir}/doomlegacy
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}
%endif
%if %{with sdl}
install -p bin/doomlegacy $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}
%endif

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/doomlegacy/legacy.wad
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
%{_pixmapsdir}/*.png

%if %{with x11}
%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/llxdoom
%attr(755,root,root) %{_libdir}/doomlegacy/r_opengl.so
%{_desktopdir}/*x11.desktop
%endif

%if %{with sdl}
%files sdl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/doomlegacy
%{_desktopdir}/*sdl.desktop
%endif
