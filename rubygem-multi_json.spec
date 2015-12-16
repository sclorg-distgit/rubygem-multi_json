%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}
# Generated from multi_json-1.0.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name multi_json

Summary: A gem to provide swappable JSON backends
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 1.7.7
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/intridea/multi_json
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygem(json)
# json_pure won't be in the collection
#BuildRequires: %%{?scl_prefix}rubygem(json_pure)
BuildRequires: %{?scl_prefix}rubygem(rspec)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
# OkJson is allowed to be bundled:
# https://fedorahosted.org/fpc/ticket/113
Provides: bundled(%{?scl_prefix}okjson) = 20110719

%description
A gem to provide swappable JSON backends utilizing Yajl::Ruby, the JSON gem,
JSON pure, or a vendored version of okjson.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl:%scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}


%prep
%setup -q -c -T
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
exit 0
pushd ./%{gem_instdir}
# simplecov gem is not available in Fedora so remove its usage
sed -i "/require 'simplecov'/,/end$/{s/^/#/}" spec/helper.rb

# oj is not available on Fedora.
sed -i '148,174 s/^/#/' spec/multi_json_spec.rb
sed -i '/expect(MultiJson.adapter).to eq MultiJson::Adapters::Oj/{s/Oj/JsonGem/}' spec/multi_json_spec.rb
sed -i 's/oj / /' spec/multi_json_spec.rb

# ruby-yajl is not available on Fedora yet.
# https://bugzilla.redhat.com/show_bug.cgi?id=823351
sed -i 's/ yajl//' spec/multi_json_spec.rb

# Prevents "dump encoding" testsuite error.
# https://github.com/intridea/multi_json/issues/126
%{?scl:scl enable %{scl} - << \EOF}
LANG=en_US.utf8 rspec spec
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_instdir}/LICENSE.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec


%changelog
* Fri Mar 21 2014 Vít Ondruch <vondruch@redhat.com> - 1.7.7-2
- Rebuid against new scl-utils to depend on -runtime package.
  Resolves: rhbz#1069109

* Thu Oct 03 2013 Josef Stribny <jstribny@redhat.com> - 1.7.7-2
- Remove requirement on json_pure

* Fri Jun 07 2013 Josef Stribny <jstribny@redhat.com> - 1.7.7-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to multi_json 1.7.7

* Wed Jul 25 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.6-1
- Updated to Multi_Json 1.3.6.
- Specfile cleanup

* Mon Apr 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.0-1
- Rebuilt for scl.
- Updated to 1.2.0.

* Tue Jan 24 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.3-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.3-3
- Removed useless shebang.

* Fri Nov 11 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.3-2
- Review fixes.

* Fri Jul 08 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.3-1
- Initial package
