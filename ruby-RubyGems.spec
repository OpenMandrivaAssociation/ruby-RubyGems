%define rname	RubyGems
%define	oname	rubygems

Summary:	Ruby package manager
Name:		ruby-%{rname}
Version:	1.8.15
Release:	1
License:	GPL
Group:		Development/Ruby
URL:		http://docs.rubygems.org/
Source0:	http://rubyforge.org/frs/download.php/60718/%{oname}-%{version}.tgz
BuildArch:	noarch
BuildRequires:	ruby
Requires:	ruby
Provides:	%{oname} = %{version}
Patch0:		rubygems-1.7.2-fix-gemspec-with-Z-dateformat.patch
Patch1:		rubygems-1.7.2-read-gemspec-with-Z-dateformat.patch


%description
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%prep
%setup -q -n rubygems-%{version}

%patch0 -p1 -b .fixZ
%patch1 -p1 -b .readZ

# gems are installed in /usr/lib even on x86_64 
%__sed -ie "s,ConfigMap\[:libdir\],\'/usr/lib\'," lib/rubygems/defaults.rb

%build

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

%files
%doc README*
%attr(755,root,root) %{_bindir}/*
%{ruby_sitelibdir}/*
%{ruby_gemdir}
