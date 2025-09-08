#ifndef matricule_hpp
#define matricule_hpp

#include <string>
#include <map>
#include <vector>
#include "register.hpp"
#include "instruction.hpp"
#include "memory.hpp"

class Matricule {
private:
    std::map<char, Register> registers;
    Memory memory;
    
    // Add missing function declarations
    uint16_t saturate(int32_t value) const;
    std::string parse_opcode(const std::string& instr);
    std::vector<std::string> parse_operands(const std::string& instr);
    
    // Add memory and stack operations
    // Change address type from uint8_t to uint16_t to support larger address space
    void memory_write(uint16_t address, uint16_t value);
    uint16_t memory_read(uint16_t address);
    void stack_push(uint16_t value);
    uint16_t stack_pop();

public:
    bool skip_next;
    
    Matricule();
    void exec_instruction(const std::string& instr);
};

void exec(const std::string& program_path);

#endif // matricule_hpp
