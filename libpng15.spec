%define libname_orig libpng
%define major 15
%define libname	%mklibname png %{major}
%define develname %mklibname png %{major} -d
%define staticname %mklibname png %{major} -d -s

%bcond_without	uclibc

Summary:	A library of functions for manipulating PNG image format files
Name:		libpng_%{major}
Version:	1.5.2
Release:	%mkrel 1
License:	zlib
Group:		System/Libraries
URL:		https://www.libpng.org/pub/png/libpng.html
Source:		http://prdownloads.sourceforge.net/libpng/%{libname_orig}-%{version}.tar.xz
# (tpg) APNG support http://littlesvr.ca/apng/
# (tpg) http://hp.vector.co.jp/authors/VA013651/freeSoftware/apng.html
# (tpg) http://sourceforge.net/projects/libpng-apng/ <- use this one
Patch0:		libpng-1.5.2-apng.patch
BuildRequires: 	zlib-devel
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.30.3
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG is
a bit-mapped graphics format similar to the GIF format.  PNG was created to
replace the GIF format, since GIF uses a patented data compression
algorithm.

Libpng should be installed if you need to manipulate PNG format image
files.

%package -n	%{libname}
Summary:	A library of functions for manipulating PNG image format files
Group:		System/Libraries
#Provides:	%{libname_orig} = 2:%{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with libpng.

%package -n	%{develname}
Summary:	Development tools for programs to manipulate PNG image format files
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Requires:	zlib-devel
#Provides:	%{libname_orig}-devel = 2:%{version}-%{release}
#Provides:	png-devel = 2:%{version}-%{release}
# remove this if 1.5.2 will become the system lib
Provides:	png15-devel = %{version}-%{release}
Conflicts:	png-devel <= 2:1.2.44

%description -n	%{develname}
The libpng-devel package contains the header files and libraries
necessary for developing programs using the PNG (Portable Network
Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install the
libpng package.

%package -n	%{staticname}
Summary:	Development static libraries
Group:		Development/C
Requires:	%{develname} >= %{version}-%{release}
Requires:	zlib-devel
#Provides:	%{libname_orig}-static-devel = 2:%{version}-%{release}
#Provides:	png-static-devel = 2:%{version}-%{release}
# remove this if 1.5.2 will become the system lib
Provides:	png15-static-devel = %{version}-%{release}
Conflicts:	png-static-devel <= 2:1.2.44

%description -n	%{staticname}
Libpng development static libraries.

%package -n	%{libname_orig}-source
Summary:	Source code of %{libname_orig}
Group:		Development/C
# remove this if 1.5.2 will become the system lib
Conflicts:	%{libname_orig}-source <= 2:1.2.44

%description -n	%{libname_orig}-source
This package contains the source code of %{libname_orig}.

%prep

%setup -q -n %{libname_orig}-%{version}
%patch0 -p1 -b .apng
./autogen.sh

%build
export CONFIGURE_TOP=`pwd`
%if %{with uclibc}
mkdir -p uclibc
cd uclibc
%configure2_5x	CC="%{uclibc_cc}" \
		CFLAGS="%{uclibc_cflags}" \
		--enable-shared=no \
		--enable-static=yes \
		--with-pic
%make
cd ..
%endif

mkdir -p shared
cd shared
CFLAGS="%{optflags} -O3 -funroll-loops" \
%configure2_5x	--with-pic
%make
cd ..

# barfs at symbols mismatch, the apng symbols needs to be added in scripts/symbols.def
#%%check
#make -C shared check

%install
rm -rf %{buildroot}
%makeinstall_std -C shared
%if %{with uclibc}
install -m644 uclibc/.libs/libpng15.a -D %{buildroot}%{uclibc_root}%{_libdir}/libpng15.a
ln -s libpng15.a %{buildroot}%{uclibc_root}%{_libdir}/libpng.a
%endif

install -d %{buildroot}%{_mandir}/man{3,5}
install -m0644 {libpng,libpngpf}.3 %{buildroot}%{_mandir}/man3
install -m0644 png.5 %{buildroot}%{_mandir}/man5/png3.5

install -d %{buildroot}%{_prefix}/src/%{libname_orig}
cp -a *.c *.h %{buildroot}%{_prefix}/src/%{libname_orig}

# remove unpackaged files
rm -rf %{buildroot}{%{_prefix}/man,%{_libdir}/lib*.la}

#multiarch
%multiarch_binaries %{buildroot}%{_bindir}/libpng15-config

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*
%{_libdir}/libpng15.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc *.txt example.c README TODO CHANGES
%{_bindir}/libpng-config
%{_bindir}/libpng15-config
%multiarch %{multiarch_bindir}/libpng15-config
%{_includedir}/*
%{_libdir}/libpng15.so
%{_libdir}/libpng.so
%{_libdir}/pkgconfig/*
%{_mandir}/man?/*

%files -n %{staticname}
%defattr(-,root,root)
%{_libdir}/libpng*.a
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libpng*.a
%endif

%files -n %{libname_orig}-source
%defattr(-,root,root)
%{_prefix}/src/%{libname_orig}

