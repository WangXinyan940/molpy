from contextlib import contextmanager
import warnings
import numpy as np
from pickle_utils import *
import errno
import sys

def _get_stream(filename, openfunction=open, mode='r'):
    """Return open stream if *filename* can be opened with *openfunction* or else ``None``."""
    try:
        stream = openfunction(filename, mode=mode)
    except (IOError, OSError) as err:
        # An exception might be raised due to two reasons, first the openfunction is unable to open the file, in this
        # case we have to ignore the error and return None. Second is when openfunction can't open the file because
        # either the file isn't there or the permissions don't allow access.
        if errno.errorcode[err.errno] in ['ENOENT', 'EACCES']:
            raise sys.exc_info()[1] from err
        return None
    if mode.startswith('r'):
        # additional check for reading (eg can we uncompress) --- is this needed?
        try:
            stream.readline()
        except IOError:
            stream.close()
            stream = None
        except:
            stream.close()
            raise
        else:
            stream.close()
            stream = openfunction(filename, mode=mode)
    return stream


class StreamWarning(Warning):
    """Warning indicating a possible problem with a stream.
    :exc:`StreamWarning` is used when streams are substituted for simple access
    by filename (see in particular
    :class:`~MDAnalysis.lib.util.NamedStream`). This does not work everywhere
    in MDAnalysis (yet).
    """

def hasmethod(obj, m):
    """Return ``True`` if object *obj* contains the method *m*."""
    return hasattr(obj, m) and callable(getattr(obj, m))

def isstream(obj):
    """Detect if `obj` is a stream.
    We consider anything a stream that has the methods
    - ``close()``
    and either set of the following
    - ``read()``, ``readline()``, ``readlines()``
    - ``write()``, ``writeline()``, ``writelines()``
    Parameters
    ----------
    obj : stream or str
    Returns
    -------
    bool
        ``True`` if `obj` is a stream, ``False`` otherwise
    See Also
    --------
    :mod:`io`
    .. versionadded:: 0.9.0
    """
    signature_methods = ("close",)
    alternative_methods = (
        ("read", "readline", "readlines"),
        ("write", "writeline", "writelines"))

    # Must have ALL the signature methods
    for m in signature_methods:
        if not hasmethod(obj, m):
            return False
    # Must have at least one complete set of alternative_methods
    alternative_results = [
        np.all([hasmethod(obj, m) for m in alternatives])
        for alternatives in alternative_methods]
    return np.any(alternative_results)


@contextmanager
def openany(datasource, mode='rt', reset=True):
    """Context manager for :func:`anyopen`.
    Open the `datasource` and close it when the context of the :keyword:`with`
    statement exits.
    `datasource` can be a filename or a stream (see :func:`isstream`). A stream
    is reset to its start if possible (via :meth:`~io.IOBase.seek` or
    :meth:`~cString.StringIO.reset`).
    The advantage of this function is that very different input sources
    ("streams") can be used for a "file", ranging from files on disk (including
    compressed files) to open file objects to sockets and strings---as long as
    they have a file-like interface.
    Parameters
    ----------
    datasource : a file or a stream
    mode : {'r', 'w'} (optional)
        open in r(ead) or w(rite) mode
    reset : bool (optional)
        try to read (`mode` 'r') the stream from the start [``True``]
    Examples
    --------
    Open a gzipped file and process it line by line::
        with openany("input.pdb.gz") as pdb:
            for line in pdb:
                if line.startswith('ATOM'):
                    print(line)
    Open a URL and read it::
       import urllib2
       with openany(urllib2.urlopen("https://www.mdanalysis.org/")) as html:
           print(html.read())
    See Also
    --------
    :func:`anyopen`
    """
    stream = anyopen(datasource, mode=mode, reset=reset)
    try:
        yield stream
    finally:
        stream.close()


def anyopen(datasource, mode='rt', reset=True):
    """Open datasource (gzipped, bzipped, uncompressed) and return a stream.
    `datasource` can be a filename or a stream (see :func:`isstream`). By
    default, a stream is reset to its start if possible (via
    :meth:`~io.IOBase.seek` or :meth:`~cString.StringIO.reset`).
    If possible, the attribute ``stream.name`` is set to the filename or
    "<stream>" if no filename could be associated with the *datasource*.
    Parameters
    ----------
    datasource
        a file (from :class:`file` or :func:`open`) or a stream (e.g. from
        :func:`urllib2.urlopen` or :class:`io.StringIO`)
    mode: {'r', 'w', 'a'} (optional)
        Open in r(ead), w(rite) or a(ppen) mode. More complicated
        modes ('r+', 'w+', ...) are not supported; only the first letter of
        `mode` is used and thus any additional modifiers are silently ignored.
    reset: bool (optional)
        try to read (`mode` 'r') the stream from the start
    Returns
    -------
    file-like object
    See Also
    --------
    :func:`openany`
      to be used with the :keyword:`with` statement.
    .. versionchanged:: 0.9.0
       Only returns the ``stream`` and tries to set ``stream.name = filename`` instead of the previous
       behavior to return a tuple ``(stream, filename)``.
    .. versionchanged:: 2.0.0
       New read handlers support pickle functionality
       if `datasource` is a filename.
       They return a custom picklable file stream in
       :class:`MDAnalysis.lib.picklable_file_io`.
    """
    read_handlers = {'bz2': bz2_pickle_open,
                     'gz': gzip_pickle_open,
                     '': pickle_open}
    write_handlers = {'bz2': bz2.open,
                      'gz': gzip.open,
                      '': open}

    if mode.startswith('r'):
        if isstream(datasource):
            stream = datasource
            try:
                filename = str(stream.name)  # maybe that does not always work?
            except AttributeError:
                filename = "<stream>"
            if reset:
                try:
                    stream.reset()
                except (AttributeError, IOError):
                    try:
                        stream.seek(0)
                    except (AttributeError, IOError):
                        warnings.warn("Stream {0}: not guaranteed to be at the beginning."
                                      "".format(filename),
                                      category=StreamWarning)
        else:
            stream = None
            filename = datasource
            for ext in ('bz2', 'gz', ''):  # file == '' should be last
                openfunc = read_handlers[ext]
                stream = _get_stream(datasource, openfunc, mode=mode)
                if stream is not None:
                    break
            if stream is None:
                raise IOError(errno.EIO, "Cannot open file or stream in mode={mode!r}.".format(**vars()), repr(filename))
    elif mode.startswith('w') or mode.startswith('a'):  # append 'a' not tested...
        if isstream(datasource):
            stream = datasource
            try:
                filename = str(stream.name)  # maybe that does not always work?
            except AttributeError:
                filename = "<stream>"
        else:
            stream = None
            filename = datasource
            name, ext = os.path.splitext(filename)
            if ext.startswith('.'):
                ext = ext[1:]
            if not ext in ('bz2', 'gz'):
                ext = ''  # anything else but bz2 or gz is just a normal file
            openfunc = write_handlers[ext]
            stream = openfunc(datasource, mode=mode)
            if stream is None:
                raise IOError(errno.EIO, "Cannot open file or stream in mode={mode!r}.".format(**vars()), repr(filename))
    else:
        raise NotImplementedError("Sorry, mode={mode!r} is not implemented for {datasource!r}".format(**vars()))
    try:
        stream.name = filename
    except (AttributeError, TypeError):
        pass  # can't set name (e.g. io.StringIO)
    return stream