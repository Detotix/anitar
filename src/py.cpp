#include <Python.h>
#include <iostream>
#include <vector>

// Initialize Python and import module once
PyObject* import_python_module(const std::string& module_name) {
    Py_Initialize();
    PyObject* pName = PyUnicode_FromString(module_name.c_str());
    PyObject* pModule = PyImport_Import(pName);
    Py_DECREF(pName);
    if (!pModule) PyErr_Print();
    return pModule;
}

// Call Python function with arbitrary arguments
PyObject* call_python_function(PyObject* pModule, const std::string& func_name, const std::vector<PyObject*>& args) {
    if (!pModule) return nullptr;

    PyObject* pFunc = PyObject_GetAttrString(pModule, func_name.c_str());
    if (!pFunc || !PyCallable_Check(pFunc)) {
        PyErr_Print();
        return nullptr;
    }

    PyObject* pArgs = PyTuple_New(args.size());
    for (size_t i = 0; i < args.size(); ++i) {
        PyTuple_SetItem(pArgs, i, args[i]); // Steals reference
    }

    PyObject* pResult = PyObject_CallObject(pFunc, pArgs);
    Py_DECREF(pArgs);
    Py_DECREF(pFunc);

    if (!pResult) PyErr_Print();
    return pResult;
}

// Cleanup
void finalize_python() {
    Py_Finalize();
}
