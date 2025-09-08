#ifndef memory_hpp
#define memory_hpp

#include <cstdint>
#include <vector>

// Memory class to encapsulate memory operations
class Memory {
private:
    std::vector<uint16_t> mem;
    size_t stack_ptr;

public:
    // Constructor with memory size
    Memory(size_t size);
    
    // Memory access operators
    uint16_t& operator[](uint16_t address);
    
    // Stack operations
    void push(uint16_t value);
    uint16_t pop();
};

// Standalone memory operations - kept for compatibility
uint16_t memory_read(uint16_t address);
void memory_write(uint16_t address, uint16_t value);

// Standalone stack operations - kept for compatibility
void stack_push(uint16_t value);
uint16_t stack_pop();

#endif // memory_hpp
