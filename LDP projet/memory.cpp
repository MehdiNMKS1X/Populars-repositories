#include "memory.hpp"
#include <iostream>
#include <cstdlib>

// Memory size constants
const uint8_t STACK_SIZE = 16;
const uint16_t MEMORY_SIZE = 256;

// Memory array for standalone functions
static uint16_t memory_array[MEMORY_SIZE] = {0};

// Stack pointer (starts at the end of the stack area)
static uint8_t SP = STACK_SIZE;

// Memory class implementation
Memory::Memory(size_t size) : mem(size, 0), stack_ptr(STACK_SIZE) {
    // Make sure size is correctly set to MEMORY_SIZE (256)
}

uint16_t& Memory::operator[](uint16_t address) {
    if (address >= mem.size()) {
        std::cerr << "Memory access out of bounds at address " << static_cast<int>(address) << std::endl;
        std::exit(1);
    }
    return mem[address];
}

void Memory::push(uint16_t value) {
    if (stack_ptr <= 0) {
        std::cerr << "Stack overflow" << std::endl;
        std::exit(1);
    }
    
    stack_ptr--;
    mem[stack_ptr] = value;
}

uint16_t Memory::pop() {
    if (stack_ptr >= STACK_SIZE) {
        std::cerr << "Stack underflow" << std::endl;
        std::exit(1);
    }
    
    uint16_t value = mem[stack_ptr];
    stack_ptr++;
    
    return value;
}

// Read a 16-bit value from memory
uint16_t memory_read(uint16_t address) {
    if (address >= MEMORY_SIZE) {
        std::cerr << "Memory read out of bounds at address " << static_cast<int>(address) << std::endl;
        std::exit(1);
    }
    
    return memory_array[address];
}

// Write a 16-bit value to memory
void memory_write(uint16_t address, uint16_t value) {
    if (address >= MEMORY_SIZE) {
        std::cerr << "Memory write out of bounds at address " << static_cast<int>(address) << std::endl;
        std::exit(1);
    }
    
    memory_array[address] = value;
}

// Push a value onto the stack
void stack_push(uint16_t value) {
    // Check if stack is full
    if (SP <= 0) {
        std::cerr << "Stack overflow" << std::endl;
        std::exit(1);
    }
    
    // Decrement SP
    SP--;
    
    // Write value to stack
    memory_array[SP] = value;
}

// Pop a value from the stack
uint16_t stack_pop() {
    // Check if stack is empty
    if (SP >= STACK_SIZE) {
        std::cerr << "Stack underflow" << std::endl;
        std::exit(1);
    }
    
    // Read value from stack
    uint16_t value = memory_array[SP];
    
    // Increment SP
    SP++;
    
    return value;
}