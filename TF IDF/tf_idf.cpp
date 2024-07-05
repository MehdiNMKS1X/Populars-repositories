#include <vector>
#include <fstream> 
#include <sstream>
#include <map>

 std::vector<std::string> readDocument(const std::string& filePath) {
    std::ifstream fileStream(filePath);
    std::vector<std::string> document;
    std::string line;

    while (std::getline(fileStream, line)) {
        std::stringstream ss(line);
        std::string word;
        while(ss >> word) {
            document.push_back(word);
        }
    }

    return document;
}

std::map<std::string, double> computeTF(const std::vector<std ::string >& words) {
    std::map<std::string, double> tf;
    int totalWords = words.size();
    for (const std::string & word : words){
        if(tf.find(word) == tf.end()) {
            tf[word] = 1.0;
        } else {
            tf[word]++;
        }
        tf[word] /= totalWords;
    } 
    return tf;
}

std::map<std::string, double> computeIDF(const std::vector<std ::map<std::string, double> > & documentsTF, int totalDocuments) {
    std::map<std::string, double> idf;
    int numDocumentsCoutainingsWord;
    for(const std::map<std::string, double >& document : documentsTF){
        numDocumentsCoutainingsWord = 0;
        for (const auto& entry : document) {
            if (idf.find(entry.first) == idf.end()) {
                if (entry.second > 0){
                    numDocumentsCoutainingsWord++;
                }
            }
        }
        for (const auto& entry : document){
            if (idf.find(entry.first) == idf.end()){
                idf[entry.first] = std::log((double)totalDocuments / numDocumentsCoutainingsWord);
            }
        }
    }
    return idf;
}
std::map<std::string, double> calculateTFIDF(const std::map< std::string, double > & tf, const std::map<std::string, double >& idf);

void displayTFIDFScores(const std::map<std::string, double>& tfidfScores);


int main (){
    std::string baseName = "Doc";
    std::string extension = ".txt";
    for (int i = 1; i <= 8; i++) {

    }
    return 0;
}

