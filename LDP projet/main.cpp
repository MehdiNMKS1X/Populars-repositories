#include "matricule.hpp"
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <program_file>" << std::endl;
        return 1;
    }
    
    std::string program_path = argv[1];
    exec(program_path);
    
    return 0;
}