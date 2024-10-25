%global appname Quotient
%define major 0
%define oldlibname %mklibname %{appname} 0
%define libname %mklibname %{appname}
%define develname %mklibname -d %{appname}
%define libqt6name %mklibname %{appname}Qt6
%define develqt6name %mklibname -d %{appname}Qt6
#define git 20221202

Name:		libquotient
Version:	0.9.0
Release:	%{?git:0.%{git}.}1
Group:		System/Libraries
License:	LGPLv2+
URL:		https://github.com/quotient-im/libQuotient
Summary:	Qt5/Qt6 library to write cross-platform clients for Matrix
Source0:	https://github.com/quotient-im/libQuotient/archive/%{?git:master}%{!?git:%{version}}/lib%{appname}-%{?git:%{git}}%{!?git:%{version}}.tar.gz
BuildRequires:	cmake(Olm)
BuildRequires:	cmake(QtOlm)
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	cmake(Qt5Network)
BuildRequires:	cmake(Qt5Multimedia)
BuildRequires:	cmake(Qt5Concurrent)
BuildRequires:	cmake(Qt5LinguistTools)
BuildRequires:	cmake(Qt5Sql)
BuildRequires:	cmake(Qt5Test)
BuildRequires:	cmake(Qt5Keychain)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	qmake5
BuildRequires:	ninja
BuildRequires:	cmake
# qt6
BuildRequires:  cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Keychain)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Multimedia)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6Sql)
BuildRequires:	cmake(Qt6Test)

%description
The Quotient project aims to produce a Qt5-based SDK to develop applications
for Matrix. libQuotient is a library that enables client applications. It is
the backbone of Quaternion, Spectral and other projects. Versions 0.5.x and
older use the previous name - libQMatrixClient.

%package -n %{libname}
Summary:	Library for the Quotient project aims to produce a Qt5-based SDK to develop applications.
Group:		System/Libraries
%rename	%{_lib}quotient0
%rename %{oldlibname}

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

#-----------------------------------------------
%package -n %{libqt6name}
Summary:	Library for the Quotient project aims to produce a Qt6-based SDK to develop applications.
Group:		System/Libraries
%rename	%{_lib}quotient-qt6

%description -n %{libqt6name}
Library for the Quotient project aims to produce a Qt6-based SDK to develop applications
for Matrix. libQuotient is a library that enables client applications.

%package -n %{develqt6name}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libqt6name} = %{EVRD}
# The dependency generator detects cmake(OpenSSL),
# but that's provided by cmake rather than OpenSSL.
# So we need to help it out a little...
Requires:	pkgconfig(openssl)
%rename	%{_lib}quotient-qt6-devel

%description -n %{develqt6name}
This is development files for Quotient. This project aims to produce a Qt5-based SDK to develop applications
for Matrix. libQuotient is a library that enables client applications. It is
the backbone of Quaternion, Spectral and other projects. Versions 0.5.x and
older use the previous name - libQMatrixClient.

%prep
%autosetup -n libQuotient-%{version}
rm -rf 3rdparty

%build
# As of libquotient 0.7 and Clang 16, crashing during compilation.
export CC=gcc
export CXX=g++
export CMAKE_BUILD_DIR=build-qt5
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DQuotient_INSTALL_TESTS:BOOL=OFF \
    -DQuotient_INSTALL_EXAMPLE:BOOL=OFF \
    -DQuotient_ENABLE_E2EE:BOOL=ON \
    -DCMAKE_INSTALL_INCLUDEDIR:PATH="include/%{appname}"

cd ..
export CMAKE_BUILD_DIR=build-qt6
%cmake \
    -G Ninja \
    -DBUILD_WITH_QT6:BOOL=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DQuotient_INSTALL_TESTS:BOOL=OFF \
    -DQuotient_INSTALL_EXAMPLE:BOOL=OFF \
    -DQuotient_ENABLE_E2EE:BOOL=ON \
    -DCMAKE_INSTALL_INCLUDEDIR:PATH="include/%{appname}"
cd ..

%ninja_build -C build-qt5

%ninja_build -C build-qt6

%install
%ninja_install -C build-qt5
rm -rf %{buildroot}%{_datadir}/ndk-modules

%ninja_install -C build-qt6
rm -rf %{buildroot}%{_datadir}/ndk-modules

%files -n %{libname}
%license COPYING
%doc README.md CONTRIBUTING.md SECURITY.md
%{_libdir}/lib*%{appname}.so.%{major}*

%files -n %{develname}
%{_includedir}/%{appname}
%{_libdir}/cmake/%{appname}
%{_libdir}/pkgconfig/%{appname}.pc
#{_libdir}/lib*%{appname}.so

#-------------------------------
%files -n %{libqt6name}
%{_libdir}/libQuotientQt6.so.%{major}*

%files -n %{develqt6name}
%{_libdir}/libQuotientQt6.so
%{_libdir}/pkgconfig/QuotientQt6.pc
%{_libdir}/cmake/QuotientQt6/
