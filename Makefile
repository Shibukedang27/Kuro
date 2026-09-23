.PHONY: test native doctor release-check clean-generated

PYTHON ?= ./.venv/bin/python
NATIVE_TARGET ?= aarch64-macos

test:
	$(PYTHON) -m pytest -q

native:
	$(PYTHON) -c 'from compiler.self_host import build_native_artifact_launcher, build_native_codegen, build_native_compiler, build_native_runtime; build_native_compiler(None, "dist/kuro-compiler", target="$(NATIVE_TARGET)"); build_native_runtime(None, "dist/kuro-runtime", target="$(NATIVE_TARGET)"); build_native_artifact_launcher("dist/kuro-bytecode", target="$(NATIVE_TARGET)"); build_native_codegen("dist/kuro-codegen", target="$(NATIVE_TARGET)"); print("native compiler/runtime/bytecode launcher/codegen rebuilt")'

doctor: native
	./bin/kuro-native doctor

release-check: doctor test
	printf 'Print 2 + 3.\n' >/tmp/kuro-release-probe.kuro
	test "$$(./bin/kuro-native run /tmp/kuro-release-probe.kuro)" = "5"
	./bin/kuro-native compile /tmp/kuro-release-probe.kuro >/tmp/kuro-release-probe.kurobc
	test "$$(./bin/kuro-native exec /tmp/kuro-release-probe.kurobc)" = "5"
	./bin/kuro-native codegen /tmp/kuro-release-probe.kurobc >/tmp/kuro-release-probe.s
	clang /tmp/kuro-release-probe.s -o /tmp/kuro-release-probe-native
	test "$$(/tmp/kuro-release-probe-native)" = "5"
	printf 'N = 0; While N is less than 3; Print N. Add 1 to N; Done.\n' >/tmp/kuro-release-loop.kuro
	./bin/kuro-native compile /tmp/kuro-release-loop.kuro >/tmp/kuro-release-loop.kurobc
	./bin/kuro-native codegen /tmp/kuro-release-loop.kurobc >/tmp/kuro-release-loop.s
	clang /tmp/kuro-release-loop.s -o /tmp/kuro-release-loop-native
	test "$$(/tmp/kuro-release-loop-native)" = "$$(printf '0\n1\n2')"
	./dist/kuro-compiler < ./dist/kuro-compiler.source.kuro >/tmp/kuro-release-self-compiler.kurobc
	{ cat /tmp/kuro-release-self-compiler.kurobc; printf 'kuro.input/1\nPrint 6 * 7.\n'; } | ./dist/kuro-bytecode >/tmp/kuro-release-second-stage.kurobc
	test "$$(./dist/kuro-bytecode < /tmp/kuro-release-second-stage.kurobc)" = "42"
	echo "Kuro native developer release verified"

clean-generated:
	find dist -type f -name '*.s' -delete
