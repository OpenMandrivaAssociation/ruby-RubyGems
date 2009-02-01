%define rname RubyGems
%define	oname	rubygems
%define	name	ruby-%{rname}

%define	version	1.3.1
%define	release	%mkrel 1

Summary:	Ruby package manager
Name:		%name
Version:	%version
Release:	%release
License:	GPL
Group:		Development/Ruby
URL: 		http://docs.rubygems.org/
Source0:	%{oname}-%{version}.tgz
BuildArch:	noarch
BuildRequires:	ruby-devel
Requires:	ruby
Provides:	%{oname}
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%prep
%setup -q -n rubygems-%{version}

%install
rm -rf %buildroot
mkdir -p %buildroot%{ruby_gemdir}
ruby setup.rb --prefix=%buildroot/%_prefix
mkdir -p %buildroot%{ruby_sitelibdir}
mv %buildroot/%_prefix/lib/{*.rb,rubygems,rbconfig} %buildroot%{ruby_sitelibdir}

for f in `find %buildroot%{ruby_sitelibdir} -name \*.rb`
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
%{ruby_sitelibdir}/*
%{ruby_gemdir}

