#define PY_SSIZE_T_CLEAN 1
#include <Python.h>
#include <bytesobject.h>

#if PY_MAJOR_VERSION >= 3
#define PyInt_Check PyLong_Check
#define PyInt_AsLong PyLong_AsLong
#endif

static PyObject *MakeOTFLibError;

static PyObject* makeotflib_test(PyObject *self, PyObject *args) {
  char output[] = "hello\0";
  return PyBytes_FromStringAndSize((char*)output, 6);
}

PyDoc_STRVAR(test__doc__,
"test() -- return 'hello'.");

static PyMethodDef makeotflib_methods[] = {
  {"test",   makeotflib_test,   METH_VARARGS, test__doc__},
  {NULL, NULL, 0, NULL}
};

PyDoc_STRVAR(makeotflib__doc__,
"Lorem ipsum.\n"
"\n"
"test() -- return 'hello'.\n");

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
