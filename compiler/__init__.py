"""Kuro compiler frontend (Stage 1-4 Python implementation).

Pipeline: source -> lexer -> parser -> AST -> resolver -> typecheck
                  -> lowering -> IR -> interpreter.

See docs/architecture/current-state.md for the audit that preceded this
package, and docs/engineering/ for the ADRs behind its design decisions.
"""

__version__ = "0.8.0-dev"
