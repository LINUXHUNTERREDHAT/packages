let ver = gitea("https://git.linux-gaming.ru", "Linux-Gaming/PortProtonQt");

if ver.starts_with("v") {
    ver = ver.sub_string(1);
}

rpm.version(ver);
