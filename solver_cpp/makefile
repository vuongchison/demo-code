CXX = g++
CXXFLAGS = -std=c++23 -Wall -g

# Phony targets
.PHONY: test clean

# Default target
all: UT sudoku

# Target to run the unit tests
test: UT
	./UT

# Target to build the unit test executable
UT: UT.o solver.o
	$(CXX) $(CXXFLAGS) -o UT UT.o solver.o

# Target for UT.o
UT.o: UT.cpp variable.hpp constraint.hpp solver.hpp
	$(CXX) $(CXXFLAGS) -c UT.cpp

# Target for solver.o
solver.o: solver.cpp solver.hpp constraint.hpp variable.hpp
	$(CXX) $(CXXFLAGS) -c solver.cpp

sudoku.o: sudoku.cpp solver.hpp
	$(CXX) $(CXXFLAGS) -c sudoku.cpp

sudoku: sudoku.o solver.o
	$(CXX) $(CXXFLAGS) -o sudoku sudoku.o solver.o

# Target to clean up
clean:
	rm -f UT UT.o solver.o sudoku.o sudoku