%define rname	RubyGems
%define	oname	rubygems

Summary:	Ruby package manager
Name:		ruby-%{rname}
Version:	1.7.2
Release:	%mkrel 2
License:	GPL
Group:		Development/Ruby
URL: 		http://docs.rubygems.org/
Source0:	http://rubyforge.org/frs/download.php/60718/%{oname}-%{version}.tgz
BuildArch:	noarch
BuildRequires:	ruby-devel
Requires:	ruby
Provides:	%{oname} = %{version}
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%prep
%setup -q -n rubygems-%{version}

# gems are installed in /usr/lib even on x86_64 
%__sed -ie "s,ConfigMap\[:libdir\],\'/usr/lib\'," lib/rubygems/defaults.rb

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

