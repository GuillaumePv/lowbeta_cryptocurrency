# Signifies our desired python version
# Makefile macros (or variables) are defined a little bit differently than traditional bash, keep in mind that in the Makefile there's top-level Makefile-only syntax, and everything else is bash script syntax.
PYTHON = python3

# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY = help run fetch process model clean


# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help

# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "--------------------------------------------------"
	@echo "----------------------HELP------------------------"
	@echo "--------------------------------------------------"
	@echo "To process data type make process_data"
	@echo "To launch our different strategies type make strats"
	@echo "To obtain metrics type make metrics"
	@echo "To launch our dashboard type make dashboard"
	@echo "To run all project data type make all"
	@echo "To obtain descriptive statistics type make stats"
	@echo "To create our different graph type make visualization"
	@echo "To run the model type make models"
	@echo "To clean "plot" folder type make cleanplots"
	@echo "To clean "latex" folder type make cleanlatex"
	@echo "--------------------------------------------------"

process_data:
	${PYTHON} preprocessing/close_marketcap_merger.py
	${PYTHON} preprocessing/crypto_selector.py
	${PYTHON} preprocessing/returns_maker.py

strats: .FORCE
	${PYTHON} strats/show_parameters.py
	${PYTHON} strats/CW.py
	${PYTHON} strats/EW.py
	${PYTHON} strats/MV.py
	${PYTHON} strats/low_beta.py
	${PYTHON} strats/low_vol.py

metrics:
	${PYTHON} metrics_maker.py

dashboard:
	${PYTHON} dashboard.py

all:
	./launch.sh

process:
	${PYTHON} scripts/process.py

models: .FORCE
	${PYTHON} scripts/models.py

visualization:
	${PYTHON} scripts/visualization.py

.FORCE:

# In this context, the *.project pattern means "anything that has the .project extension"
clean:
	rm -rf *.json *.csv

cleanplots:
	rm -rf plots/*.png
	rm -rf notebooks/*.png

cleanlatex:
	rm -rf latex/*.tex