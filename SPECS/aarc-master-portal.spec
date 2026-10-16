Name:           aarc-master-portal
Version:        0.2.7
Release:        1%{?dist}
Summary:        AARC Master Portal
License:        Apache-2.0
URL:            https://github.com/rcauth-eu/aarc-master-portal

# Macro for directory path
%global tomcat_webapps_dir /var/lib/tomcat/webapps
%global server_tools_dir /var/www/server/tools

# Prebuilt artifacts are copied in from SOURCES/
Source0:        https://github.com/rcauth-eu/aarc-master-portal/releases/download/v%{version}/mp-oa2-client.war
Source1:        https://github.com/rcauth-eu/aarc-master-portal/releases/download/v%{version}/mp-oa2-server.war
Source2:        https://github.com/rcauth-eu/aarc-master-portal/releases/download/v%{version}/oa2-cli.jar#/mp-oa2-cli.jar
Source3:        https://github.com/rcauth-eu/aarc-ssh-portal/releases/download/v%{version}/sshkey-portal.war
Source4:        https://github.com/rcauth-eu/aarc-vo-portal/releases/download/v%{version}/vo-portal.war

BuildArch:      noarch

# Tomcat must exist and own the target directory before this package installs.
Requires: (tomcat >= 1:9 with tomcat < 1:10)

%description
Installs the RCauth.eu / AARC Master Portal components.

These are prebuilt Maven artifacts (see the aarc-master-portal,
aarc-ssh-portal, and aarc-vo-portal build instructions).
This package only handles their deployment layout, ownership, and permissions.

%prep
# Nothing to unpack/patch — the Source files are already built artifacts.
# Place them under ~/rpmbuild/SOURCES/ before running rpmbuild.

%build
# Nothing to compile.

%install
# buildroot - temporary staging directory
install -d -m 0755 %{buildroot}%{tomcat_webapps_dir}
install -d -m 0755 %{buildroot}%{server_tools_dir}

# 0644 - owner read/write, group/other read-only
install -m 0644 %{SOURCE0} %{buildroot}%{tomcat_webapps_dir}/mp-oa2-client.war
install -m 0644 %{SOURCE1} %{buildroot}%{tomcat_webapps_dir}/mp-oa2-server.war
install -m 0644 %{SOURCE2} %{buildroot}%{server_tools_dir}/oa2-cli.jar
install -m 0644 %{SOURCE3} %{buildroot}%{tomcat_webapps_dir}/sshkey-portal.war
install -m 0644 %{SOURCE4} %{buildroot}%{tomcat_webapps_dir}/vo-portal.war

# Every file the RPM install and track (for upgrades/removal) must be listed here, or the build fails with "unpackaged files"
%files
%attr(0644, tomcat, tomcat) %{tomcat_webapps_dir}/mp-oa2-client.war
%attr(0644, tomcat, tomcat) %{tomcat_webapps_dir}/mp-oa2-server.war
%attr(0644, tomcat, tomcat) %{server_tools_dir}/oa2-cli.jar
%attr(0644, tomcat, tomcat) %{tomcat_webapps_dir}/sshkey-portal.war
%attr(0644, tomcat, tomcat) %{tomcat_webapps_dir}/vo-portal.war

%post
# Tomcat will auto-explode/deploy new WARs on next restart.
# If this command fails, don't fail the whole RPM install
systemctl try-restart tomcat.service >/dev/null 2>&1 || :

%postun
if [ $1 -eq 0 ]; then
    # For full uninstall (not upgrade) — clean up exploded webapp dirs Tomcat
    # creates alongside the WARs, which rpm won't own/remove itself.
    rm -rf %{tomcat_webapps_dir}/mp-oa2-client
    rm -rf %{tomcat_webapps_dir}/mp-oa2-server
    rm -rf %{tomcat_webapps_dir}/sshkey-portal
    rm -rf %{tomcat_webapps_dir}/vo-portal
    # Clean up Tomcat's workdir on uninstall. Compiled JSPs and session data are left in this directory
    rm -rf /var/cache/tomcat/work/Catalina/localhost/mp-oa2-client
    rm -rf /var/cache/tomcat/work/Catalina/localhost/mp-oa2-server
    rm -rf /var/cache/tomcat/work/Catalina/localhost/sshkey-portal
    rm -rf /var/cache/tomcat/work/Catalina/localhost/vo-portal
    systemctl try-restart tomcat.service >/dev/null 2>&1 || :
fi

%changelog
* Wed Oct 10 2026 Hieu <hieu.le@stfc.ac.uk> - 0.2.7-1
- Initial packaging of aarc-master-portal