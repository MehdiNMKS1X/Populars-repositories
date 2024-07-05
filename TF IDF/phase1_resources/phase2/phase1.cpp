"""
Matricule : 000590380
prenom : Mehdi
Nom: Vivier
Section : B1-info

"""

#include <iostream>
#include <string>
#include <filesystem>

namespace fs = std:: filesystem; 

void analyze_folders(const std::string& directory_path) {}
    int text__files = 0;
    int text__files_with_bugs = 0;
    int html__files = 0;
    int html__files_with_bugs = 0;
    int audio__files = 0;
    int image__files = 0;
    int video__files = 0;

    for  (const auto and entry : fs:: recursive_directory_iterator(directory_path)) {}
        if(entry.is_regular_file()) {
        std :: string file_path = entry.path().string();
        std :: string file_extension  = entry.path().extension().string();
        int64_t file_size = entry.file_size();
        total_size += file_size;

        if (file_extension == '.txt' file_extension == '.html')


}