#ifndef DOTENV_H
#define DOTENV_H

#include <string>

// Load variables from .env file into environment
void loadDotEnv(const std::string &filename = ".env");

#endif
