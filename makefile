# Signifies our desired python version
# Makefile macros (or variables) are defined a little bit differently than traditional bash, keep in mind that in the Makefile there's top-level Makefile-only syntax, and everything else is bash script syntax.
PYTHON = python3

# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY = help run


# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help

# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "--------------------------------------------------"
	@echo "----------------------HELP------------------------"
	@echo "--------------------------------------------------"
	@echo "To run the whole project type make run"
	@echo "--------------------------------------------------"

run:
	${PYTHON} preprocessing/close_marketcap_merger.py
	${PYTHON} preprocessing/crypto_selector.py
	${PYTHON} preprocessing/returns_maker.py
	${PYTHON} strats/CW.py
	${PYTHON} strats/EW.py
	${PYTHON} strats/low_beta.py
	${PYTHON} strats/low_vol.py
	${PYTHON} strats/MV.py
	${PYTHON} strats/RP.py
	${PYTHON} metrics_maker.py
	${PYTHON} dashboard.py
