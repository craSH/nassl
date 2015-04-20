#!/usr/bin/env python2.7
"""
File Copyleft 2013 Ian Gallagher <crash@neg9.org>
Licensed under the GPLv2; see ./LICENSE
"""
import sys, urllib2, tarfile, hashlib

# URLs and SHA384 of files we need
deps = [('http://zlib.net/zlib-1.2.8.tar.gz',
         'ce7147f4568e01922a5d3cb7db56427b54ea2e84a47aea2a999d2f3af2b1e034d90509b449643641bf4c8bfbc9ad0bc7'),
        ('https://www.openssl.org/source/openssl-1.0.2a.tar.gz',
         'ea6e0d3afae2b040b6ce934e5ba418c552d088baa358d7232c6c3795c11c247e31c35bca1314e530718101efd1df62ff')]

def fetch_file(url, trusted_digest, debug=0, insecure=False):
    url_obj = urllib2.urlopen(url)
    fileobj = urllib2.StringIO(url_obj.read())

    fetched_digest = hashlib.new('sha384', fileobj.read())
    fileobj.reset()

    if fetched_digest.hexdigest() != trusted_digest:
        if debug > 0: print >>sys.stderr, "WARNING: File checksum for %s did not match, file may be tampered with or corrupt!" % url
        if insecure:
            return fileobj
        else:
            print >>sys.stderr, "Aborting to to failed file checksum."
            return None
    else:
        if debug > 1: print >>sys.stderr, "File checksum for %s matched" %url
        return fileobj

def extract_tgz(fileobj, dest_path='./', debug=0):
    if fileobj:
        try:
            tgz = tarfile.open(fileobj=fileobj)
            tgz.extractall()
        except Exception as ex:
            raise
        finally:
            fileobj.close()

    else:
        if debug > 0: print >>sys.stderr, "No file object provided for extraction."

def main():
    import optparse
    parser = optparse.OptionParser(usage="Usage: %prog [options]")

    parser.add_option('-d', '--debug', dest='debug', type='int', default=1, help='Debug level (0, 1, 2; default 1)')
    parser.add_option('-k', '--insecure', dest='insecure', action='store_true', default=False, help='Insecure mode - do not check file hashes')

    (options, args) = parser.parse_args()

    for dep in deps:
        print "Fetching and extracting %s" % dep[0]
        saved_file = fetch_file(dep[0], dep[1], debug=options.debug, insecure=options.insecure)
        extract_tgz(saved_file, debug=options.debug)

    return(0)

if '__main__' == __name__:
    sys.exit(main())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
