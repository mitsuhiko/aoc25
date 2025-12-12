DAYS := 01 02 03 04 05 06 07 08 09 10 11 12
TEST_TARGETS := $(addprefix test-day,$(DAYS))

.PHONY: test $(TEST_TARGETS) format

test:
	@failed=0; \
	for day in $(DAYS); do \
		if ! $(MAKE) -s test-day$${day}; then \
			failed=1; \
		fi; \
	done; \
	exit $$failed

$(TEST_TARGETS): test-day%:
	@printf "Testing test-day$*... "
	@start=$$(python3 -c 'import time; print(time.time())'); \
	if python3 day$*.py | diff -q - day$*.out > /dev/null 2>&1; then \
		end=$$(python3 -c 'import time; print(time.time())'); \
		elapsed=$$(python3 -c "print(f'{$$end - $$start:.3f}s')"); \
		echo "OK ($$elapsed)"; \
	else \
		echo "FAILED"; \
		python3 day$*.py | diff - day$*.out; \
		exit 1; \
	fi

format:
	uvx ruff format .
