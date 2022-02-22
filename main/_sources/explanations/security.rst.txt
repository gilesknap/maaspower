Security
========

Code Execution
--------------

Note that the command line interface allows the remote execution of any
command on the machine running the webhooks. Make sure good passwords
are used and also use a localhost only service to avoid remote 
execution if possible.

This is less serious than it sounds because the only way to change 
the commands executed is by modifying the config file. So protecting the 
config file via file permissions is also important.

Login
-----

At present maaspower supports the basic authentication method implemented
in Flask and supported in MAAS by adding a username and password to the 
webhook config.

Unless an SSL connection is configured, these credentials will be visible
on the network.

TODO: document setting up an SSL certificate.

The username and password accepted by the server are given in the config
file. Therefore the config file should be kept securely and usually have
file mode of 600. This is how k8s kubectl config is secured.

Network
-------

For the safest results it is recommended to configure the ip_address as 
127.0.0.1 or localhost. Then you would be required to run the webhook service
on the same machine as the MAAS rack server (or servers).

For a production system it is recommended that an SSL connection is used,
and that Flask is configured for a production environment. See

- https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/
