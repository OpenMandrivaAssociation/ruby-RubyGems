%define rname RubyGems
%define	oname	rubygems
%define	name	ruby-%{rname}

%define	version	0.9.0
%define	release	%mkrel 2

Summary:	Ruby package manager
Name:		%name
Version:	%version
Release:	%release
License:	GPL
Group:		Development/Other
URL: 		http://docs.rubygems.org/
Source0:	%{oname}-%{version}.tar.bz2
Patch0:		rubygems-0.8.11-post.patch
Patch1:		rubygems-0.9.0-gemsdir.patch
BuildArch:	noarch
BuildRequires:	ruby-devel
Requires:	ruby
Provides:	%{oname}
BuildRoot:	%{_tmppath}/%{name}-buildroot

%define	ruby_archdir	%(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"]')
%define	ruby_libdir	%(ruby -rrbconfig -e 'puts Config::CONFIG["sitelibdir"]')
%define	ruby_gemdir	%{_libdir}/ruby/gems/%(ruby -r rbconfig -e 'print Config::CONFIG["ruby_version"]')

%description
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%prep
%setup -q -n rubygems-%{version}
%patch0 -p1
%patch1 -p1 -b .gemsdir
ruby setup.rb config
ruby setup.rb setup

%install
rm -rf %buildroot
mkdir -p %buildroot%{ruby_gemdir}
ruby setup.rb install --prefix=%buildroot
DESTDIR=%buildroot ruby manual-post.rb

for f in `find %buildroot%{ruby_libdir} -name \*.rb`
do
	if head -n1 "$f" | grep '^#!' >/dev/null;
	then
		sed -i 's|/usr/local/bin|/usr/bin|' "$f"
		chmod 0755 "$f"
	else
		chmod 0644 "$f"
	fi
done


%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%doc README*
%attr(755,root,root) %{_bindir}/*
%{ruby_libdir}/*
%{ruby_gemdir}

