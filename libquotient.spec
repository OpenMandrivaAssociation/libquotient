%define major 0
%define libpackage %mklibname quotient %{major}
%define devpackage %mklibname -d quotient

%global appname Quotient
%global libname lib%{appname}

Name: libquotient
Version: 0.6.2
Release: 1

License: LGPLv2+
URL: https://github.com/quotient-im/libQuotient
Summary: Qt5 library to write cross-platform clients for Matrix
Source0: https://github.com/quotient-im/libQuotient/archive/%{version}/%{libname}-%{version}.tar.gz

BuildRequires: cmake(Olm)
BuildRequires: cmake(QtOlm)
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5Multimedia)
BuildRequires: cmake(Qt5Concurrent)
BuildRequires: cmake(Qt5LinguistTools)
BuildRequires: cmake(Qt5Test)
BuildRequires: qmake5
BuildRequires: ninja
BuildRequires: cmake

%description
The Quotient project aims to produce a Qt5-based SDK to develop applications
for Matrix. libQuotient is a library that enables client applications. It is
the backbone of Quaternion, Spectral and other projects. Versions 0.5.x and
older use the previous name - libQMatrixClient.

%package -n %{libpackage}
Group:		System/Libraries
Summary:	Library for the Quotient project aims to produce a Qt5-based SDK to develop applications.

%description -n %{libpackage}
Library for the Quotient project aims to produce a Qt5-based SDK to develop applications
for Matrix. libQuotient is a library that enables client applications.

%package -n %{devpackage}
Summary: Development files for %{name}
Requires:	%{libpackage} = %{EVRD}


%description -n %{devpackage}
This is development files for Quotient. This project aims to produce a Qt5-based SDK to develop applications
for Matrix. libQuotient is a library that enables client applications. It is
the backbone of Quaternion, Spectral and other projects. Versions 0.5.x and
older use the previous name - libQMatrixClient.

%prep
%autosetup -n %{libname}-%{version}
rm -rf 3rdparty

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DQuotient_INSTALL_TESTS:BOOL=OFF \
    -DQuotient_INSTALL_EXAMPLE:BOOL=OFF \
    -DQuotient_ENABLE_E2EE:BOOL=ON \
    -DCMAKE_INSTALL_INCLUDEDIR:PATH="include/%{appname}"
%ninja_build

%install
%ninja_install -C build
rm -rf %{buildroot}%{_datadir}/ndk-modules

%files -n %{libpackage}
%license COPYING
%doc README.md CONTRIBUTING.md SECURITY.md
%{_libdir}/%{libname}.so.%{major}*

%files -n %{devpackage}
%{_includedir}/%{appname}/
%{_libdir}/cmake/%{appname}/
%{_libdir}/pkgconfig/%{appname}.pc
%{_libdir}/%{libname}.so
