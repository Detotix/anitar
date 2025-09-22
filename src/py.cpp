#include <Python.h>
#include <iostream>
#include <string>
#include <json.hpp>

using json = nlohmann::json;
// Initialize Python and import module once
PyObject* importmodule(const std::string& module_name) {
    Py_Initialize();
    PyObject* pName = PyUnicode_FromString(module_name.c_str());
    PyObject* pModule = PyImport_Import(pName);
    Py_DECREF(pName);
    if (!pModule) PyErr_Print();
    return pModule;
}

// Call Python function with arbitrary arguments
PyObject* callfunc(PyObject* pModule, const std::string& func_name, const std::vector<PyObject*>& args) {
    if (!pModule) return nullptr;

    PyObject* pFunc = PyObject_GetAttrString(pModule, func_name.c_str());
    if (!pFunc || !PyCallable_Check(pFunc)) {
        PyErr_Print();
        return nullptr;
    }

    PyObject* pArgs = PyTuple_New(args.size());
    for (size_t i = 0; i < args.size(); ++i) {
        PyTuple_SetItem(pArgs, i, args[i]); 
    }

    PyObject* pResult = PyObject_CallObject(pFunc, pArgs);
    Py_DECREF(pArgs);
    Py_DECREF(pFunc);

    if (!pResult) PyErr_Print();
    return pResult;
}

// Cleanup
void finalize() {
    Py_Finalize();
}

json calljsfunc(PyObject* pModule, const std::string& func_name, const json& input_json) {
    if (!pModule) return json();

    PyObject* pFunc = PyObject_GetAttrString(pModule, func_name.c_str());
    if (!pFunc || !PyCallable_Check(pFunc)) {
        PyErr_Print();
        return json();
    }

    std::string json_input_str = input_json.dump();

    PyObject* pArg = PyUnicode_FromString(json_input_str.c_str());
    PyObject* pArgs = PyTuple_Pack(1, pArg);
    Py_DECREF(pArg);

    PyObject* pResult = PyObject_CallObject(pFunc, pArgs);
    Py_DECREF(pArgs);
    Py_DECREF(pFunc);

    if (!pResult) {
        PyErr_Print();
        return json();
    }

    const char* result_cstr = PyUnicode_AsUTF8(pResult);
    std::string result_str = result_cstr ? result_cstr : "";
    Py_DECREF(pResult);

    try {
        return json::parse(result_str);
    } catch (const json::parse_error& e) {
        std::cerr << "JSON parse error: " << e.what() << std::endl;
        return json();
    }
}