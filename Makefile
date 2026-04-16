# python-marathon Makefile

.PHONY: man verify completion

# Generate man page from markdown (requires pandoc)
man: docs/marathon.1.md
	@mkdir -p man
	pandoc -s -t man docs/marathon.1.md -o man/marathon.1
	@echo "man/marathon.1 generated — view with: man ./man/marathon.1"

# Run all reference solutions against tests
verify:
	cd exercises && python marathon.py verify

# Generate zsh completion
completion:
	cd exercises && python marathon.py completion zsh > ../completions/_marathon
	@echo "completions/_marathon generated"
