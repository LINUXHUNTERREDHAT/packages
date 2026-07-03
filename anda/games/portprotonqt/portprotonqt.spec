%global debug_package %{nil}
%global pypi_name portprotonqt
%global pypi_version 1.2.0
%global oname PortProtonQt
%global _python_no_extras_requires 1

Name:           %{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        GUI for managing and launching games from PortProton and Steam
License:        MIT
URL:            https://git.linux-gaming.ru/Linux-Gaming/PortProtonQt
Source0:        %{url}/archive/v%{version}.tar.gz
ExclusiveArch:  x86_64

BuildRequires:  meson >= 0.61.2
BuildRequires:  ninja-build
BuildRequires:  python3-devel
BuildRequires:  git
BuildRequires:  gettext
BuildRequires:  systemd-rpm-macros
BuildRequires:  vulkan-loader-devel
BuildRequires:  gcc
BuildRequires:  fdupes
BuildRequires:  desktop-file-utils

Obsoletes:      python3-%{pypi_name} < %{version}-%{release}
Provides:       python3-%{pypi_name} = %{version}-%{release}

Requires:       python3-babel
Requires:       python3-evdev
Requires:       python3-websocket-client
Requires:       python3-orjson
Requires:       python3-psutil
Requires:       python3-pyside6
Requires:       python3-pygame
Requires:       python3-requests
Requires:       python3-tqdm
Requires:       python3-vdf
Requires:       python3-pefile
Requires:       python3-pillow
Requires:       python3-pillow-qt
Requires:       python3-rapidfuzz
Requires:       python3-libarchive-c
Requires:       perl-Image-ExifTool
Requires:       SDL3
Requires:       qt6-qtsvg
Requires:       qt6-qtimageformats
Requires:       cabextract
Requires:       gzip
Requires:       unzip
Requires:       curl
Requires:       jq
Requires:       file
Requires:       findutils
Requires:       gawk
Requires:       grep
Requires:       tar
Requires:       xz
Requires:       zstd
Requires:       unrar
Requires:       glx-utils
Requires:       pciutils
Requires:       vulkan-loader
Requires:       procps-ng
Requires:       psmisc
Requires:       7zip
Requires:       python3-dbus-fast

# System Tab
Recommends:     NetworkManager
Recommends:     bluez
Recommends:     upower
Recommends:     pulseaudio-utils
Recommends:     python3-qrcode

# For legacy PortProton prefix backup support
Recommends:     squashfs-tools

%description
A GUI for managing and launching games from PortProton and Steam.
Combines libraries in one place and simplifies running Windows games on Linux.

%package completions
Summary:        Shell completions for %{oname}
Group:          System/Management
BuildArch:      noarch
Requires:       %{name} = %{version}
Supplements:    (%{name} and bash-completion)
Supplements:    (%{name} and zsh)
Supplements:    (%{name} and fish)

%description completions
Shell auto-completion scripts for %{oname} (bash, zsh and fish).

%{?python_disable_dependency_generator}

%prep
%autosetup -n %{pypi_name}

%build
%meson \
    -Dpython_purelibdir=%{python3_sitelib} \
    -Dudev_rulesdir=%{_udevrulesdir}
%meson_build

%install
%meson_install
bash ./dev-scripts/generate-completions.sh
install -Dpm 0644 ./completions/portprotonqt -t %{buildroot}%{bash_completions_dir}
install -Dpm 0644 ./completions/portprotonqt.fish -t %{buildroot}%{fish_completions_dir}
install -Dpm 0644 ./completions/_portprotonqt -t %{buildroot}%{zsh_completions_dir}

chmod -x %{buildroot}%{_datadir}/portproton/conf/*.conf
chmod -x %{buildroot}%{_datadir}/portproton/scripts/thanks

find %{buildroot}%{_datadir}/portproton/scripts -type f -exec sed -i 's|#!/usr/bin/env bash|#!/usr/bin/bash|g' {} +
find %{buildroot}%{_datadir}/portproton/scripts -type f -exec sed -i 's|#!/usr/bin/env sh|#!/usr/bin/sh|g' {} +
find %{buildroot} -type f -name "vk_gpu_info" -exec strip --strip-unneeded {} +

sed -i '1{/^#!/d}' %{buildroot}%{python3_sitelib}/portprotonqt/scripts_utils/easyterm.py
sed -i 's|#!/usr/bin/env python3|#!/usr/bin/python3|g' %{buildroot}%{_bindir}/portprotonqt
sed -i 's|Categories=Game;Utility;|Categories=Game;Amusement;|g' %{buildroot}%{_datadir}/applications/ru.linux_gaming.PortProtonQt.desktop

%fdupes %{buildroot}%{python3_sitelib}
%fdupes %{buildroot}%{_datadir}

%find_lang %{pypi_name}
%desktop_file_validate %{buildroot}%{_datadir}/applications/ru.linux_gaming.PortProtonQt.desktop

%check
%meson_test

%files -f %{pypi_name}.lang
%doc README.md
%license LICENSE
%dir %{_datadir}/portproton
%{_datadir}/portproton/*
%{_bindir}/%{pypi_name}
%{_bindir}/vk_gpu_info
%{python3_sitelib}/%{pypi_name}
%{_scalableiconsdir}/ru.linux_gaming.PortProtonQt.svg
%{_metainfodir}/ru.linux_gaming.PortProtonQt.metainfo.xml
%{_udevrulesdir}/60-portprotonqt.rules
%{_datadir}/polkit-1/rules.d/ru.linux_gaming.PortProtonQt.rules
%{_appsdir}/ru.linux_gaming.PortProtonQt.desktop
%{_datadir}/mime/packages/ru.linux_gaming.PortProtonQt.xml


%files completions
%{bash_completions_dir}/portprotonqt
%{fish_completions_dir}/portprotonqt.fish
%{zsh_completions_dir}/_portprotonqt

%changelog
* Fri Jul 03 2026 Stas <soyu7658@gmail.com> - 1.2.0-1
- Initial package


