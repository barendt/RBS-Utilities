#include "Python.h"

static PyObject *
overlap_count(PyObject *self, PyObject *args) {
  int i = 0;
  int j = 0;
  int k = 0;
  int count = 0;
  int haystack_length = 0;
  int needle_length;
  const char* haystack;
  const char* needle;

  if (!PyArg_ParseTuple(args, "ss", &haystack, &needle)) {
    return NULL;
  }

  haystack_length = strlen(haystack);
  needle_length = strlen(needle);

  for (i=0; i < haystack_length; i++) {
    if (haystack[i] == needle[0]) {
      k = i + 1;
      for (j=1; j < needle_length; j++) {
        if (haystack[k] == needle[j]) {
          if (j == needle_length-1) {
            count++;
          }
          k++;          
        }
        else {
          break;
        }
      }      
    }
  }

  return Py_BuildValue("i", count);
}

static PyMethodDef cStrings_methods[] = {
  {"overlap_count", (PyCFunction)overlap_count, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initcStrings() {
  Py_InitModule3("cStrings", cStrings_methods, "docstring");
}
