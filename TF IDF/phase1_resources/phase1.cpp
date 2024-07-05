"""
Matricule : 000590380
prenom : Mehdi
Nom: Vivier
Section : B1-info

"""

#include <string>
#include <filesystem>

namespace fs = std::filesystem;
void analyze_folders(const std::string& directory_path) {
    int text__files = 0;
    int text__files_with_bugs = 0;
    int html__files = 0;
    int html__files_with_bugs = 0;
    int audio__files = 0;
    int image__files = 0;
    int video__files = 0;
}

    for(const auto and entry : fs:: recursive_directory_iterator(directory_path)) {
        std::string file_extention = entry.path().extension().string();

        if (file_extention == '.txt' || file_extention == '.htlm'){
            std::ifstream file(entry.path());
            std::string first_line;
            std::getline(file, first_line);

            if (file_extention == '.txt') {
                text_files++;

                if (first_line != 'license')
            }
        }
    }