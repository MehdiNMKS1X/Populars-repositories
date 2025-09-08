#include "instruction.hpp"
#include <iostream>
#include <sstream>
#include <algorithm>

// Constructor implementation
Instruction::Instruction(const std::string& instruction_str) {
    // Parse the instruction string
    std::istringstream iss(instruction_str);
    
    // Read the opcode
    iss >> opcode;
    
    // Convert opcode to uppercase for case-insensitive comparison
    std::transform(opcode.begin(), opcode.end(), opcode.begin(), ::toupper);
    
    // Read operands based on the opcode
    if (opcode == "SETv" || opcode == "SETr" || 
        opcode == "ADDv" || opcode == "ADDr" || 
        opcode == "SUBv" || opcode == "SUBr") {
        // These instructions take two operands
        iss >> operand1 >> operand2;
    } else if (opcode == "IFNZ" || opcode == "PUSH" || 
               opcode == "POP" || opcode == "PRINT") {
        // These instructions take one operand
        iss >> operand1;
        operand2 = "";
    } else if (opcode == "LOAD" || opcode == "STORE") {
        // These instructions take two operands (address and register)
        iss >> operand1 >> operand2;
    } else {
        // Unknown opcode or no operands needed
        operand1 = "";
        operand2 = "";
    }
}

// Destructor implementation
Instruction::~Instruction() {
    // No dynamic memory to clean up
}

// Getter for opcode
std::string Instruction::get_opcode() const {
    return opcode;
}

// Getter for first operand
std::string Instruction::get_operand1() const {
    return operand1;
}

// Getter for second operand
std::string Instruction::get_operand2() const {
    return operand2;
}
