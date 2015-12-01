#define PY_SSIZE_T_CLEAN 1
#include <Python.h>
#include <bytesobject.h>

#if PY_MAJOR_VERSION >= 3
#define PyInt_Check PyLong_Check
#define PyInt_AsLong PyLong_AsLong
#endif

int main(int argc, char *argv[]);

static PyObject *MakeOTFLibError;

static PyObject* makeotflib_main(PyObject *self, PyObject *args) {
    PyObject *list_obj;
    PyObject *bytes_obj;
    size_t list_len = 0;
    int i;
    int argc = 1;
    int retcode = -1;

    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &list_obj))
        return NULL;

    list_len = PyList_Size(list_obj);
    argc += list_len;

    char **argv = malloc(argc * sizeof(char*));
    argv[0] = "makeotfexe";

    for (i = 0; i < list_len; i++) {
        char *arg_str = NULL;
        size_t arg_len = 0;
        bytes_obj = PyList_GetItem(list_obj, i);
        arg_str = PyBytes_AsString(bytes_obj);
        arg_len = PyBytes_Size(bytes_obj) + 1;
        argv[i+1] = malloc(arg_len * sizeof(char));
        strncpy(argv[i+1], arg_str, arg_len);
    }

    retcode = main(argc, argv);

    for (i = 1; i < argc; i++) {
        free(argv[i]);
    }
    free(argv);

    return PyLong_FromLong(retcode);
}

PyDoc_STRVAR(main__doc__,
"main() -- Run 'makeotfexe'.");

static PyMethodDef makeotflib_methods[] = {
    {"main",   makeotflib_main,   METH_VARARGS, main__doc__},
    {NULL, NULL, 0, NULL}
};

PyDoc_STRVAR(makeotflib__doc__,
"Python wrapper for Adobe FDK's makeotflib.\n"
"\n"
"main() -- Run 'makeotfexe'.\n");

#if PY_MAJOR_VERSION >= 3
#define INIT_MAKEOTFLIB   PyInit__makeotflib
#define CREATE_MAKEOTFLIB PyModule_Create(&_makeotflib_module)
#define RETURN_MAKEOTFLIB return m

static struct PyModuleDef _makeotflib_module = {
    PyModuleDef_HEAD_INIT,
    "_makeotflib",
    makeotflib__doc__,
    0,
    makeotflib_methods,
    NULL,
    NULL,
    NULL
};
#else
#define INIT_MAKEOTFLIB   init_makeotflib
#define CREATE_MAKEOTFLIB Py_InitModule3("_makeotflib", makeotflib_methods, makeotflib__doc__)
#define RETURN_MAKEOTFLIB return
#endif

PyMODINIT_FUNC INIT_MAKEOTFLIB(void) {
    PyObject *m = CREATE_MAKEOTFLIB;

    MakeOTFLibError = PyErr_NewException((char*) "makeotflib.error", NULL, NULL);

    if (MakeOTFLibError != NULL) {
        Py_INCREF(MakeOTFLibError);
        PyModule_AddObject(m, "error", MakeOTFLibError);
    }

    RETURN_MAKEOTFLIB;
}
