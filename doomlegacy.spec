Summary:	DOOM Legacy for Linux X-Windows and Mesa
Name:		doomlegacy
Version:	1.32
Release:	1.beta1
Source0:	http://prdownloads.sourceforge.net/doomlegacy/legacy_132beta1_src.tar.gz
Source1:	http://prdownloads.sourceforge.net/doomlegacy/doom3_wad_132.zip
Patch0:		%{name}-paths.patch
Patch1:		%{name}-Makefile.patch
License:	GPL, perhaps except for doom3.wad
Group:		Amusements/Games
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix /usr/X11R6

%description
This is Doom Legacy for Linux X11 and Mesa.

%prep
%setup -q -n doomlegacy -a 1
%patch0 -p1
%patch1 -p1

%build
install -d {,linux_x/{musserv,sndesrv}/}{objs,bin}
%{__make} PGCC=1 LINUX=1 OPTFLAGS="%{!?debug:%{rpmcflags}} %{?debug:-O1 -g}"

%install
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/doom,%{_datadir}/games/doom}

install ../bin/llxdoom			$RPM_BUILD_ROOT%{_bindir}
install linux_x/sndserv/linux/llsndserv $RPM_BUILD_ROOT%{_bindir}
install linux_x/musserv/linux/musserver $RPM_BUILD_ROOT%{_bindir}
install ../bin/r_opengl.so		$RPM_BUILD_ROOT%{_libdir}/doom

install doom3.wad			$RPM_BUILD_ROOT%{_datadir}/games/doom

gzip -9nf _doc/*.txt

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(644,root,root,755)
%doc _doc/*.txt.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*
%{_datadir}/games/doom/doom3.wad
