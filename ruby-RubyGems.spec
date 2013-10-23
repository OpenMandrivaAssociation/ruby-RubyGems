%define rname	RubyGems
%define	oname	rubygems

# The RubyGems library has to stay out of Ruby directory three, since the
# RubyGems should be share by all Ruby implementations.
%define rubygems_dir %{_datadir}/ruby/gems

# Specify custom RubyGems root and other related macros.
%define gem_dir %{_datadir}/ruby/gems
# TODO: These folders should go into rubygem-filesystem but how to achieve it,
# since noarch package cannot provide arch dependent subpackages?
# http://rpm.org/ticket/78
%define gem_extdir %{_exec_prefix}/lib{,64}/gems

%bcond_without	bootstrap

Summary:	Ruby package manager
Name:		ruby-%{rname}
Version:	2.0.10
Release:	1
License:	GPLv2+
Group:		Development/Ruby
URL:		http://docs.rubygems.org/
Source0:	http://production.cf.rubygems.org/rubygems/%{oname}-%{version}.tgz
Source1:	ruby-RubyGems.rpmlintrc
# Sources from the works by Vít Ondruch <vondruch@redhat.com>
Source100:	operating_system.rb
# Add support for installing binary extensions according to FHS.
# https://github.com/rubygems/rubygems/issues/210
# Note that 8th patch might be resolved by
# https://bugs.ruby-lang.org/issues/7897
Patch109: rubygems-2.0.0-binary-extensions.patch
# This slightly changes behavior of "gem install --install-dir" behavior.
# Without this patch, Specifications.dirs is modified and gems installed on
# the system cannot be required anymore. This causes later issues when RDoc
# documentation should be generated, since json gem is sudenly not accessible.
# https://github.com/rubygems/rubygems/pull/452
#Patch113: rubygems-2.0.5-Do-not-modify-global-Specification.dirs-during-install.patch
# This prevents issues, when ruby configuration specifies --with-ruby-version=''.
# https://github.com/rubygems/rubygems/pull/455
#Patch114: rubygems-2.0.5-Fixes-for-empty-ruby-version.patch
# It seems that with rubygem 2.0.5, when building C extension
# results can be nil
Patch115: rubygems-2.0.7-extension-result-nil.patch

BuildArch:	noarch
BuildRequires:	ruby
BuildRequires:	locales-en
# If !%{with bootstrap} installed rubygem may be boostrap and not require it
%if !%{with bootstrap}
BuildRequires:	rubygem(rdoc)
%endif
Requires:	locales
Requires:	ruby
%if !%{with bootstrap}
Requires:	rubygem(rdoc)
%endif
Provides:	%{oname} = %{version}
Provides:	ruby(rubygems) = %{version}-%{release}

%description
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%prep
%setup -q -n rubygems-%{version}
%apply_patches

%install
LANG=en_US.UTF-8 GEM_HOME=%{buildroot}/%{gem_dir} \
    ruby setup.rb --prefix=/\
%if !%{with bootstrap}
        --rdoc --ri \
%else
	--no-document --no-rdoc --no-ri \
%endif
        --destdir=%{buildroot}/%{rubygems_dir}/

mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}/%{rubygems_dir}/bin/gem %{buildroot}/%{_bindir}/gem
rm -rf %{buildroot}/%{rubygems_dir}/bin

mv %{buildroot}/%{rubygems_dir}/lib/* %{buildroot}/%{rubygems_dir}/.
# No longer needed
rmdir %{buildroot}%{rubygems_dir}/lib

# Install custom operating_system.rb.
mkdir -p %{buildroot}%{rubygems_dir}/rubygems/defaults
install -cpm 0644 %{SOURCE100} %{buildroot}%{rubygems_dir}/rubygems/defaults/

# Kill bundled cert.pem
mkdir -p %{buildroot}%{rubygems_dir}/rubygems/ssl_certs/
ln -sf %{_sysconfdir}/pki/tls/cert.pem \
	%{buildroot}%{rubygems_dir}/rubygems/ssl_certs/ca-bundle.pem

# Create gem folders.
mkdir -p %{buildroot}%{gem_dir}/{cache,gems,specifications,doc}
mkdir -p %{buildroot}%{gem_extdir}/exts

# Create macros.rubygems file for rubygems-devel
mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d

cat >> %{buildroot}%{_sysconfdir}/rpm/macros.d/rubygems.macros << \EOF
# The RubyGems root folder.
%%gem_dir %{gem_dir}

# Common gem locations and files.
%%gem_instdir %%{gem_dir}/gems/%%{gem_name}-%%{version}
%%gem_extdir %%{_libdir}/gems/exts/%%{gem_name}-%%{version}
%%gem_libdir %%{gem_instdir}/lib
%%gem_cache %%{gem_dir}/cache/%%{gem_name}-%%{version}.gem
%%gem_spec %%{gem_dir}/specifications/%%{gem_name}-%%{version}.gemspec
%%gem_docdir %%{gem_dir}/doc/%%{gem_name}-%%{version}
EOF

%files
%doc README* 
%doc History.txt
%doc MIT.txt LICENSE.txt
%dir %{gem_dir}
%dir %{gem_dir}/cache
%dir %{gem_dir}/gems
%dir %{gem_dir}/specifications
%doc %{gem_dir}/doc
%{_bindir}/gem

#% dir %{rubygems_dir}/
%{rubygems_dir}/rubygems/
%{rubygems_dir}/rubygems.rb
%{rubygems_dir}/ubygems.rb
%{rubygems_dir}/gauntlet_rubygems.rb

%dir %{_exec_prefix}/lib/gems
%dir %{_exec_prefix}/lib64/gems
%dir %{_exec_prefix}/lib/gems/exts
%dir %{_exec_prefix}/lib64/gems/exts

%{_sysconfdir}/rpm/macros.d/rubygems.macros
