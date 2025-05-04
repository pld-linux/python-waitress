#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module	waitress
Summary:	Waitress WSGI server
Summary(pl.UTF-8):	Serwer WSGI Waitress
Name:		python-%{module}
# keep 1.x here for python2 support
Version:	1.4.4
Release:	4
License:	ZPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/waitress/
Source0:	https://files.pythonhosted.org/packages/source/w/waitress/%{module}-%{version}.tar.gz
# Source0-md5:	079c3c4902b1cb5d0a917276ee70f1df
URL:		https://docs.pylonsproject.org/projects/waitress/
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:41
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3 >= 1.8.1
BuildRequires:	python3-docutils
BuildRequires:	python3-pylons-sphinx-themes >= 1.0.9
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Waitress is meant to be a production-quality pure-Python WSGI server
with very acceptable performance.

%description -l pl.UTF-8
Waitress jest serwerem WSGI tworzonym w czystym Pythonie, z myślą o
produkcyjnej jakości i akceptowalnej wydajności.

%package apidocs
Summary:	API documentation for Python waitress module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona waitress
Group:		Documentation

%description apidocs
API documentation for Python waitress module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona waitress.

%prep
%setup -q -n %{module}-%{version}

%build
%py_build

%if %{with tests}
PYTHONPATH=$(pwd)/src \
%{__python} -m unittest discover -s tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/waitress-serve{,-2}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.txt COPYRIGHT.txt HISTORY.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/waitress-serve-2
%{py_sitescriptdir}/waitress
%{py_sitescriptdir}/waitress-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
