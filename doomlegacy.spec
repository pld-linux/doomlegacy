Summary:	DOOM Legacy for Linux
Summary(pl):	DOOM Legacy dla Linuksa
Name:		doomlegacy
Version:	1.32
Release:	1.beta1.1
License:	GPL, perhaps except for doom3.wad
Group:		Applications/Games
Group(cs):	Aplikace/Hry
Group(da):	Programmer/Spil
Group(de):	Applikationen/Spiele
Group(es):	Aplicaciones/Juegos
Group(fr):	Applications/Jeux
Group(is):	Forrit/Leikir
Group(it):	Applicazioni/Giochi
Group(ja):	•¢•◊•Í•±°º•∑•Á•Û/•≤°º•‡
Group(no):	Applikasjoner/Spill
Group(pl):	Aplikacje/Gry
Group(pt):	AplicaÁıes/Jogos
Group(ru):	“…Ãœ÷≈Œ…—/È«“Ÿ
Group(sl):	Programi/Igre
Group(sv):	Till‰mpningar/Spel
Group(uk):	“…ÀÃ¡ƒŒ¶ “œ«“¡Õ…/∂«“…
Source0:	http://prdownloads.sourceforge.net/doomlegacy/legacy_132beta1_src.tar.gz
Source1:	http://prdownloads.sourceforge.net/doomlegacy/doom3_wad_132.zip
Patch0:		%{name}-paths.patch
Patch1:		%{name}-Makefile.patch
Patch2:		%{name}-nosndstat.patch
BuildRequires:	XFree86-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	nasm
BuildRequires:	unzip
ExclusiveArch:	%{ix86}
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		debugcflags	-O1 -g
%define		_noautoreqdep	libGL.so.1 libGLU.so.1

%description
DOOM Legacy for Linux.

%description -l pl
DOOM Legacy dla Linuksa.

%package common
Summary:	DOOM Legacy for Linux - common files
Summary(pl):	DOOM Legacy dla Linuksa - pliki wspÛlne
Group:		X11/Applications/Games
Group(cs):	X11/Aplikace/Hry
Group(da):	X11/Programmer/Spil
Group(de):	X11/Applikationen/Spiele
Group(es):	X11/Aplicaciones/Juegos
Group(fr):	X11/Applications/Jeux
Group(is):	X11/Forrit/Leikir
Group(it):	X11/Applicazioni/Giochi
Group(ja):	X11/•¢•◊•Í•±°º•∑•Á•Û/•≤°º•‡
Group(no):	X11/Applikasjoner/Spill
Group(pl):	X11/Aplikacje/Gry
Group(pt):	X11/AplicaÁıes/Jogos
Group(ru):	X11/“…Ãœ÷≈Œ…—/È«“Ÿ
Group(sl):	X11/Programi/Igre
Group(sv):	X11/Till‰mpningar/Spel
Group(uk):	X11/“…ÀÃ¡ƒŒ¶ “œ«“¡Õ…/∂«“…

%description common
Common files for both versions of DOOM Legacy.

%description common -l pl
Pliki wspÛlne dla obu wersji DOOM Legacy.

%package x11
Summary:	DOOM Legacy for Linux - X Window and OpenGL version
Summary(pl):	DOOM Legacy dla Linuksa - wersja korzystaj±ca z X Window i OpenGL
Group:		X11/Applications/Games
Group(cs):	X11/Aplikace/Hry
Group(da):	X11/Programmer/Spil
Group(de):	X11/Applikationen/Spiele
Group(es):	X11/Aplicaciones/Juegos
Group(fr):	X11/Applications/Jeux
Group(is):	X11/Forrit/Leikir
Group(it):	X11/Applicazioni/Giochi
Group(ja):	X11/•¢•◊•Í•±°º•∑•Á•Û/•≤°º•‡
Group(no):	X11/Applikasjoner/Spill
Group(pl):	X11/Aplikacje/Gry
Group(pt):	X11/AplicaÁıes/Jogos
Group(ru):	X11/“…Ãœ÷≈Œ…—/È«“Ÿ
Group(sl):	X11/Programi/Igre
Group(sv):	X11/Till‰mpningar/Spel
Group(uk):	X11/“…ÀÃ¡ƒŒ¶ “œ«“¡Õ…/∂«“…
Requires:	OpenGL

%description x11
This is DOOM Legacy for Linux - X11 and OpenGL version.

%description x11 -l pl
To jest DOOM Legacy dla Linuksa - wersja korzystaj±ca z X Window i
OpenGL.

%package sdl
Summary:	DOOM Legacy for Linux - SDL version
Summary(pl):	DOOM Legacy dla Linuksa - wersja korzystaj±ca z SDL
Group:		X11/Applications/Games
Group(cs):	X11/Aplikace/Hry
Group(da):	X11/Programmer/Spil
Group(de):	X11/Applikationen/Spiele
Group(es):	X11/Aplicaciones/Juegos
Group(fr):	X11/Applications/Jeux
Group(is):	X11/Forrit/Leikir
Group(it):	X11/Applicazioni/Giochi
Group(ja):	X11/•¢•◊•Í•±°º•∑•Á•Û/•≤°º•‡
Group(no):	X11/Applikasjoner/Spill
Group(pl):	X11/Aplikacje/Gry
Group(pt):	X11/AplicaÁıes/Jogos
Group(ru):	X11/“…Ãœ÷≈Œ…—/È«“Ÿ
Group(sl):	X11/Programi/Igre
Group(sv):	X11/Till‰mpningar/Spel
Group(uk):	X11/“…ÀÃ¡ƒŒ¶ “œ«“¡Õ…/∂«“…
Requires:	OpenGL

%description sdl
This is DOOM Legacy for Linux - SDL version.

%description sdl -l pl
To jest DOOM Legacy dla Linuksa - wersja SDL.

%prep
%setup -q -c -a 1
%patch0 -p1
%patch1 -p0
%patch2 -p1

%build
install -d doomlegacy/linux_x/{musserv,sndserv}/{objs,bin}
%{__make} -C doomlegacy PGCC=1 LINUX=1 OPTFLAGS="%{rpmcflags}"
%{__make} -C doomlegacy clean LINUX=1
%{__make} -C doomlegacy PGCC=1 LINUX=1 SDL=1 OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/doomlegacy,%{_datadir}/doomlegacy}

install bin/llxdoom	$RPM_BUILD_ROOT%{_bindir}
install bin/lsdldoom	$RPM_BUILD_ROOT%{_bindir}
install doomlegacy/linux_x/sndserv/linux/llsndserv $RPM_BUILD_ROOT%{_libdir}/doomlegacy
install doomlegacy/linux_x/musserv/linux/musserver $RPM_BUILD_ROOT%{_libdir}/doomlegacy
install bin/r_opengl.so	$RPM_BUILD_ROOT%{_libdir}/doomlegacy

install doom3.wad	$RPM_BUILD_ROOT%{_datadir}/doomlegacy

gzip -9nf doomlegacy/_doc/*.txt

%clean
rm -rf ${RPM_BUILD_ROOT}

%files common
%defattr(644,root,root,755)
%doc doomlegacy/_doc/*.txt.gz
%dir %{_libdir}/doomlegacy
%attr(755,root,root) %{_libdir}/doomlegacy/*serv*
%{_datadir}/doomlegacy

%files x11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/llxdoom
%attr(755,root,root) %{_libdir}/doomlegacy/r_opengl.so

%files sdl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lsdldoom
