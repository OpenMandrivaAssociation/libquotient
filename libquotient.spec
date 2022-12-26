%bcond_without qt5
%bcond_without qt6

%global appname Quotient
%define major 0
%define libname %mklibname %{appname} %{major}
%define develname %mklibname -d %{appname}

# With stable release 0.7.0 please don't go with git again (as long as it is not very necessary), just switch to stable release.
#define git 20221202

Name:		libquotient
Version:	0.7.0
Release:	%{?git:0.%{git}.}1
Group:		System/Libraries
License:	LGPLv2+
URL:		https://github.com/quotient-im/libQuotient
Summary:	Qt5 library to write cross-platform clients for Matrix
Source0:	https://github.com/quotient-im/libQuotient/archive/%{?git:master}%{!?git:%{version}}/lib%{appname}-%{?git:%{git}}%{!?git:%{version}}.tar.gz
BuildRequires:	cmake(Olm)
BuildRequires:	cmake(QtOlm)
%if %{with qt5}
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	cmake(Qt5Network)
BuildRequires:	cmake(Qt5Multimedia)
BuildRequires:	cmake(Qt5Concurrent)
BuildRequires:	cmake(Qt5LinguistTools)
BuildRequires:	cmake(Qt5Sql)
BuildRequires:	cmake(Qt5Test)
BuildRequires:	cmake(Qt5Keychain)
BuildRequires:	qmake5
%endif
BuildRequires:	pkgconfig(openssl)
BuildRequires:	ninja
BuildRequires:	cmake
%if %{with qt6}
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6WebSockets)
BuildRequires: cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Multimedia)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6Sql)
BuildRequires:	cmake(Qt6Test)
BuildRequires: qmake-qt6
BuildRequires: qt6-cmake
%endif


%description
The Quotient project aims to produce a Qt5-based SDK to develop applications
for Matrix. libQuotient is a library that enables client applications. It is
the backbone of Quaternion, Spectral and other projects. Versions 0.5.x and
older use the previous name - libQMatrixClient.

%package -n %{libname}
Summary:	Library for the Quotient project aims to produce a Qt5-based SDK to develop applications.
Group:		System/Libraries
%rename	%{_lib}quotient0

%description -n %{libname}
Library for the Quotient project aims to produce a Qt5-based SDK to develop applications
for Matrix. libQuotient is a library that enables client applications.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
# The dependency generator detects cmake(OpenSSL),
# but that's provided by cmake rather than OpenSSL.
# So we need to help it out a little...
Requires:	pkgconfig(openssl)
%rename	%{_lib}quotient-devel

%description -n %{develname}
This is development files for Quotient. This project aims to produce a Qt5-based SDK to develop applications
for Matrix. libQuotient is a library that enables client applications. It is
the backbone of Quaternion, Spectral and other projects. Versions 0.5.x and
older use the previous name - libQMatrixClient.

%prep
%autosetup -n libQuotient-%{version}
rm -rf 3rdparty

%build
%if %{with qt5}
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DQuotient_INSTALL_TESTS:BOOL=OFF \
    -DQuotient_INSTALL_EXAMPLE:BOOL=OFF \
    -DQuotient_ENABLE_E2EE:BOOL=ON \
    -DCMAKE_INSTALL_INCLUDEDIR:PATH="include/%{appname}"
cd ..
%endif
%if %{with qt6}
CMAKE_BUILD_DIR=build-qt6 %cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DQuotient_INSTALL_TESTS:BOOL=OFF \
    -DQuotient_INSTALL_EXAMPLE:BOOL=OFF \
    -DQuotient_ENABLE_E2EE:BOOL=ON \
    -DCMAKE_INSTALL_INCLUDEDIR:PATH="include/%{appname}" \
    -G Ninja
%endif
%if %{with qt5}
%ninja_build
%endif
%if %{with qt6}
%ninja_build -C build-qt6
%endif

%install
%if %{with qt5}
%ninja_install -C build
rm -rf %{buildroot}%{_datadir}/ndk-modules
%endif
%if %{with qt6}
%ninja_install -C build-qt6
%endif
%files -n %{libname}
%license COPYING
%doc README.md CONTRIBUTING.md SECURITY.md
%{_libdir}/lib*%{appname}.so.%{major}*

%files -n %{develname}
%{_includedir}/%{appname}
%{_libdir}/cmake/%{appname}
%{_libdir}/pkgconfig/%{appname}.pc
%{_libdir}/lib*%{appname}.so
