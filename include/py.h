#ifndef PY_H
#define PY_H

#include <Python.h>
#include <iostream>
#include <string>
#include <json.hpp>

using json = nlohmann::json;

class py{
    public:
        static PyObject* import_python_module(const std::string& module_name);
        static PyObject* call_python_function(PyObject* pModule, const std::string& func_name, const std::vector<PyObject*>& args);
        static void finalize_python();
        static json call_python_json_function(PyObject* pModule, const std::string& func_name, const json& input_json);
};

#endif
