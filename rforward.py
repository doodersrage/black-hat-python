def main():
    options, server, remote = parse_options()
    password = None
    if options.readpass:
        password = getpass.getpass('Enter SSH password: ')
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    verbose('Connecting to ssh host %s:%d ...' % (server[0], server[1]))
    try:
        client.connect(server[0], server[1], username=options.user,
        key_filename=options.keyfile,
        look_for_keys=options.look_for_keys, password=password)
    except Exception as e:
    print('*** Failed to connect to %s:%d: %r' % (server[0], server[1], e))
    sys.exit(1)
    verbose('Now forwarding remote port %d to %s:%d ...' % (options.port, remote[0], remote[1]))
    try:
        reverse_forward_tunnel(options.port, remote[0], remote[1], client.get_transport())
    except KeyboardInterrupt:
        print('C-c: Port forwarding stopped.')
        sys.exit(0)
