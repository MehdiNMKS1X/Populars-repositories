# Makefile

# Compiler and flags
CXX = g++
CXXFLAGS = -std=c++11 -Wall -Werror

# Source files
SOURCES = tf_idf.cpp

# Object files
OBJECTS = $(SOURCES:.cpp=.o)

# Target executable
EXECUTABLE = tf_idf.cpp

# Rules
all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $<

clean:
	rm -f $(OBJECTS) $(EXECUTABLE)

run: $(EXECUTABLE)
	./$(EXECUTABLE)