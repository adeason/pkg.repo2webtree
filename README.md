# pkg.repo2webtree

`pkg.repo2webtree` is a Python script that can convert a Solaris IPS pkg
repository into a self-contained plain directory tree suitable for serving over
HTTP. This lets you easily serve a repository of IPS packages via almost any
webserver, possibly a webserver running on another machine that doesn't run
Solaris or know anything about IPS.

IPS itself can be used to serve a repository via Apache with
`pkg.depot-config -F`, but the generated directory is Apache-specific, and
isn't self-contained (it requires disk access to the IPS repository).

## Requirements

`pkg.repo2webtree` is intended to run on Solaris 11.4+. The script itself
requires:

* Python 3.6+
* The `pkg` Python library (generally only available on Solaris)

Running the tests requires `pytest`.

To serve the generated directory tree, you should be able to use almost any
reasonable webserver. The only specific required behaviors are:

* Serving `index.html` for directories (e.g. `versions/0/index.html` is served
  when `/versions/0/` is requested)
* Requests with encoded characters are served either the file path will all
  characters decoded, or the file path all non-slash characters decoded (e.g.
  when `foo%2Fbar%2Cbaz` is requested, either `foo/bar,baz` or `foo%2Fbar,baz`
  is served)

When using Apache, this means the `AllowEncodedSlashes` directive must be set
to either `On` or `NoDecode`. It is not possible to work with the default value
of `Off`, because `pkg install` requests URLs with encoded slashes in them.

The following webservers have been specifically confirmed to work:

* nginx
* Apache (with `AllowEncodedSlashes`)
* Python's `http.server`

## Usage

Generate a standalone directory tree from an existing IPS repository:

```
$ pkg.repo2webtree /export/repository /tmp/pkg
creating /tmp/pkg/versions/0/index.html
creating /tmp/pkg/status/0/index.html
[...]
```

Copy the generated directory tree to an existing webserver:

```
$ rsync -av /tmp/pkg/ pkg.example.com:/srv/www/pkg/
[...]
```

And now the repo can be used like any other IPS repository:

```
$ pkgrepo info -s http://pkg.example.com/pkg
PUBLISHER PACKAGES STATUS           UPDATED
[...]
$ pkg set-publisher -p http://pkg.example.com/pkg
pkg set-publisher:
  Added publisher(s): [...]
```

## Limitations

`pkg.repo2webtree` is only intended for somewhat small repositories. If you use
it for larger repos, you will end up with very large directories (`file/1/`,
and possibly some subdirectories of `manifest/0/`), which may not be good for
performance.

`pkg.repo2webtree` currently only copies an entire IPS repository at once.
There is no functionality for incrementally updating a repo, or for filtering
the repo contents in any way. These features could probably be added easily.

## License

Zero-Clause BSD.
