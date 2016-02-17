# ------------------------------------------------------------------------------
# MODULE INFORMATIONS ----------------------------------------------------------

__all__ = ['parse_from_regexp']

# ------------------------------------------------------------------------------
# PARSERS ----------------------------------------------------------------------

def parse_from_regexp(path, names, regexp, extractor):
    regexps = {name: regexp(name) for name in names}
    values = {}
    with open(path) as f:
        lines = filter(None, f.read().splitlines())
        for line in lines:
            for name, regexp in regexps.items():
                md = regexp.match(line)
                if md:
                    try:
                        values[name] = extractor(md)
                    except:
                        pass
    return values

# ------------------------------------------------------------------------------
# vim: set filetype=python :
