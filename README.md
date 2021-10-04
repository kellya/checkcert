# checkcert

This utility was based off of [this
gist](https://gist.github.com/gdamjan/55a8b9eec6cf7b771f92021d93b87b2c).

checkcert has the logic of that gist wrapped in a click-based CLI and added command-line options
(checkcert --help to see them)

Full documentation is available at
[https://checkcert.readthedocs.io](https://checkcert.readthedocs.io)

# Installation

## from PyPi
pip install checkert

# Usage

When you run `pip install checkcert`, you will get a `checkcert` command.  To
show all the options, simply run `checkcert --help` to get the most-current list
of commands and options.

### Basic Usage
The basic usage is `checkcert example.com`

### Check cert with an alternate port

Anywhere you specify the host, you may use the format `host:port` to specify an
alternate port.  If no port is specified, 443 will be used.  To check something
running on port 8081 for example, execute `checkcert example.com:8081`

### Multiple domains

checkcert will take all domains specified on the command line.  Multiple values
may be specified as `checkcert example.com www.example.com alt.example.com:444`

### Domain list from a file

checkcert can be instructed to pull the list of domains from a file instead with
the --filename option.  The file contents will just be a domain per line
(specified in host:port format, or just host to default to port 443)

create a file named domains.txt with contents like the following

```
example.com
www.example.com
alt.example.com:444
```

Then execute `checkcert --filename domains.txt`
