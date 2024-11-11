import pkg_resources

# List installed packages in the current environment
installed_packages = pkg_resources.working_set
requirements = sorted(
    ["{}=={}".format(pkg.key, pkg.version) for pkg in installed_packages]
)

# Save to requirements.txt
requirements_file_path = "./requirements.txt"
with open(requirements_file_path, "w") as f:
    f.write("\n".join(requirements))

requirements_file_path
