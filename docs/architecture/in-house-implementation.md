# In-house implementation policy

Status: binding architecture constraint

Kuro is intended to become a programming language whose production compiler,
runtime, standard library, package format, and developer tools are authored in
Kuro. We do not solve missing language capabilities by embedding another
language's semantics or application runtime behind Kuro syntax.

## Bootstrap boundary

The current Python implementation is a temporary bootstrap oracle. It exists
to execute the early Kuro sources while Kuro is still too small to compile its
own compiler. It is not the target implementation and must not become a
permanent dependency of Kuro programs or Kuro releases.

The bootstrap exit gate is:

1. Kuro can express its lexer, parser, resolver, typechecker, IR lowering, and
   runtime support without relying on Python behavior for language semantics.
2. A Kuro compiler can compile those Kuro sources into Kuro's own executable
   format.
3. The Kuro-built compiler passes the same differential and regression suite
   as the bootstrap oracle.
4. A clean environment can build and run Kuro programs without Python,
   Node.js, Rust, or another language runtime installed.

## Native boundary

Eventually Kuro must own its code generation and runtime. The lowest-level
backend may emit machine instructions or a documented Kuro bytecode format,
and it may invoke operating-system ABIs or syscalls where an application must
talk to the host OS. Those are platform boundaries, not substitute language
implementations. Kuro's value model, memory rules, errors, I/O APIs, and
application libraries remain defined by Kuro.

## Development order

The implementation order is therefore:

1. Finish a small self-hosting Kuro subset and its core data structures.
2. Port the compiler phases from the Python oracle into Kuro.
3. Define and implement Kuro-owned IR/bytecode and its runtime.
4. Bootstrap the Kuro compiler and compare it against the oracle.
5. Remove Python from the required release path.
6. Add the standard library, modules, package manager, and application APIs
   on top of that owned foundation.

Features that cannot be implemented honestly within this boundary remain
explicitly marked as unavailable; they are not simulated by a hidden foreign
runtime.
