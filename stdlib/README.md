# Kuro standard library

The first standard-library modules are written in Kuro and imported as normal
source modules. They intentionally use only language operations; there is no
host-language callback hidden behind these APIs.

Current modules: `core.kuro`, `text.kuro`, `collections.kuro`, `math.kuro`,
and `io.kuro`. The library is still pre-1.0: filesystem, networking,
process, time, and platform APIs are not yet specified and therefore are not
pretended to be complete.
